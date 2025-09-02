#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Medical Journal Entry Processor
Extracts and cleans all 79 medical journal entries from medical.md
Following 1177_cleaner_prompt.txt specifications
"""

import re
from datetime import datetime
from typing import List, Dict, Any

def read_medical_file(filename: str) -> str:
    """Read the medical.md file with proper encoding"""
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def extract_medical_entries(content: str) -> List[Dict[str, Any]]:
    """Extract all medical journal entries from the content"""
    entries = []
    
    # Find actual entry starts - lines that begin new medical entries
    # These are the main entry types that start a new journal entry
    entry_start_patterns = [
        r'^Besöksanteckning (\d{4}-\d{2}-\d{2}(?:\s+\d{2}:\d{2})?)',
        r'^Anteckning utan fysiskt möte (\d{4}-\d{2}-\d{2}(?:\s+\d{2}:\d{2})?)',
        r'^Ambulans (\d{4}-\d{2}-\d{2}(?:\s+\d{2}:\d{2})?)',
        r'^Operation (\d{4}-\d{2}-\d{2}(?:\s+\d{2}:\d{2})?)',
        # Lab results that are standalone
        r'^Slutsvar$'  # Usually followed by provtagningstid
    ]
    
    lines = content.split('\n')
    entry_starts = []
    
    for i, line in enumerate(lines):
        line = line.strip()
        # Check for main entry types
        for pattern in entry_start_patterns:
            if re.match(pattern, line):
                entry_starts.append((i, line, 'main'))
                break
        
        # Special handling for lab results
        if line == 'Slutsvar' and i < len(lines) - 1:
            # Check if next line contains 'Provtagningstid'
            next_line = lines[i+1].strip() if i < len(lines) - 1 else ""
            if 'Provtagningstid' in next_line or re.search(r'\d{4}-\d{2}-\d{2}', next_line):
                entry_starts.append((i, line, 'lab'))
    
    print(f"Found {len(entry_starts)} main entry start points")
    
    # Now extract the content between entries
    for i, (start_line_num, start_line, entry_type) in enumerate(entry_starts):
        # Find end of this entry (start of next entry or end of file)
        if i < len(entry_starts) - 1:
            end_line_num = entry_starts[i + 1][0]
        else:
            end_line_num = len(lines)
        
        # Extract entry content
        entry_lines = lines[start_line_num:end_line_num]
        entry_content = '\n'.join(entry_lines).strip()
        
        # Extract date from the entry
        date_match = re.search(r'(\d{4}-\d{2}-\d{2}(?:\s+\d{2}:\d{2})?)', entry_content)
        entry_date = date_match.group(1) if date_match else "DATUM SAKNAS"
        
        entries.append({
            'index': i + 1,
            'date': entry_date,
            'type': entry_type,
            'start_line': start_line,
            'content': entry_content,
            'line_count': len(entry_lines)
        })
    
    # Sort entries by date (newest first, as in original)
    entries.sort(key=lambda x: x['date'], reverse=True)
    
    return entries

def clean_entry(raw_entry: str, index: int, total: int) -> str:
    """Clean a single entry according to 1177_cleaner_prompt.txt specifications"""
    # This will be implemented with detailed cleaning logic
    lines = raw_entry.strip().split('\n')
    
    # Extract basic info
    entry_type = "Okänd"
    date_time = "DATUM SAKNAS"
    healthcare_provider = ""
    care_unit = ""
    
    # Try to identify entry type and date from first lines
    for line in lines[:5]:
        if 'Besöksanteckning' in line:
            entry_type = "Besöksanteckning"
            date_match = re.search(r'(\d{4}-\d{2}-\d{2}(?:\s+\d{2}:\d{2})?)', line)
            if date_match:
                date_time = date_match.group(1)
        elif 'Anteckning utan fysiskt möte' in line:
            entry_type = "Anteckning utan fysiskt möte"
            date_match = re.search(r'(\d{4}-\d{2}-\d{2}(?:\s+\d{2}:\d{2})?)', line)
            if date_match:
                date_time = date_match.group(1)
        elif 'Diagnos:' in line:
            entry_type = "Diagnos"
            date_match = re.search(r'(\d{4}-\d{2}-\d{2}(?:\s+\d{2}:\d{2})?)', line)
            if date_match:
                date_time = date_match.group(1)
    
    # Build cleaned chunk
    chunk = f"=== CHUNK {index}/{total} ===\n"
    chunk += f"Typ: {entry_type}\n"
    chunk += f"DatumTid: {date_time}\n"
    chunk += f"Vårdpersonal: {healthcare_provider}\n"
    chunk += f"Vårdenhet: {care_unit}\n"
    
    # Add raw content for now (will be refined)
    chunk += "\nRådata:\n"
    chunk += raw_entry[:500] + "..." if len(raw_entry) > 500 else raw_entry
    
    chunk += f"\n=== END CHUNK {index}/{total} ===\n\n"
    
    return chunk

def main():
    """Main processing function"""
    print("Processing medical journal entries...")
    
    # Read the medical file
    try:
        content = read_medical_file('medical.md')
        print(f"Read file: {len(content)} characters")
    except Exception as e:
        print(f"Error reading file: {e}")
        return
    
    # Extract entries
    entries = extract_medical_entries(content)
    print(f"Extracted {len(entries)} main entries")
    
    if entries:
        # Show summary of entries
        print(f"\nEntry breakdown:")
        entry_years = {}
        for entry in entries:
            year = entry['date'][:4] if len(entry['date']) >= 4 else 'UNKNOWN'
            entry_years[year] = entry_years.get(year, 0) + 1
        
        total_identified = 0
        for year, count in sorted(entry_years.items()):
            print(f"  {year}: {count} entries")
            if year != 'UNKNOWN':
                total_identified += count
        
        print(f"\nTotal main entries identified: {total_identified}")
        
        # Show first few entries for verification
        print(f"\nFirst 5 entries:")
        for i, entry in enumerate(entries[:5]):
            print(f"  {i+1}. {entry['date']} - {entry['start_line'][:50]}...")
        
        print(f"\nLast 5 entries:")
        for i, entry in enumerate(entries[-5:], len(entries)-4):
            print(f"  {i}. {entry['date']} - {entry['start_line'][:50]}...")
    
    else:
        print("No entries found - checking content structure...")
        # Debug: show first 20 lines that contain dates
        lines = content.split('\n')
        date_lines = []
        for i, line in enumerate(lines):
            if re.search(r'20\d\d-\d\d-\d\d', line):
                date_lines.append(f"  Line {i+1}: {line.strip()}")
                if len(date_lines) >= 20:
                    break
        
        print("Lines containing dates:")
        for line in date_lines:
            print(line)

if __name__ == "__main__":
    main()