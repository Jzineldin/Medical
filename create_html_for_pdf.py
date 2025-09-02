#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skript för att skapa HTML från markdown som kan öppnas och skrivas ut som PDF
"""

import os
import re

# Mapp med dokumenten
docs_dir = r"C:\Users\Jzine\Desktop\Medical\SLUTGILTIG_DOKUMENTATION_2025"
output_dir = r"C:\Users\Jzine\Desktop\Medical"

# Filer i rätt ordning
files_in_order = [
    "00_START_HÄR_ÖVERSIKT.md",
    "01_ALLA_KONTAKTER_KOMPLETT.md",
    "02_VAD_DU_SOM_BARN_SKA_GÖRA.md",
    "03_PATIENTSAMMANFATTNING_ENKELT.md",
    "04_ÅTGÄRDSPLAN_FÖR_PATIENT.md",
    "05_LÄKEMEDELSRISKER.md",
    "06_TILL_LÄKAREN_KRITISKA_TESTER.md",
    "07_MEDICINSK_VERIFIERING.md",
    "08_VÅRDSKADOR_FÖR_IVO.md",
    "09_DISKRIMINERING_FÖR_DO.md",
    "10_KOMPLETT_VERIFIERING.md",
    "11_ANVÄNDNINGSGUIDE_FÖR_ALLA_DOKUMENT.md"
]

def markdown_to_html(text):
    """Enkel markdown till HTML konvertering"""
    # Headers
    text = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', text, flags=re.MULTILINE)
    
    # Bold
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    
    # Lists
    text = re.sub(r'^- (.*?)$', r'<li>\1</li>', text, flags=re.MULTILINE)
    text = re.sub(r'^\d+\. (.*?)$', r'<li>\1</li>', text, flags=re.MULTILINE)
    
    # Line breaks
    text = re.sub(r'^---$', r'<hr>', text, flags=re.MULTILINE)
    
    # Paragraphs
    paragraphs = text.split('\n\n')
    html_paragraphs = []
    for p in paragraphs:
        if not p.strip():
            continue
        if p.strip().startswith('<'):
            html_paragraphs.append(p)
        else:
            html_paragraphs.append(f'<p>{p}</p>')
    
    return '\n'.join(html_paragraphs)

# HTML template
html_template = """<!DOCTYPE html>
<html lang="sv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Komplett Medicinsk Dokumentation 2025</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: white;
        }
        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            page-break-before: always;
        }
        h2 {
            color: #34495e;
            margin-top: 30px;
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 5px;
        }
        h3 {
            color: #555;
            margin-top: 20px;
        }
        strong {
            color: #e74c3c;
        }
        hr {
            border: none;
            border-top: 2px solid #ecf0f1;
            margin: 30px 0;
        }
        ul, ol {
            margin-left: 20px;
        }
        li {
            margin: 5px 0;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #3498db;
            color: white;
        }
        .warning {
            background-color: #fff3cd;
            border-left: 5px solid #ffc107;
            padding: 10px;
            margin: 20px 0;
        }
        .critical {
            background-color: #f8d7da;
            border-left: 5px solid #dc3545;
            padding: 10px;
            margin: 20px 0;
        }
        .page-break {
            page-break-after: always;
        }
        @media print {
            body {
                font-size: 11pt;
            }
            h1 {
                page-break-before: always;
            }
            .no-print {
                display: none;
            }
        }
    </style>
</head>
<body>
    <div style="text-align: center; padding: 50px 0;">
        <h1 style="border: none; font-size: 36px;">KOMPLETT MEDICINSK DOKUMENTATION</h1>
        <h2 style="border: none; font-size: 24px;">För rättvisa och rätt vård</h2>
        <p><strong>Patient:</strong> Kvinna född 1962-04-08 (63 år)</p>
        <p><strong>Period:</strong> 2006-2025 (660 journalanteckningar)</p>
        <p><strong>Sammanställt:</strong> 2025-09-02</p>
        <p><strong>Status:</strong> KRITISK - Flera allvarliga vårdfel identifierade</p>
    </div>
    
    <div class="page-break"></div>
    
    <h1>Innehållsförteckning</h1>
    <ol>
        {toc}
    </ol>
    
    <div class="page-break"></div>
    
    {content}
    
    <div class="no-print" style="margin-top: 50px; padding: 20px; background: #f0f0f0; text-align: center;">
        <h2>Instruktioner för att skapa PDF</h2>
        <ol style="text-align: left; display: inline-block;">
            <li>Tryck Ctrl+P (eller Cmd+P på Mac)</li>
            <li>Välj "Skriv ut som PDF" eller "Microsoft Print to PDF"</li>
            <li>Välj "Spara som PDF"</li>
            <li>Spara filen som "KOMPLETT_DOKUMENTATION_2025.pdf"</li>
        </ol>
    </div>
</body>
</html>
"""

# Skapa innehåll
toc_items = []
content_items = []

for i, filename in enumerate(files_in_order):
    filepath = os.path.join(docs_dir, filename)
    if os.path.exists(filepath):
        print(f"Bearbetar: {filename}")
        
        # Skapa titel för innehållsförteckning
        title = filename.replace(".md", "").replace("_", " ")
        if title[:2].isdigit():
            title = title[3:]
        toc_items.append(f'<li><a href="#doc{i}">{title}</a></li>')
        
        # Läs och konvertera innehåll
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Lägg till ankare och sidbrytning
        content_items.append(f'<div id="doc{i}" class="page-break">')
        content_items.append(markdown_to_html(content))
        content_items.append('</div>')

# Sätt ihop HTML - ersätt placeholders manuellt för att undvika CSS-problem
final_html = html_template.replace('{toc}', '\n'.join(toc_items))
final_html = final_html.replace('{content}', '\n'.join(content_items))

# Spara HTML
html_path = os.path.join(output_dir, "KOMPLETT_DOKUMENTATION_2025.html")
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(final_html)

print(f"\nHTML-fil skapad: {html_path}")
print("\n" + "="*60)
print("INSTRUKTIONER FÖR ATT SKAPA PDF:")
print("="*60)
print("1. Öppna filen KOMPLETT_DOKUMENTATION_2025.html i webbläsaren")
print("2. Tryck Ctrl+P (eller högerklicka och välj 'Skriv ut')")
print("3. Välj 'Spara som PDF' eller 'Microsoft Print to PDF'")
print("4. Spara som KOMPLETT_DOKUMENTATION_2025.pdf")
print("="*60)