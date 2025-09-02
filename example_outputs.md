# Example Outputs - 1177 Journal Processing
## Real Examples from 20-Year Dataset (2005-2025)

---

## PART 1: RAW INPUT EXAMPLE
```
Gå direkt till huvudinnehåll
Gå direkt till sök i din journal
[1177/Inera]
Sara El-Zarka

Inställningar
Logga ut

Start
Inkorg
Bokade tider
Journalen
Egen provhantering
Stöd och behandling
Intyg
Övriga tjänster
Du är här:
Start
Journalen
Journalöversikt
Journalen
Journalöversikt
Här finns alla tillgängliga uppgifter ur din journal, i tidsordning med de nyaste överst.

1240 uppgifter hittades
informationstyp
informationstyp

Anteckningar

Diagnoser

Läkemedel

Provsvar

Remisser

Uppmärksamhetsinformation

Vårdkontakter
Datum från
ÅÅÅÅ-MM-DD
Datum till
ÅÅÅÅ-MM-DD
vårdpersonal
vårdpersonal

**Anders HB Pettersson

**Anita Wikander Säldebjer

[... 200+ more staff names ...]

2025-08-31 13:54
Beställt av
Kaneberg, Sofia (ST-läkare)
Akutmottagningen medicin Växjö
Provsvar
Analys
Referensintervall
Resultat och kommentarer

* markerar resultat utanför referens­intervallet
  P—Troponin T
  Referensintervall: <15
  4 ng/L
  Graf
  Vidimerat: Kaneberg, Sofia (ST-läkare) 2025-08-31
  
[... continues with more entries ...]
```

---

## PART 2: CLEANED CHUNKS OUTPUT

