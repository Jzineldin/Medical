# 1177 Journal Analysis Workflow Guide
## Complete System for 20-Year Medical History Processing

### Overview
This workflow processes Swedish 1177 healthcare journal exports (2005-2025) through two AI prompts:
1. **CLEANER**: Removes navigation/lists, normalizes format → structured CHUNKs
2. **DIAGNOSTIC WORKUP**: Analyzes patterns → differential diagnosis + actionable plan

### File Sizes & Performance
- **Typical export**: 500KB-1MB (70-100 entries over 20 years)
- **Processing time**: 2-5 minutes for cleaning, 3-5 minutes for analysis
- **Token usage**: ~15-20K for cleaning, ~20-30K for analysis

---

## STEP 1: Export Your Journal from 1177

1. Log into 1177.se
2. Navigate to "Journalen" → "Journalöversikt"
3. Select date range (leave empty for all records)
4. Click "Visa alla uppgifter"
5. Select all text (Ctrl+A) and copy
6. Save to `medical_raw.txt`

---

## STEP 2: Optional Pre-Cleaning (Recommended for files >500KB)

### Option A: Quick PowerShell Clean (Windows)
```powershell
# Remove navigation and staff lists
$content = Get-Content medical_raw.txt -Raw
$content = $content -replace '(?m)^(Gå direkt till.*|Du är här:.*|\*\*.*|vårdpersonal)$\n?', ''
$content | Set-Content medical_precleaned.txt
```

### Option B: Manual Regex Clean
1. Open `medical_raw.txt` in VS Code
2. Press Ctrl+H for Find/Replace
3. Enable regex mode (.*icon)
4. Use patterns from `regex_helpers.txt`
5. Save as `medical_precleaned.txt`

### Option C: Quick Manual Clean
1. Delete everything before first date (20XX-XX-XX)
2. Delete obvious staff lists (lines starting with **)
3. Save as `medical_precleaned.txt`

**Result**: File reduced by 30-50% without losing medical data

---

## STEP 3: Run CLEANER Prompt

### For Standard Dataset (≤50 entries)
1. Open AI interface (Claude, GPT-4, etc.)
2. Copy entire content from `1177_cleaner_prompt.txt`
3. Paste into AI
4. Add your journal text after the prompt
5. Wait for "CLEAN COMPLETE - X chunks processed"

### For Large Dataset (50-100 entries)
Split by decade for better processing:

```
# First message:
[CLEANER PROMPT]
[Entries from 2005-2010]

# Second message:
CONTINUE CLEANING - Starting from chunk 16/79
[Entries from 2011-2015]

# Third message:
CONTINUE CLEANING - Starting from chunk 31/79
[Entries from 2016-2020]

# Fourth message:
CONTINUE CLEANING - Starting from chunk 55/79
[Entries from 2021-2025]

# Fifth message:
FINALIZE - Create CSV summary for all 79 chunks
```

### For Very Large Dataset (>100 entries)
Process by year or specific periods of interest:

```
# Focus on recent issues:
[CLEANER PROMPT]
FOCUS PERIOD: 2023-2025 only
[Recent entries]

# Historical context:
[CLEANER PROMPT]
FOCUS PERIOD: Major events only (operations, diagnoses, medication changes)
[Full dataset]
```

### Saving Cleaned Output
Copy all CHUNKs to `medical_cleaned.txt`

---

## STEP 4: Run Diagnostic Analysis

1. Open new AI conversation (or continue if context allows)
2. Copy entire content from `diagnostic_workup_prompt.txt`
3. Paste into AI
4. Add your cleaned CHUNKs
5. Type: `ALL CHUNKS READY`
6. Wait for comprehensive analysis

### Output Components
- **Clinical Summary**: Professional medical analysis
- **Timeline Table**: 20-year overview
- **Differential Diagnosis**: Ranked possibilities with %
- **Working Diagnosis**: Most likely diagnosis with confidence
- **Action Plan**: Urgent/diagnostic/therapeutic steps
- **Patient-Friendly Summary**: Simple Swedish explanation
- **JSON Export**: Structured data for programs

### Save Results
- Copy clinical summary to `medical_analysis.md`
- Copy JSON to `medical_data.json`
- Copy patient summary to `patient_summary.txt`

---

## STEP 5: Selective Analysis Options

### A. Period-Specific Analysis
```
Run diagnostic on CHUNKS 70-79 only (last 2 years)
Focus on hypertension development
```

