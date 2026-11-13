import unittest
from fastapi.testclient import TestClient
from flood_drone.api import app
class TelemetryCoercion(unittest.TestCase):
 def test_validation_flag_and_measurements_keep_original_types(self):
  body=dict(timestamp_s=0,attitude_timestamp_s=0,altitude_timestamp_s=0,slant_range_m=2,roll_rad=0,pitch_rad=0,altitude_m=3,road_elevation_m=0,datum='local_survey',altitude_sigma_m=.04,water_return_validated=True,now_s=0)
  with TestClient(app) as client:
   self.assertTrue(client.post('/api/telemetry',json=body).json()['accepted'])
   for key,value in [('water_return_validated','true'),('water_return_validated',1),('altitude_m',True),('slant_range_m','2')]:
    with self.subTest(key=key,value=value):self.assertEqual(client.post('/api/telemetry',json={**body,key:value}).status_code,422)