```
=== CHUNK 1/79 ===
Typ: Operation
DatumTid: 2005-06-30 09:19
Vårdpersonal: [Ej angivet]
Vårdenhet: Gastroenterologi
Kontaktorsak: Smärtor i övre delen av buken
Anamnes/Aktuellt: Patient med buksmärtor, remitterad för gastroskopi
Status:
  Esofagus: Normalt
  Cardia: Normalt
  Magsäck: Normalt
  Duodenum: Normalt
  Tunntarm: Normalt
Mått: [Ej angivet]
Lab: [Inga lab detta besök]
Operation/Åtgärd: UJD02 Gastroskopi
EKG/Imaging: [Ej relevant]
Bedömning: Normal skopi. Kopia av utlåtande som remissvar.
Planering/Åtgärd: Uppföljning via remitterande
Diagnoser/ICD: R101 - Smärtor i övre delen av buken
Läkemedel: [Inga ändringar]
Citat: ["2005-06-30: normal skopi"]
=== END CHUNK 1/79 ===

=== CHUNK 45/79 ===
Typ: Provsvar
DatumTid: 2015-12-14 14:52
Vårdpersonal: Mencser, Krisztina (distriktsläkare)
Vårdenhet: Vårdcentralen Åseda
Kontaktorsak: Rutinkontroll
Anamnes/Aktuellt: Provtagning för uppföljning
Status: [Ej angivet]
Mått: [Ej angivet]
Lab:
  Analys | Värde | Enhet | Ref | Markering
  P—Kalium | 4.6 | mmol/L | 3.5-4.4 | *
  P—Natrium | 142 | mmol/L | 137-145 |
  Pt—eGFR(Krea)relativ | 88 | mL/min/1,73m2 | 60-110 |
  P—Calcium | 2.44 | mmol/L | 2.15-2.50 |
  P—Albumin | 47 | g/L | 36-45 | *
  P—Kreatinin | 61 | µmol/L | 45-90 |
Operation/Åtgärd: [Ej relevant]
EKG/Imaging: [Ej angivet]
Bedömning: Lätt förhöjt kalium och albumin
Planering/Åtgärd: Kontroll om 3 månader
Diagnoser/ICD: [Inga nya]
Läkemedel: [Inga ändringar]
Citat: ["2015-12-14: K 4.6*, Albumin 47*"]
=== END CHUNK 45/79 ===

=== CHUNK 78/79 ===
Typ: Besöksanteckning
DatumTid: 2025-08-31 06:13
Vårdpersonal: Liselotte Gunnarsson (Sjuksköterska)
Vårdenhet: Akutmottagningen Växjö
Kontaktorsak: Hypertoni. Bröstsmärta.
Anamnes/Aktuellt: Patient med känd hypertoni, medicineras via vårdcentral. Vaknat av att hon inte mådde bra, kollat blodtryck som låg väldigt högt (253/133). Kontaktar ambulans. Beskriver att hon "försvinner bort", oklart om synkope. Initialt ångestdriven och orolig, lugnar sig varvid blodtrycket går ner.
Status:
  Allmäntillstånd: Ångestpåverkad initialt, stabiliseras
  Aktivitet: Uppegående utan hjälpmedel
Mått: BT=253/133 mmHg (hemma), senare normaliserat på akuten
Lab:
  Analys | Värde | Enhet | Ref | Markering
  P—Troponin T | 4 | ng/L | <15 |
Operation/Åtgärd: Perifer venkateter inlagd
EKG/Imaging: EKG - Normal
Bedömning: Bröstsmärta. Normalt EKG och Troponin normalt. Ingen misstanke om bakomliggande akut koronart syndrom.
Planering/Åtgärd: Blodtrycksjustering, uppföljning vårdcentral
Diagnoser/ICD: I10 - Essentiell hypertoni
Läkemedel:
  - Candesartan 8 mg, fortsatt
  - Överväg Amlodipin insättning
Citat: ["2025-08-31: BT 253/133, försvinner bort"]
=== END CHUNK 78/79 ===

=== CHUNK 79/79 ===
Typ: Anteckning utan fysiskt möte
DatumTid: 2025-09-01 10:17
Vårdpersonal: [Läkare, namn ej angivet]
Vårdenhet: Vårdcentralen
Kontaktorsak: Uppföljning efter akutbesök
Anamnes/Aktuellt: Tagit Candesartan 4 mg 2x1 på morgonen enligt rekommendation från akuten, ändå haft blodtryck upp mot 200/130 uppmätt hemma. På eget bevåg tagit enalapril samt amlodipin 5 mg. Upplever att blodtrycket går ner. Tror själv att Duloxetin är orsak till högt blodtryck (tog 1 tabl fredag, 1 tabl lördag, sedan högt tryck).
Status:
  Allmäntillstånd: På kliniken opåverkad, blodtryck under kontroll
Mått: BT=Under kontroll (exakt värde ej angivet)
Lab: [Inga nya]
Operation/Åtgärd: [Ej relevant]
EKG/Imaging: [Ej angivet]
Bedömning: Duloxetin kan enligt FASS ge hypertoni som biverkning, kan ej utesluta detta som orsak trots endast 2 dagars behandling
Planering/Åtgärd: 
  - Utsätter Duloxetin
  - Insätter Fluoxetin (viktneutralt, ej hypertoni som biverkning)
  - Insätter Amlodipin 5 mg
  - Fortsätter Candesartan 8 mg
  - Mäter blodtryck hemma fredag, ringer in värde
Diagnoser/ICD: 
  - I10 - Essentiell hypertoni
  - F32.9 - Blandade ångest- och depressionstillstånd
Läkemedel:
  - STOP: Duloxetin (misstänkt orsak till BT-stegring)
  - START: Fluoxetin
  - START: Amlodipin 5 mg
  - FORTSÄTT: Candesartan 8 mg
Citat: ["2025-09-01: Duloxetin → BT 200/130 inom 48h"]
=== END CHUNK 79/79 ===

CSV SUMMARY:
Date,Type,Unit,Key_Finding,Vitals,Key_Labs,Diagnoses,Med_Changes,Note
2005-06-30,Operation,Gastro,Normal gastroscopy,-,-,R101,-,Baseline exam
2007-06-16,Besök,VC,Check-up,-,-,-,-,Routine
2010-10-31,Provsvar,Psyk,Labs not taken,-,Not done,-,-,Psych follow-up
2015-12-14,Provsvar,VC Åseda,Elevated K/Alb,-,K=4.6* Alb=47*,-,-,Mild abnormalities
2020-03-15,Besök,VC,Depression review,-,-,F32.9,+Mirtazapin,Depression treatment
2024-08-27,Besök,VC,Med adjustment,-,-,F32.9,-Mirtazapin +Duloxetin,Weight gain issue
2025-08-31,Besök,Akuten,HTN crisis,BP=253/133,TnT=4,I10,Consider Amlodipin,Acute HTN
2025-09-01,Telefon,VC,Duloxetin stopped,BP controlled,-,I10/F32.9,-Duloxetin +Fluoxetin +Amlodipin,Med side effect

**CLEAN COMPLETE - 79 chunks processed**
```

