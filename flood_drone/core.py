from __future__ import annotations
from dataclasses import dataclass, asdict
import json, math, random
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
@dataclass(frozen=True)
class Sample:
    timestamp_s:float
    attitude_timestamp_s:float
    altitude_timestamp_s:float
    slant_range_m:float
    roll_rad:float
    pitch_rad:float
    altitude_m:float
    road_elevation_m:float
    datum:str='local_survey'
    road_datum:str='local_survey'
    altitude_sigma_m:float=.04
    range_sigma_m:float=.02
    baseline_sigma_m:float=.02
    attitude_sigma_rad:float=.01
    water_return_validated:bool=False
    source:str='external'
def estimate(sample:Sample,now_s:float)->dict:
    """Project a rigid downward beam; refuse unsynchronized/unvalidated water returns."""
    if not math.isfinite(now_s):raise ValueError('now_s must be finite')
    for key,value in asdict(sample).items():
        if isinstance(value,(float,int)) and not isinstance(value,bool) and not math.isfinite(value):raise ValueError(f'{key} must be finite')
    if any(getattr(sample,k)<0 for k in ['altitude_sigma_m','range_sigma_m','baseline_sigma_m','attitude_sigma_rad']):raise ValueError('uncertainties must be nonnegative')
    reasons=[]
    if now_s<sample.timestamp_s or now_s-sample.timestamp_s>2:reasons.append('stale_or_future_sample')
    if max(abs(sample.timestamp_s-sample.attitude_timestamp_s),abs(sample.timestamp_s-sample.altitude_timestamp_s))>.1:reasons.append('unsynchronized')
    if sample.datum!=sample.road_datum or sample.datum not in ('local_survey','NAVD88','MSL'):reasons.append('datum_mismatch_or_unknown')
    if not .2<=sample.slant_range_m<=8:reasons.append('range_outside_demo_envelope')
    if max(abs(sample.roll_rad),abs(sample.pitch_rad))>math.radians(25):reasons.append('excessive_tilt')
    if not sample.water_return_validated:reasons.append('water_return_not_validated')
    c=math.cos(sample.roll_rad)*math.cos(sample.pitch_rad);vertical=sample.slant_range_m*c
    raw_depth=sample.altitude_m-vertical-sample.road_elevation_m
    tilt_var=(sample.slant_range_m*math.sin(sample.roll_rad)*math.cos(sample.pitch_rad)*sample.attitude_sigma_rad)**2+(sample.slant_range_m*math.cos(sample.roll_rad)*math.sin(sample.pitch_rad)*sample.attitude_sigma_rad)**2
    sigma=math.sqrt(sample.altitude_sigma_m**2+(c*sample.range_sigma_m)**2+sample.baseline_sigma_m**2+tilt_var)
    if sigma>.15:reasons.append('uncertainty_too_large')
    return dict(accepted=not reasons,reasons=reasons,vertical_range_m=vertical,depth_m=max(0,raw_depth) if not reasons else None,raw_depth_m=raw_depth,sigma_m=sigma,interval_95_m=[max(0,raw_depth-1.96*sigma),max(0,raw_depth+1.96*sigma)] if not reasons else None,status='OBSERVATION_REQUIRES_REVIEW' if not reasons else 'UNKNOWN',source=sample.source)
def episode(seed:int,steps:int=120,storm:float=1.0)->list[dict]:
    if not 0<=seed<=2**31-1 or not 10<=steps<=360 or not .2<=storm<=3:raise ValueError('scenario outside bounded envelope')
    rng=random.Random(seed);peak,width=rng.uniform(25,65),rng.uniform(10,23);runoff,drainage=rng.uniform(.55,.9),rng.uniform(.008,.02)
    depth=.01;rain_sum=0;out=[]
    for t in range(steps):
        rain=storm*rng.uniform(.8,1.2)*70*math.exp(-((t-peak)/width)**2);rain_sum+=rain/60
        depth=max(0,depth+runoff*rain/60000*25-drainage*depth);gauge=max(0,depth+rng.gauss(0,.025))
        out.append(dict(minute=t,rain_mm_h=rain,gauge_m=gauge,truth_m=depth,accumulated_rain_mm=rain_sum))
    return out
