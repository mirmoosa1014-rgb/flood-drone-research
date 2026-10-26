"""Optional FastAPI interface, intentionally no flight commands."""
from fastapi import FastAPI,HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel,ConfigDict,Field
from .core import ROOT,Sample,demo,estimate
app=FastAPI(title='Flood Drone Research Workbench',version='1.0.0')
class Telemetry(BaseModel):
    model_config=ConfigDict(extra='forbid',allow_inf_nan=False)
    timestamp_s:float
    attitude_timestamp_s:float
    altitude_timestamp_s:float
    slant_range_m:float
    roll_rad:float
    pitch_rad:float
    altitude_m:float
    road_elevation_m:float
    datum:str='unknown'
    road_datum:str='local_survey'
    altitude_sigma_m:float=Field(default=2,ge=0)
    range_sigma_m:float=Field(default=.02,ge=0)
    baseline_sigma_m:float=Field(default=.02,ge=0)
    attitude_sigma_rad:float=Field(default=.01,ge=0)
    water_return_validated:bool=False
    source:str='external'
    now_s:float
@app.get('/api/health')
def health():return {'ok':True,'mode':'research','flight_commands':False}
@app.get('/api/demo')
def replay(seed:int=2026,storm:float=1):
    try:return demo(seed,storm)
    except ValueError as e:raise HTTPException(422,str(e))
@app.post('/api/telemetry')
def telemetry(body:Telemetry):
    d=body.model_dump();now=d.pop('now_s')
    try:return estimate(Sample(**d),now)
    except ValueError as e:raise HTTPException(422,str(e))
if (ROOT/'frontend/dist').exists():app.mount('/',StaticFiles(directory=ROOT/'frontend/dist',html=True),name='frontend')