---

## PART 3: DIAGNOSTIC ANALYSIS OUTPUT

### KLINISK SAMMANFATTNING

**20-års journalöversikt (2005-2025)**

**Tidslinje-tabell:**
| Period | Huvudfynd | Utveckling |
|--------|-----------|------------|
| 2005-2010 | GI-symtom, normal gastroskopi | Initiala mag-tarmbesvär, utredning ua |
| 2010-2015 | Psykiatrisk kontakt påbörjad | Depression/ångest etableras som diagnos |
| 2015-2020 | Stabil period, lätt lab-avvikelser | K+ och albumin förhöjt, njurfunktion OK |
| 2020-2024 | Antidepressiv behandling intensifieras | Mirtazapin → viktuppgång problem |
| 2024-2025 | Hypertoni utvecklas, medicineringsproblem | Duloxetin → akut BT-stegring 253/133 |

**Mönsteranalys:**
- Långvarig psykiatrisk problematik (15+ år)
- Nyutvecklad/förvärrad hypertoni senaste året
- Tydlig korrelation Duloxetin → BT-stegring inom 48h
- Viktproblematik sekundärt till Mirtazapin

**Lab-trender (20 år):**
```
Parameter | 2015 | 2020 | 2025 | Trend | Betydelse
eGFR | 88 | - | - | → | Stabil njurfunktion
K+ | 4.6* | - | - | ↑ | Mild hyperkalemi
Albumin | 47* | - | - | ↑ | Ospecifik förhöjning
Troponin | - | - | 4 | → | Normal, utesluter ACS
```

### DIFFERENTIAL DIAGNOS

| Diagnos | Sannolikhet | För | Mot | Bekräfta med |
|---------|-------------|-----|-----|--------------|
| Läkemedelsutlöst hypertoni (Duloxetin) | 85% | Tidssamband 48h, FASS-biverkan, BT 253/133 direkt efter insättning | Kort exponering (2 doser) | Utsättning → normalisering |
| Essentiell hypertoni med akut exacerbation | 60% | Känd HTN, stress/ångest trigger | Extremt högt BT för essentiell | 24h-BT efter stabilisering |
| Whitecoat + ångest-HTN | 40% | Känd ångest, "försvinner bort", lugnar sig → BT ner | BT 253/133 hemma också | Hemblodtryck vs klinik |
| Sekundär hypertoni | 20% | Snabb försämring, läkemedelsresistens | Känd essentiell HTN | Endokrin screening |
| Autonom dysfunktion | 15% | "Försvinner bort" episoder, BT-variabilitet | Ej synkope beskrivet | Tilt-test |

### WORKING DIAGNOSIS
**Primär: Läkemedelsutlöst hypertensiv kris sekundärt till Duloxetin**
- Confidence: 85%
- Motivering: Tydligt tidssamband (48h), känd biverkan, resolving efter utsättning
- Underliggande: Essentiell hypertoni + F32.9 Ångest/depression

### RED FLAGS & HANDLINGSPLAN

**AKUT (inom 24h):**
- BT >180/110 → akut vård
- Bröstsmärta/dyspné → akut vård
- "Försvinner bort" episoder → neurologkontakt

**DIAGNOSTIK (prioritet):**
1. 24h-BT om 1 vecka (efter Duloxetin-utsättning)
2. TSH, fT4 (aldrig testat på 20 år?)
3. Aldosteron/renin om BT kvarstår högt
4. Urin-metanefriner om episodiska attacker

