#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Medical Encounter Extractor - Groups related records into distinct encounters
Identifies the 79 main medical encounters from medical.md
"""

import re
from datetime import datetime, timedelta
from typing import List, Dict, Any, Set
from collections import defaultdict

def read_medical_file(filename: str) -> str:
    """Read the medical.md file with proper encoding"""
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def extract_all_records(content: str) -> List[Dict[str, Any]]:
    """Extract all medical records including visits, diagnoses, medications, lab results"""
    records = []
    
    # Main entry patterns - these typically start new medical encounters
    main_entry_patterns = [
        (r'^Besöksanteckning (\d{4}-\d{2}-\d{2}(?:\s+\d{2}:\d{2})?)', 'Besöksanteckning'),
        (r'^Anteckning utan fysiskt möte (\d{4}-\d{2}-\d{2}(?:\s+\d{2}:\d{2})?)', 'Anteckning utan fysiskt möte'),
        (r'^Ambulans (\d{4}-\d{2}-\d{2}(?:\s+\d{2}:\d{2})?)', 'Ambulans'),
        (r'^Operation (\d{4}-\d{2}-\d{2}(?:\s+\d{2}:\d{2})?)', 'Operation')
    ]
    
    # Related records - these usually belong to the nearest main encounter
    related_patterns = [
        (r'^Diagnos: .+ (\d{4}-\d{2}-\d{2}(?:\s+\d{2}:\d{2})?)', 'Diagnos'),
        (r'^[A-Z][a-zA-ZåäöÅÄÖ\s]+ (\d{4}-\d{2}-\d{2}(?:\s+\d{2}:\d{2})?)', 'Läkemedel'),  # Medicine entries
        (r'^Slutsvar', 'Provsvar')  # Lab results
    ]
    
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        line_stripped = line.strip()
        if not line_stripped:
            continue
            
        record_found = False
        
        # Check for main entry patterns
        for pattern, record_type in main_entry_patterns:
            match = re.match(pattern, line_stripped)
            if match:
                date_time = match.group(1)
                
                # Find the end of this record
                record_content = [line_stripped]
                j = i + 1
                while j < len(lines):
                    next_line = lines[j].strip()
                    
                    # Stop if we hit another main entry or related entry with different date
                    is_new_entry = False
                    for p, _ in main_entry_patterns + related_patterns:
                        if re.match(p, next_line):
                            # Check if it's the same date/time
                            next_match = re.search(r'\d{4}-\d{2}-\d{2}(?:\s+\d{2}:\d{2})?', next_line)
                            if next_match and next_match.group(0) != date_time:
                                is_new_entry = True
                                break
                    
                    if is_new_entry:
                        break
                    
                    record_content.append(next_line)
                    j += 1
                
                records.append({
                    'type': record_type,
                    'date_time': date_time,
                    'date': date_time.split()[0],  # Extract date part
                    'time': date_time.split()[1] if ' ' in date_time else '',
                    'line_start': i,
                    'content': '\n'.join(record_content),
                    'is_main_entry': True
                })
                record_found = True
                break
        
        # If not a main entry, check for related patterns
        if not record_found:
            for pattern, record_type in related_patterns:
                match = re.match(pattern, line_stripped)
                if match or (record_type == 'Provsvar' and line_stripped == 'Slutsvar'):
                    # Extract date from content
                    date_match = None
                    if match and len(match.groups()) > 0:
                        date_time = match.group(1)
                    else:
                        # Look for date in surrounding lines
                        search_lines = lines[max(0, i-5):min(len(lines), i+10)]
                        for search_line in search_lines:
                            date_match = re.search(r'(\d{4}-\d{2}-\d{2}(?:\s+\d{2}:\d{2})?)', search_line)
                            if date_match:
                                date_time = date_match.group(1)
                                break
                        
                        if not date_match:
                            continue  # Skip if no date found
                    
                    # Extract content for this record
                    record_content = [line_stripped]
                    j = i + 1
                    content_length = 0
                    while j < len(lines) and content_length < 50:  # Limit related record size
                        next_line = lines[j].strip()
                        if not next_line:
                            j += 1
                            continue
                            
                        # Stop if we hit another entry
                        is_new_entry = any(re.match(p, next_line) for p, _ in main_entry_patterns + related_patterns)
                        if is_new_entry:
                            break
                            
                        record_content.append(next_line)
                        content_length += 1
                        j += 1
                    
                    records.append({
                        'type': record_type,
                        'date_time': date_time,
                        'date': date_time.split()[0],
                        'time': date_time.split()[1] if ' ' in date_time else '',
                        'line_start': i,
                        'content': '\n'.join(record_content),
                        'is_main_entry': False
                    })
                    record_found = True
                    break
    
    return records

def group_into_encounters(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Group related records into distinct medical encounters"""
    # Group records by date first
    by_date = defaultdict(list)
    for record in records:
        by_date[record['date']].append(record)
    
    encounters = []
    
    for date, date_records in by_date.items():
        # Sort by time if available
        date_records.sort(key=lambda x: x.get('time', ''))
        
        # Find main entries for this date
        main_entries = [r for r in date_records if r['is_main_entry']]
        related_entries = [r for r in date_records if not r['is_main_entry']]
        
        if main_entries:
            # Each main entry becomes an encounter
            for main_entry in main_entries:
                encounter = {
                    'date': date,
                    'main_record': main_entry,
                    'related_records': [],
                    'all_content': [main_entry['content']]
                }
                
                # Add related records from same date/time
                main_time = main_entry.get('time', '')
                for related in related_entries:
                    # If times match or are within reasonable proximity, include
                    related_time = related.get('time', '')
                    if not main_time or not related_time or abs_time_diff(main_time, related_time) <= 60:  # Within 1 hour
                        encounter['related_records'].append(related)
                        encounter['all_content'].append(related['content'])
                
                encounters.append(encounter)
        
        elif related_entries:
            # Create encounter from related entries only (rare case)
            encounter = {
                'date': date,
                'main_record': related_entries[0],  # Use first as main
                'related_records': related_entries[1:],
                'all_content': [r['content'] for r in related_entries]
            }
            encounters.append(encounter)
    
    # Sort encounters by date (newest first)
    encounters.sort(key=lambda x: x['date'], reverse=True)
    
    return encounters

