#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filter to 79 Main Medical Encounters
Identifies the most significant medical encounters from the complete set
"""

import json
import re
from typing import List, Dict, Any
from collections import defaultdict

def load_encounters() -> List[Dict[str, Any]]:
    """Load encounters from JSON file"""
    with open('encounters.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def is_significant_encounter(encounter: Dict[str, Any]) -> bool:
    """
    Determine if an encounter is significant enough to be one of the 79 main encounters
    Priority order:
    1. Physical visits (Besöksanteckning) 
    2. Ambulans/Emergency visits
    3. Operations/Procedures
    4. Significant remote consultations (Anteckning utan fysiskt möte) with substantial content
    5. Lab results with abnormal findings
    """
    
    enc_type = encounter['type']
    content = encounter.get('full_content', '')
    
    # High priority encounters
    if enc_type in ['Besöksanteckning', 'Operation', 'Ambulans']:
        return True
    
    # Lab results - only if significant (abnormal values, new findings)
    if enc_type == 'Provsvar':
        # Check for abnormal markers (*) or significant findings
        if '*' in content or 'abnorm' in content.lower() or 'förhöj' in content.lower():
            return True
        return False
    
    # Remote consultations - only if substantial
    if enc_type == 'Anteckning utan fysiskt möte':
        # Check content length and significance indicators
        content_length = len(content)
        significance_indicators = [
            'remiss', 'diagnos', 'medicin', 'behandling', 'symtom', 
            'bedömning', 'planering', 'förvärr', 'akut', 'ny'
        ]
        
        # Must have reasonable content length AND significance indicators
        if content_length > 300 and any(indicator in content.lower() for indicator in significance_indicators):
            return True
        
        # Always include if it's the only encounter on that date
        return False
    
    # Medications - only significant changes (new starts, major dosage changes)
    if enc_type == 'Läkemedel':
        if any(word in content.lower() for word in ['insatt', 'utsatt', 'ny', 'ändrat', 'ökat']):
            return True
        return False
    
    # Diagnoses - always significant
    if enc_type == 'Diagnos':
        return True
    
    return False

def filter_to_main_encounters(encounters: List[Dict[str, Any]], target_count: int = 79) -> List[Dict[str, Any]]:
    """
    Filter encounters to the most significant ones
    """
    
    # First pass - get all significant encounters
    significant = []
    for enc in encounters:
        if is_significant_encounter(enc):
            significant.append(enc)
    
    print(f"Found {len(significant)} significant encounters")
    
    if len(significant) <= target_count:
        print(f"Using all {len(significant)} significant encounters")
        return significant
    
    # If we have too many, prioritize further
    print(f"Need to reduce from {len(significant)} to {target_count}")
    
    # Priority scoring
    def get_priority_score(enc):
        enc_type = enc['type']
        content = enc.get('full_content', '')
        date = enc['date']
        
        score = 0
        
        # Type priority
        type_scores = {
            'Besöksanteckning': 100,
            'Operation': 95,
            'Ambulans': 90,
            'Diagnos': 85,
            'Provsvar': 60,
            'Anteckning utan fysiskt möte': 50,
            'Läkemedel': 30
        }
        score += type_scores.get(enc_type, 0)
        
        # Content richness (more detailed = higher priority)
        content_length = len(content)
        if content_length > 2000:
            score += 20
        elif content_length > 1000:
            score += 10
        elif content_length > 500:
            score += 5
        
        # Recent entries get slight boost
        year = int(date[:4])
        if year >= 2020:
            score += 10
        elif year >= 2015:
            score += 5
        
        # Clinical significance indicators
        clinical_keywords = [
            'akut', 'svår', 'kraftig', 'plötslig', 'försämr', 'förvärr',
            'smärta', 'feber', 'blödning', 'andnöd', 'bröstsmärta',
            'medvetslös', 'kramper', 'syncope', 'hypertoni', 'diabetes'
        ]
        
        keyword_count = sum(1 for keyword in clinical_keywords if keyword in content.lower())
        score += keyword_count * 2
        
        return score
    
    # Score and sort
    scored = [(enc, get_priority_score(enc)) for enc in significant]
    scored.sort(key=lambda x: x[1], reverse=True)
    
    # Take top encounters
    top_encounters = [enc for enc, score in scored[:target_count]]
    
    # Sort back by date (newest first)
    top_encounters.sort(key=lambda x: x['date'], reverse=True)
    
    return top_encounters

def analyze_main_encounters(encounters: List[Dict[str, Any]]) -> None:
    """Analyze the filtered main encounters"""
    print(f"\nMain encounters analysis:")
    print(f"Total: {len(encounters)} encounters")
    
    # By year
    by_year = defaultdict(int)
    for enc in encounters:
        year = enc['date'][:4]
        by_year[year] += 1
    
    print(f"\nBy year:")
    for year in sorted(by_year.keys()):
        count = by_year[year]
        print(f"  {year}: {count} encounters")
    
    # By type
    by_type = defaultdict(int)
    for enc in encounters:
        by_type[enc['type']] += 1
    
    print(f"\nBy type:")
    for enc_type, count in by_type.items():
        print(f"  {enc_type}: {count}")
    
    # Sample entries
    print(f"\nFirst 10 encounters:")
    for i, enc in enumerate(encounters[:10]):
        content_preview = enc['content_preview'][:100] + "..." if len(enc['content_preview']) > 100 else enc['content_preview']
        print(f"  {i+1}. {enc['date']} - {enc['type']}: {content_preview}")

def main():
    """Main function"""
    print("Filtering to main medical encounters...")
    
    # Load all encounters
    encounters = load_encounters()
    print(f"Loaded {len(encounters)} total encounters")
    
    # Filter to main 79
    main_encounters = filter_to_main_encounters(encounters, 79)
    
    # Analyze results
    analyze_main_encounters(main_encounters)
    
    # Save main encounters
    with open('main_encounters.json', 'w', encoding='utf-8') as f:
        json.dump(main_encounters, f, ensure_ascii=False, indent=2)
    
    print(f"\nSaved {len(main_encounters)} main encounters to main_encounters.json")

if __name__ == "__main__":
    main()