**BEHANDLING:**
- Amlodipin 5 mg 1x1 ✓ (insatt)
- Candesartan 8 mg 1x1 ✓ (fortsatt)
- Fluoxetin 20 mg ✓ (ersätter Duloxetin)
- Målblodtryck: <140/90

**UPPFÖLJNING:**
- Hemblodtryck 2x/dag i 1 vecka
- VC-kontroll om 2 veckor
- Psykiatri om 1 månad för depression

### PATIENTVÄNLIG SAMMANFATTNING

Din journal från 2005 visar en lång historia med mag-tarmutredning (som var normal) och senare utveckling av depression/ångest som behandlats i många år. 

Det senaste året har du utvecklat högt blodtryck som blev akut värre när du startade medicinen Duloxetin för bara några dagar sedan. Ditt blodtryck gick upp till farligt höga nivåer (253/133) vilket ledde till akutbesök.

Planen nu är att du slutat med Duloxetin (som troligen orsakade blodtrycksökningen) och börjat med Fluoxetin istället för din depression. För blodtrycket har du fått Amlodipin tillagt till din Candesartan. Mät blodtrycket hemma och kontakta vårdcentralen om det går över 180/110 eller om du får bröstsmärtor.

### JSON EXPORT
```json
{
  "analysis_date": "2025-09-02",
  "data_span": "2005-2025",
  "total_entries": 79,
  "working_diagnosis": {
    "primary": "Läkemedelsutlöst hypertensiv kris (Duloxetin)",
    "confidence_percent": 85,
    "icd_codes": ["I10", "F32.9", "Y57.0"]
  },
  "differential": [
    {"diagnosis": "Läkemedelsutlöst HTN", "probability": 85, "urgency": "high"},
    {"diagnosis": "Essentiell HTN exacerbation", "probability": 60, "urgency": "medium"},
    {"diagnosis": "Whitecoat + ångest-HTN", "probability": 40, "urgency": "low"}
  ],
  "red_flags": {
    "urgent": ["BT >180/110", "Bröstsmärta", "Synkope"],
    "soon": ["BT 160-180/100-110", "Huvudvärk"],
    "routine": ["Viktuppgång", "Depression försämring"]
  },
  "labs_of_concern": [
    {"test": "K+", "value": "4.6", "trend": "↑", "action_needed": "Kontroll med ACE-i"},
    {"test": "eGFR", "value": "88", "trend": "→", "action_needed": "Årlig kontroll"},
    {"test": "TSH", "value": "Never done", "trend": "-", "action_needed": "Baseline needed"}
  ],
  "medications": {
    "current": ["Candesartan 8mg", "Amlodipin 5mg", "Fluoxetin 20mg"],
    "stopped": ["Duloxetin", "Mirtazapin"],
    "contraindicated": ["Duloxetin", "SNRI-preparat"],
    "recommended": ["Continue current regimen"]
  },
  "next_steps": {
    "urgent": ["Hemblodtryck 2x dagligen", "Akut om BT >180/110"],
    "diagnostic": ["24h-BT om 1v", "TSH/fT4", "Consider aldosteron/renin"],
    "therapeutic": ["Titrera Amlodipin vid behov", "Fluoxetin upptitrering"],
    "monitoring": ["VC 2v", "Psyk 1 mån", "Vikt månadsvis"]
  },
  "missing_critical_info": [
    "Thyroid function (never tested)",
    "Lipid panel last 5 years",
    "HbA1c screening",
    "ECG during symptoms",
    "Family history CVD"
  ],
  "data_gaps": {
    "years": ["2011-2014 sparse", "2021-2022 limited"],
    "tests_never_done": ["TSH", "Cortisol", "Metanephrines", "Sleep study"]
  }
}
```

---

## SÄKERHETSPÅMINNELSE
*Denna analys baseras på journaldata och är endast för informationssyfte. Den ersätter inte medicinsk bedömning. Vid akuta symtom - sök vård omedelbart. Diskutera alltid resultat och planering med din läkare.*