### B. System-Specific Analysis
```
Analyze only cardiovascular-related entries
Include: BP measurements, cardiac symptoms, related medications
```

### C. Medication Timeline
```
Create medication-only timeline
Show all starts, stops, changes, side effects
```

### D. Lab Trend Analysis
```
Extract all lab values across 20 years
Create trend graphs for: eGFR, electrolytes, inflammatory markers
```

---

## Performance Optimization Tips

### 1. Token Management
- **Problem**: AI hitting token limits
- **Solution**: Process in chunks, focus on specific years/systems

### 2. Format Inconsistencies
- **Problem**: Different formats across 20 years
- **Solution**: Run era-specific cleaning (2005-2010, 2011-2020, 2021-2025)

### 3. Missing Data Periods
- **Problem**: Gaps in records (e.g., 2011-2014)
- **Solution**: Note in analysis, don't interpolate

### 4. Duplicate Entries
- **Problem**: Same visit appears multiple times
- **Solution**: CLEANER merges same-date entries automatically

### 5. Language Mix
- **Problem**: Some English terms mixed with Swedish
- **Solution**: CLEANER preserves original language

---

## Advanced Features

### Custom Filtering
Add to CLEANER prompt:
```
FILTER: Only include entries with:
- Diagnoses (ICD codes)
- Abnormal lab values
- Medication changes
- Emergency visits
```

### Urgency Ranking
Add to DIAGNOSTIC prompt:
```
PRIORITIZE: Rank all findings by clinical urgency
1. Life-threatening (immediate action)
2. Urgent (within 24-48h)
3. Soon (within week)
4. Routine (scheduled follow-up)
```

### Correlation Analysis
Add to DIAGNOSTIC prompt:
```
CORRELATE: Find temporal relationships between:
- Medication starts → symptom changes
- Lab changes → clinical events
- Seasonal patterns → exacerbations
```

---

## Troubleshooting

### Issue: "File too large" error
**Fix**: Pre-clean with regex, split by date ranges

### Issue: Cleaned chunks missing information
**Fix**: Check original has complete entries, adjust CLEANER settings

### Issue: Analysis too generic
**Fix**: Provide more specific instructions in DIAGNOSTIC prompt

### Issue: Wrong language in output
**Fix**: Add "ALWAYS respond in Swedish" to prompts

### Issue: Dates out of order
**Fix**: CLEANER sorts chronologically - check source data

---

## Quality Checklist

Before cleaning:
- [ ] File backed up
- [ ] Date range verified (2005-2025)
- [ ] Pre-cleaning done if >500KB

After cleaning:
- [ ] All 79 entries accounted for
- [ ] Dates preserved correctly
- [ ] Lab values with units
- [ ] Medications with doses
- [ ] No navigation text remains

After analysis:
- [ ] Working diagnosis makes sense
- [ ] Timeline is complete
- [ ] Red flags identified
- [ ] Action plan is specific
- [ ] Patient summary is clear

---

## Security & Privacy

⚠️ **IMPORTANT**: 
- These are sensitive medical records
- Use secure, private AI services only
- Don't share outputs publicly
- Store files encrypted
- Delete temporary files after use

---

## Example Commands for Specific Queries

### "What medications have I tried for depression?"
```
Analyze CHUNKS for all antidepressant medications
Include: start dates, stop dates, reasons for change, effects
```

### "Show my blood pressure trend"
```
Extract all BP measurements from CHUNKS
Create timeline graph with medications overlay
```

### "Have my kidney values changed?"
```
Track eGFR, creatinine across all years
Flag concerning trends
```

### "What triggered my ER visits?"
```
Filter CHUNKS for emergency/acute visits only
Identify patterns and triggers
```

---

## Next Steps After Analysis

1. **Print analysis** for next doctor visit
2. **Highlight concerns** from red flags section
3. **Prepare questions** based on gaps identified
4. **Track parameters** mentioned in monitoring plan
5. **Update regularly** - re-run quarterly or after major events

---

## Support Resources

- **1177 Vårdguiden**: 1177.se
- **Patient privacy**: datainspektionen.se
- **Medical questions**: Always consult your healthcare provider
- **Technical issues**: Check regex_helpers.txt for patterns

---

*Version 1.0 - Covers 1177 exports 2005-2025*
*For use with Swedish healthcare journal data only*
*This tool provides information, not medical advice*