def abs_time_diff(time1: str, time2: str) -> int:
    """Calculate absolute difference between two times in minutes"""
    try:
        if not time1 or not time2:
            return 0
            
        h1, m1 = map(int, time1.split(':'))
        h2, m2 = map(int, time2.split(':'))
        
        total_min1 = h1 * 60 + m1
        total_min2 = h2 * 60 + m2
        
        return abs(total_min1 - total_min2)
    except:
        return 0

def analyze_encounters(encounters: List[Dict[str, Any]]) -> None:
    """Analyze the extracted encounters"""
    print(f"Total encounters found: {len(encounters)}")
    
    # Group by year
    by_year = defaultdict(int)
    for enc in encounters:
        year = enc['date'][:4]
        by_year[year] += 1
    
    print("\nEncounters by year:")
    total = 0
    for year in sorted(by_year.keys()):
        count = by_year[year]
        print(f"  {year}: {count} encounters")
        total += count
    
    print(f"\nTotal: {total} encounters")
    
    # Show types of main records
    main_types = defaultdict(int)
    for enc in encounters:
        main_types[enc['main_record']['type']] += 1
    
    print(f"\nEncounter types:")
    for enc_type, count in main_types.items():
        print(f"  {enc_type}: {count}")
    
    # Show recent encounters
    print(f"\nMost recent 10 encounters:")
    for i, enc in enumerate(encounters[:10]):
        main = enc['main_record']
        related_count = len(enc['related_records'])
        print(f"  {i+1}. {enc['date']} - {main['type'][:30]} (+{related_count} related)")

def main():
    """Main processing function"""
    print("Extracting medical encounters...")
    
    # Read the medical file
    try:
        content = read_medical_file('medical.md')
        print(f"Read file: {len(content)} characters")
    except Exception as e:
        print(f"Error reading file: {e}")
        return
    
    # Extract all records
    print("Extracting all medical records...")
    records = extract_all_records(content)
    print(f"Found {len(records)} total records")
    
    # Group into encounters
    print("Grouping records into encounters...")
    encounters = group_into_encounters(records)
    
    # Analyze results
    analyze_encounters(encounters)
    
    # Save encounter list for processing
    print(f"\nSaving encounter data...")
    import json
    encounter_data = []
    for i, enc in enumerate(encounters):
        encounter_data.append({
            'index': i + 1,
            'date': enc['date'],
            'type': enc['main_record']['type'],
            'content_preview': enc['main_record']['content'][:200] + "..." if len(enc['main_record']['content']) > 200 else enc['main_record']['content'],
            'related_count': len(enc['related_records']),
            'full_content': '\n\n=== MAIN RECORD ===\n' + enc['main_record']['content'] + 
                           '\n\n=== RELATED RECORDS ===\n' + '\n\n'.join([r['content'] for r in enc['related_records']]) if enc['related_records'] else enc['main_record']['content']
        })
    
    with open('encounters.json', 'w', encoding='utf-8') as f:
        json.dump(encounter_data, f, ensure_ascii=False, indent=2)
    
    print(f"Saved {len(encounter_data)} encounters to encounters.json")

if __name__ == "__main__":
    main()