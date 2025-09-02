#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skript för att skapa en sammanslagen PDF från alla markdown-dokument
"""

import os
import glob
from pathlib import Path

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

# Skapa sammanslagen markdown
combined_content = []
combined_content.append("# KOMPLETT MEDICINSK DOKUMENTATION")
combined_content.append("## För rättvisa och rätt vård")
combined_content.append("**Skapad:** 2025-09-02")
combined_content.append("**Patient:** Kvinna född 1962-04-08 (63 år)")
combined_content.append("**Omfattning:** 660 journalanteckningar 2006-2025")
combined_content.append("\n---\n")
combined_content.append("# INNEHÅLLSFÖRTECKNING\n")

# Lägg till innehållsförteckning
for i, filename in enumerate(files_in_order):
    title = filename.replace(".md", "").replace("_", " ")
    # Ta bort nummer i början
    if title[:2].isdigit():
        title = title[3:]
    combined_content.append(f"{i+1}. {title}")

combined_content.append("\n\\newpage\n")

# Läs och lägg till varje fil
for filename in files_in_order:
    filepath = os.path.join(docs_dir, filename)
    if os.path.exists(filepath):
        print(f"Lägger till: {filename}")
        
        # Lägg till sidbrytning före varje nytt dokument
        combined_content.append("\n\\newpage\n")
        combined_content.append(f"---\n")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            combined_content.append(content)
    else:
        print(f"Varning: Kunde inte hitta {filename}")

# Spara sammanslagen markdown
combined_md_path = os.path.join(output_dir, "KOMPLETT_DOKUMENTATION_2025.md")
with open(combined_md_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(combined_content))

print(f"\nSammanslagen markdown skapad: {combined_md_path}")
print(f"Storlek: {len(''.join(combined_content))} tecken")
print("\nFör att konvertera till PDF, använd något av följande:")
print("1. Öppna markdown-filen i VS Code och använd 'Markdown PDF' extension")
print("2. Använd pandoc: pandoc KOMPLETT_DOKUMENTATION_2025.md -o KOMPLETT_DOKUMENTATION_2025.pdf")
print("3. Använd online-konverterare som markdown-pdf.com")
print("4. Öppna i Word och spara som PDF")