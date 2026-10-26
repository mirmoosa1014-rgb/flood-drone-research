"""Train and evaluate whole held-out synthetic episodes; write auditable evidence."""
import argparse,csv,json,sys,statistics
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from flood_drone.core import ROOT,train,evaluate,demo
p=argparse.ArgumentParser();p.add_argument('--quick',action='store_true');args=p.parse_args()
model=train(range(20 if args.quick else 80));(ROOT/'models/hydrology.json').write_text(json.dumps(model,indent=2)+'\n');reports=[];all_rows=[]
for name,seeds,storm in [('held_out',range(1000,1005 if args.quick else 1020),1.0),('ood_intense',range(2000,2005 if args.quick else 2020),2.5)]:
    metrics,records=evaluate(model,seeds,storm);metrics['split']=name;errs=[abs(r['error_m']) for r in records];metrics['absolute_error_p95_m']=sorted(errs)[int(.95*(len(errs)-1))];metrics['per_episode_mae_std_m']=statistics.pstdev([statistics.mean(abs(r['error_m']) for r in records if r['seed']==seed) for seed in seeds]);reports.append(metrics)
    for row in records:row['split']=name
    all_rows+=records
(ROOT/'results/metrics.json').write_text(json.dumps(reports,indent=2)+'\n')
with (ROOT/'results/predictions.csv').open('w') as f:
    w=csv.DictWriter(f,fieldnames=list(all_rows[0]));w.writeheader();w.writerows(all_rows)
replay=demo();(ROOT/'results/demo.json').write_text(json.dumps(replay,indent=2)+'\n');rows=replay['samples'];mx=max(r['truth_m'] for r in rows)*1.2
points=lambda field,offset=0:' '.join(f'{70+(i+offset)/119*1040:.2f},{310-row[field]/mx*200:.2f}' for i,row in enumerate(rows[:120-offset]))
svg='''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="570" viewBox="0 0 1200 570"><rect width="1200" height="570" rx="20" fill="#071724"/><text x="58" y="48" fill="#55d4de" font-family="sans-serif" font-size="13" letter-spacing="3">FLOOD DRONE / SYNTHETIC EVIDENCE</text><text x="58" y="96" fill="#e2f2fc" font-family="sans-serif" font-size="32">A forecast with its limitations in view.</text><text x="58" y="127" fill="#8aafc4" font-family="sans-serif" font-size="15">Seed 2026 · crossing dip depth · ten-minute horizon · whole-episode holdout</text>'''
for i in range(5):
    y=310-i*50;svg+=f'<line x1="70" x2="1110" y1="{y}" y2="{y}" stroke="#1d394b"/><text x="20" y="{y+5}" fill="#8aafc4" font-family="sans-serif" font-size="12">{mx*i/4:.2f}</text>'
svg+=f'<polyline points="{points("truth_m")}" fill="none" stroke="#54d9dc" stroke-width="3"/><polyline points="{points("forecast_m",10)}" fill="none" stroke="#f6b96b" stroke-width="3" stroke-dasharray="7 5"/>'
svg+='<text x="70" y="340" fill="#8aafc4" font-family="sans-serif" font-size="13">Depth (m) · vertical axis</text><text x="900" y="340" fill="#8aafc4" font-family="sans-serif" font-size="13">Elapsed time: 0–119 min</text><text x="70" y="379" fill="#54d9dc" font-family="sans-serif" font-size="14">— Synthetic crossing truth</text><text x="400" y="379" fill="#f6b96b" font-family="sans-serif" font-size="14">┄ Forecast aligned to valid time</text>'
for i,m in enumerate(reports):
    x=70+i*540;svg+=f'<rect x="{x}" y="410" width="500" height="104" rx="10" fill="#102b3a"/><text x="{x+20}" y="439" fill="#a2c4d3" font-family="sans-serif" font-size="13">{m["split"]} / {m["episodes"]} episodes</text><text x="{x+20}" y="478" fill="#e1f4ff" font-family="sans-serif" font-size="24">MAE {m["model_mae_m"]:.4f} m</text><text x="{x+265}" y="478" fill="#a2c4d3" font-family="sans-serif" font-size="13">Persistence {m["persistence_mae_m"]:.4f} m</text>'
svg+='<text x="70" y="547" fill="#729aac" font-family="sans-serif" font-size="12">All results synthetic. No validated water-surface measurement, real-world forecast or driveability claim.</text></svg>'
(ROOT/'docs/images/evidence.svg').write_text(svg);print(json.dumps(reports,indent=2))
