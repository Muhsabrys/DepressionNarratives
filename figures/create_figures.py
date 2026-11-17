#!/usr/bin/env python3
"""Regenerate aggregate thesis figures as self-contained SVGs (Python stdlib only)."""
from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent
with (ROOT / "results/thesis-summary.csv").open(newline="", encoding="utf-8") as f:
    ROWS = list(csv.DictReader(f))

def value(measure, group):
    return int(next(r["value"] for r in ROWS if r["measure"] == measure and r["group"] == group))

def svg(title, subtitle, width, height, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{title}</title><desc id="desc">{subtitle}</desc>
<rect width="100%" height="100%" fill="#fbfaf7"/>
<style>text{{font-family:Arial,sans-serif;fill:#202b3c}} .title{{font-size:26px;font-weight:700}} .sub{{font-size:14px;fill:#566174}} .label{{font-size:15px}} .small{{font-size:12px;fill:#566174}} .value{{font-size:14px;font-weight:700}}</style>
<text x="42" y="45" class="title">{title}</text><text x="42" y="70" class="sub">{subtitle}</text>{body}
<text x="42" y="{height-22}" class="small">Source: Abdo (2020), thesis; aggregate values redrawn from cited pages. Percentages as reported.</text></svg>'''

def bar_chart(title, subtitle, rows, maxval, suffix, filename, width=760, row_height=46):
    top=112; height=top + len(rows)*row_height + 48; left=190; chartw=width-left-55
    parts=[]
    for i,(label,val,color) in enumerate(rows):
        y=top+i*row_height
        parts.append(f'<text x="{left-14}" y="{y+18}" text-anchor="end" class="label">{label}</text>')
        parts.append(f'<rect x="{left}" y="{y}" width="{chartw}" height="22" rx="5" fill="#e8e8e5"/>')
        parts.append(f'<rect x="{left}" y="{y}" width="{chartw*val/maxval:.1f}" height="22" rx="5" fill="{color}"/>')
        parts.append(f'<text x="{left+chartw*val/maxval+8:.1f}" y="{y+17}" class="value">{val:,}{suffix}</text>')
    (OUT/filename).write_text(svg(title,subtitle,width,height,''.join(parts)),encoding='utf-8')

blue='#365b84'; red='#bd4b55'; gold='#b68735'; green='#4b806b'
# Separate scales for narrative counts and word totals, each with its own panel.
parts=[]
for panel, measure, maximum, unit, y0 in [('Narratives','Narratives',3000,'narratives',128),('Corpus words','Corpus words',2000000,'words',260)]:
    parts.append(f'<text x="55" y="{y0-24}" class="label" font-weight="700">{panel}</text>')
    for j,group in enumerate(['MDD','BD']):
        val=value(measure,group); y=y0+j*46; x=220; w=420
        parts.append(f'<text x="{x-14}" y="{y+18}" text-anchor="end" class="label">{group}</text>')
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="22" rx="5" fill="#e8e8e5"/>')
        parts.append(f'<rect x="{x}" y="{y}" width="{w*val/maximum:.1f}" height="22" rx="5" fill="{blue if group=="MDD" else red}"/>')
        parts.append(f'<text x="{x+w*val/maximum+8:.1f}" y="{y+17}" class="value">{val:,} {unit}</text>')
(OUT/'corpus-profile.svg').write_text(svg('Corpus profile','Narratives and token counts reported in thesis, p. 14',760,420,''.join(parts)),encoding='utf-8')
bar_chart('Appraisal type distribution','Share of each corpus’s appraisal evaluations; thesis pp. 127–128',[
 ('MDD · Affect',value('Affect','MDD'),gold),('BD · Affect',value('Affect','BD'),gold),
 ('MDD · Judgment',value('Judgment','MDD'),blue),('BD · Judgment',value('Judgment','BD'),blue),
 ('MDD · Appreciation',value('Appreciation','MDD'),red),('BD · Appreciation',value('Appreciation','BD'),red)],50,'%','appraisal-types.svg',width=760,row_height=38)
bar_chart('Other reported outcomes','Percentages use distinct denominators; see notes in CSV (thesis pp. 128, 147)',[
 ('MDD · negative Affect',value('Negative emotions','MDD'),red),('BD · negative Affect',value('Negative emotions','BD'),red),
 ('MDD · Social Esteem',value('Social Esteem','MDD'),blue),('BD · Social Esteem',value('Social Esteem','BD'),blue),
 ('MDD · attitudinal fields',value('Attitudinal fields','MDD'),green),('BD · attitudinal fields',value('Attitudinal fields','BD'),green),
 ('Combined · attitudinal',value('Attitudinal fields','Combined'),gold)],100,'%','additional-outcomes.svg',width=900,row_height=38)
