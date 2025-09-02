#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive Medical Record Cleaner and Formatter
Creates structured CHUNKS following 1177_cleaner_prompt.txt specifications
Processes all 79 main medical encounters
"""

import json
import re
from typing import List, Dict, Any, Tuple
from datetime import datetime

def load_main_encounters() -> List[Dict[str, Any]]:
    """Load the 79 main encounters"""
    with open('main_encounters.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def normalize_vitals(text: str) -> str:
    """Normalize vital signs according to specifications"""
    # Blood pressure: XXX/YY mmHg (not mm[Hg])
    text = re.sub(r'(\d+)/(\d+)\s*mm\[?Hg\]?', r'\1/\2 mmHg', text)
    
    # Pulse: XX /min
    text = re.sub(r'(\d+)\s*/min', r'\1 /min', text)
    text = re.sub(r'Puls\s*(\d+)', r'Puls=\1/min', text)
    
    # SpO2: XX% (not "XX %")
    text = re.sub(r'(\d+)\s*%', r'\1%', text)
    text = re.sub(r'SpO2.*?(\d+)%', r'SpO2=\1%', text)
    
    # Temperature: XX.X°C
    text = re.sub(r'(\d+[,.]?\d*)\s*°C', r'\1°C', text)
    text = re.sub(r'Temperatur.*?(\d+[,.]?\d*)°C', r'Temp=\1°C', text)
    
    # Respiratory rate: XX /min
    text = re.sub(r'Andningsfrekvens.*?(\d+)\s*/min', r'AF=\1 /min', text)
    
    return text

def extract_structured_data(content: str) -> Dict[str, Any]:
    """Extract structured data from encounter content"""
    data = {
        'typ': 'Okänd',
        'datum_tid': '',
        'vardpersonal': '',
        'vardenhet': '',
        'kontaktorsak': '',
        'anamnes_aktuellt': '',
        'status': {},
        'matt': {},
        'lab': [],
        'operation': '',
        'ekg_imaging': '',
        'bedomning': '',
        'planering': '',
        'diagnoser': [],
        'lakemedel': [],
        'citat': []
    }
    
    lines = content.split('\n')
    current_section = None
    current_content = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Detect entry type and date
        if re.match(r'^(Besöksanteckning|Anteckning utan fysiskt möte|Operation|Ambulans)', line):
            match = re.search(r'(\d{4}-\d{2}-\d{2}(?:\s+\d{2}:\d{2})?)', line)
            if match:
                data['datum_tid'] = match.group(1)
            
            if 'Besöksanteckning' in line:
                data['typ'] = 'Besöksanteckning'
            elif 'Anteckning utan fysiskt möte' in line:
                data['typ'] = 'Anteckning utan fysiskt möte'
            elif 'Operation' in line:
                data['typ'] = 'Operation'
            elif 'Ambulans' in line:
                data['typ'] = 'Ambulans'
        
        # Healthcare provider
        elif 'Antecknad av' in line:
            current_section = 'vardpersonal'
            current_content = []
        elif current_section == 'vardpersonal' and '(' in line and ')' in line:
            data['vardpersonal'] = line
            current_section = None
        
        # Care unit
        elif current_section == 'vardpersonal' and ('vårdcentral' in line.lower() or 'medicinkliniken' in line.lower() or 'region' in line.lower()):
            data['vardenhet'] = line
            current_section = None
        
        # Contact reason
        elif line == 'Kontaktorsak':
            current_section = 'kontaktorsak'
            current_content = []
        elif current_section == 'kontaktorsak' and line not in ['Anamnes', 'Status', 'Aktuellt']:
            data['kontaktorsak'] = line
            current_section = None
        
        # Anamnesis/Current
        elif line in ['Anamnes', 'Aktuellt', 'Socialt', 'Tidigare och nuvarande sjukdomar']:
            current_section = 'anamnes'
            current_content = []
        elif current_section == 'anamnes' and line not in ['Status', 'Bedömning', 'Planering']:
            current_content.append(line)
            data['anamnes_aktuellt'] = ' '.join(current_content)
        
        # Status sections
        elif line == 'Status':
            current_section = 'status'
            current_content = []
        elif line in ['Allmäntillstånd', 'Hjärta', 'Lungor', 'Buk', 'Lokalstatus', 'Psykiskt status', 'Andningsfrekvens', 'Temperatur']:
            if current_section == 'status':
                current_section = f'status_{line.lower().replace("ä", "a").replace("ö", "o")}'
                current_content = []
        elif current_section and current_section.startswith('status_'):
            if line not in ['Bedömning', 'Planering', 'Lab', 'EKG']:
                current_content.append(line)
                section_name = current_section.replace('status_', '')
                data['status'][section_name] = ' '.join(current_content)
        
        # Vitals
        elif 'Blodtryck' in line:
            current_section = 'vitals_bt'
            current_content = []
        elif 'Systoliskt' in line and current_section == 'vitals_bt':
            pass  # Skip header
        elif 'Diastoliskt' in line and current_section == 'vitals_bt':
            pass  # Skip header
        elif re.match(r'^\d+\s*mm', line) and current_section == 'vitals_bt':
            # Extract blood pressure values
            systolic = re.search(r'(\d+)', line)
            if systolic and 'systoliskt' not in data['matt']:
                data['matt']['systoliskt'] = systolic.group(1)
            elif systolic and 'diastoliskt' not in data['matt']:
                data['matt']['diastoliskt'] = systolic.group(1)
        elif 'Puls' in line and re.search(r'(\d+)', line):
            pulse_match = re.search(r'(\d+)', line)
            if pulse_match:
                data['matt']['puls'] = pulse_match.group(1) + ' /min'
        elif 'SpO2' in line and re.search(r'(\d+)', line):
            spo2_match = re.search(r'(\d+)', line)
            if spo2_match:
                data['matt']['spo2'] = spo2_match.group(1) + '%'
        elif 'Temperatur' in line and re.search(r'(\d+[,.]?\d*)', line):
            temp_match = re.search(r'(\d+[,.]?\d*)', line)
            if temp_match:
                data['matt']['temp'] = temp_match.group(1) + '°C'
        
        # Lab results
        elif line == 'Lab':
            current_section = 'lab'
            current_content = []
        elif current_section == 'lab' and '—' in line and any(char.isdigit() for char in line):
            # Parse lab result line like "P—Troponin T" followed by values
            data['lab'].append(line)
        
        # EKG/Imaging
        elif line == 'EKG' or 'EKG' in line:
            current_section = 'ekg'
            current_content = []
        elif current_section == 'ekg' and line not in ['Bedömning', 'Planering']:
            current_content.append(line)
            data['ekg_imaging'] = ' '.join(current_content)
        
        # Assessment
        elif line == 'Bedömning':
            current_section = 'bedomning'
            current_content = []
        elif current_section == 'bedomning' and line not in ['Planering', 'Diagnos/åtgärdskod']:
            current_content.append(line)
            data['bedomning'] = ' '.join(current_content)
        
        # Planning
        elif line == 'Planering':
            current_section = 'planering'
            current_content = []
        elif current_section == 'planering' and line not in ['Diagnos/åtgärdskod', 'Diagnos:']:
            current_content.append(line)
            data['planering'] = ' '.join(current_content)
        
        # Diagnoses
        elif 'Diagnos' in line or re.match(r'^[A-Z]\d+', line):  # ICD codes
            if re.search(r'[A-Z]\d+', line):  # Contains ICD code
                data['diagnoser'].append(line)
        
        # Medications - look for medication names followed by dates
        elif re.search(r'\d{4}-\d{2}-\d{2}', line) and any(word in line for word in ['mg', 'Tablett', 'Kapsel', 'Ordinerat']):
            data['lakemedel'].append(line)
    
    return data

def format_chunk(encounter: Dict[str, Any], index: int, total: int) -> str:
    """Format encounter as structured CHUNK following specifications"""
    
    # Extract structured data
    data = extract_structured_data(encounter['full_content'])
    
    # Build formatted chunk
    chunk = f"=== CHUNK {index}/{total} ===\n"
    chunk += f"Typ: {data['typ']}\n"
    chunk += f"DatumTid: {data['datum_tid'] if data['datum_tid'] else encounter['date']}\n"
    chunk += f"Vårdpersonal: {data['vardpersonal']}\n"
    chunk += f"Vårdenhet: {data['vardenhet']}\n"
    
    if data['kontaktorsak']:
        chunk += f"Kontaktorsak: {data['kontaktorsak']}\n"
    
    if data['anamnes_aktuellt']:
        chunk += f"Anamnes/Aktuellt: {data['anamnes_aktuellt']}\n"
    
    # Status sections
    if data['status']:
        chunk += "Status:\n"
        for section, content in data['status'].items():
            if content:
                chunk += f"  {section.title()}: {content}\n"
    
    # Measurements
    if data['matt']:
        matt_parts = []
        if 'systoliskt' in data['matt'] and 'diastoliskt' in data['matt']:
            matt_parts.append(f"BT={data['matt']['systoliskt']}/{data['matt']['diastoliskt']} mmHg")
        if 'puls' in data['matt']:
            matt_parts.append(f"Puls={data['matt']['puls']}")
        if 'spo2' in data['matt']:
            matt_parts.append(f"SpO2={data['matt']['spo2']}")
        if 'temp' in data['matt']:
            matt_parts.append(f"Temp={data['matt']['temp']}")
        
        if matt_parts:
            chunk += f"Mått: {', '.join(matt_parts)}\n"
    
    # Lab results
    if data['lab']:
        chunk += "Lab:\n"
        chunk += "  Analys | Värde | Enhet | Ref | Markering\n"
        for lab_line in data['lab']:
            chunk += f"  {lab_line}\n"
    
    if data['operation']:
        chunk += f"Operation/Åtgärd: {data['operation']}\n"
    
    if data['ekg_imaging']:
        chunk += f"EKG/Imaging: {data['ekg_imaging']}\n"
    
    if data['bedomning']:
        chunk += f"Bedömning: {data['bedomning']}\n"
    
    if data['planering']:
        chunk += f"Planering/Åtgärd: {data['planering']}\n"
    
    if data['diagnoser']:
        chunk += "Diagnoser/ICD:\n"
        for diagnosis in data['diagnoser']:
            chunk += f"  - {diagnosis}\n"
    
    if data['lakemedel']:
        chunk += "Läkemedel:\n"
        for medication in data['lakemedel']:
            chunk += f"  - {medication}\n"
    
    # Add raw content as citat for important information preservation
    important_quotes = []
    content_lines = encounter['full_content'].split('\n')
    for line in content_lines:
        if any(keyword in line.lower() for keyword in ['akut', 'svår', 'kraftig', 'smärta', 'blödning']):
            if len(line.strip()) > 10:  # Avoid short meaningless lines
                date_match = re.search(r'(\d{4}-\d{2}-\d{2})', encounter['full_content'])
                date_str = date_match.group(1) if date_match else encounter['date']
                important_quotes.append(f'[{date_str}: "{line.strip()}"]')
    
    if important_quotes:
        chunk += "Citat:\n"
        for quote in important_quotes[:3]:  # Limit to 3 most important quotes
            chunk += f"  {quote}\n"
    
    chunk += f"=== END CHUNK {index}/{total} ===\n\n"
    
    return chunk

def create_csv_summary(encounters: List[Dict[str, Any]]) -> str:
    """Create CSV summary table as specified"""
    csv_content = "Date,Type,Unit,Key_Finding,Vitals,Key_Labs,Diagnoses,Med_Changes,Note\n"
    
    for encounter in encounters:
        date = encounter['date']
        enc_type = encounter['type']
        
        # Extract key info
        content = encounter['full_content']
        
        # Unit
        unit = ""
        if 'Vårdcentralen' in content:
            unit = "VC"
        elif 'Medicinkliniken' in content:
            unit = "Medicin"
        elif 'Akutmottagningen' in content:
            unit = "Akuten"
        
        # Key findings
        key_finding = ""
        if 'hypertoni' in content.lower():
            key_finding = "Hypertoni"
        elif 'ångest' in content.lower():
            key_finding = "Ångest"
        elif 'depression' in content.lower():
            key_finding = "Depression"
        elif 'smärta' in content.lower():
            key_finding = "Smärta"
        
        # Vitals
        vitals = ""
        bt_match = re.search(r'(\d+)/(\d+)', content)
        if bt_match:
            vitals = f"BP={bt_match.group(1)}/{bt_match.group(2)}"
        
        # Labs
        labs = ""
        if '*' in content:  # Abnormal values marked with *
            labs = "Abnormal values"
        elif 'troponin' in content.lower():
            labs = "Troponin checked"
        
        # Diagnoses
        diagnoses = ""
        icd_match = re.search(r'([A-Z]\d+)', content)
        if icd_match:
            diagnoses = icd_match.group(1)
        
        # Medication changes
        med_changes = ""
        if 'insatt' in content.lower():
            med_changes = "New medication"
        elif 'utsatt' in content.lower():
            med_changes = "Discontinued"
        elif 'ökat' in content.lower():
            med_changes = "Increased dose"
        
        # Note
        note = ""
        if 'akut' in content.lower():
            note = "Acute"
        elif 'uppföljning' in content.lower():
            note = "Follow-up"
        elif 'kontroll' in content.lower():
            note = "Routine"
        
        csv_content += f"{date},{enc_type},{unit},{key_finding},{vitals},{labs},{diagnoses},{med_changes},{note}\n"
    
    return csv_content

def main():
    """Main processing function"""
    print("Creating complete cleaned chunks from 79 main medical encounters...")
    
    # Load encounters
    encounters = load_main_encounters()
    print(f"Loaded {len(encounters)} main encounters")
    
    # Process each encounter
    all_chunks = []
    total_encounters = len(encounters)
    
    for i, encounter in enumerate(encounters):
        print(f"Processing encounter {i+1}/{total_encounters}: {encounter['date']}")
        chunk = format_chunk(encounter, i+1, total_encounters)
        all_chunks.append(chunk)
    
    # Combine all chunks
    complete_content = ""
    for chunk in all_chunks:
        complete_content += chunk
    
    # Add CSV summary
    csv_summary = create_csv_summary(encounters)
    complete_content += "\n\n=== CSV ÖVERSIKTSTABELL ===\n"
    complete_content += "```csv\n"
    complete_content += csv_summary
    complete_content += "```\n"
    
    # Add completion message
    complete_content += f"\n**CLEAN COMPLETE - {total_encounters} chunks processed**\n"
    
    # Save to file
    with open('complete_cleaned_chunks.md', 'w', encoding='utf-8') as f:
        f.write(complete_content)
    
    print(f"\nSaved complete cleaned chunks to complete_cleaned_chunks.md")
    print(f"Total chunks processed: {total_encounters}")
    print(f"Total content size: {len(complete_content)} characters")

if __name__ == "__main__":
    main()