def features(rows:list[dict],t:int)->list[float]:
    return [1,rows[t]['gauge_m'],rows[t]['rain_mm_h']/100,rows[t]['gauge_m']-rows[max(0,t-5)]['gauge_m'],sum(r['rain_mm_h'] for r in rows[max(0,t-9):t+1])/1000]
def solve(a,b):
    m=[list(row)+[v] for row,v in zip(a,b)];n=len(b)
    for k in range(n):
        p=max(range(k,n),key=lambda i:abs(m[i][k]));m[k],m[p]=m[p],m[k]
        if abs(m[k][k])<1e-12:raise ValueError('singular design')
        d=m[k][k];m[k]=[v/d for v in m[k]]
        for i in range(n):
            if i!=k:
                d=m[i][k];m[i]=[x-d*y for x,y in zip(m[i],m[k])]
    return [r[-1] for r in m]
def train(seeds=range(80))->dict:
    a=[[0.0]*5 for _ in range(5)];b=[0.0]*5
    for seed in seeds:
        rows=episode(seed)
        for t in range(5,110):
            x=features(rows,t);y=rows[t+10]['truth_m']
            for i in range(5):
                b[i]+=x[i]*y
                for j in range(5):a[i][j]+=x[i]*x[j]
    for i in range(1,5):a[i][i]+=.1
    return dict(type='ridge-linear',features=['intercept','current_gauge_m','rain_mm_h/100','gauge_delta_5min_m','rain_history_10min/1000'],coefficients=solve(a,b),horizon_min=10,train_seeds=list(seeds),version=1)
def predict(model,rows,t):return max(0,sum(a*b for a,b in zip(model['coefficients'],features(rows,t))))
def evaluate(model,seeds=range(1000,1020),storm=1.0):
    records=[]
    for seed in seeds:
        rows=episode(seed,storm=storm)
        for t in range(5,110):
            truth=rows[t+10]['truth_m'];p=predict(model,rows,t)
            records.append(dict(seed=seed,minute=t,truth_m=truth,prediction_m=p,persistence_m=rows[t]['gauge_m'],error_m=p-truth))
    mae=lambda key:sum(abs(r[key]-r['truth_m']) for r in records)/len(records)
    return dict(synthetic=True,episodes=len(list(seeds)),samples=len(records),storm_multiplier=storm,model_mae_m=mae('prediction_m'),persistence_mae_m=mae('persistence_m')),records
def demo(seed=2026,storm=1.0):
    model_path=ROOT/'models/hydrology.json';model=json.loads(model_path.read_text()) if model_path.exists() else train()
    rows=episode(seed,storm=storm);rng=random.Random(seed+1);samples=[]
    for t,row in enumerate(rows):
        x=60*t/(len(rows)-1);road=.6*((x-30)/30)**2;roll=.13*math.sin(t/8);pitch=.09*math.cos(t/11)
        surface=max(road,row['truth_m']);altitude=5.5;slant=(altitude-surface)/(math.cos(roll)*math.cos(pitch))+rng.gauss(0,.015)
        s=Sample(t*60,t*60,t*60,slant,roll,pitch,altitude,road,water_return_validated=t%13!=0,source='synthetic_replay');e=estimate(s,t*60)
        samples.append(dict(**row,x_m=x,road_m=road,water_surface_m=surface,roll_rad=roll,pitch_rad=pitch,slant_range_m=slant,altitude_m=altitude,local_truth_depth_m=max(0,surface-road),estimate=e,forecast_m=predict(model,rows,t)))
    return dict(synthetic=True,seed=seed,storm=storm,samples=samples,horizon_min=10,note='Synthetic replay. Illustrative forecast. No road is classified safe.',hardware=[dict(name='Pixhawk 2.4.8',port='Flight controller'),dict(name='ESP8266',port='TELEM1'),dict(name='TF-Luna',port='TELEM2'),dict(name='ESP32-CAM',port='PDB regulated 5V')])
