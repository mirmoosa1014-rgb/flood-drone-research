import unittest,math
from dataclasses import replace
from flood_drone.core import Sample,estimate,episode,train,predict,features,evaluate
from flood_drone.telemetry import normalize
class Tests(unittest.TestCase):
    def setUp(self):self.s=Sample(10,10,10,4,0,0,5,0,water_return_validated=True)
    def test_projection(self):self.assertAlmostEqual(estimate(self.s,10)['depth_m'],1)
    def test_tilt(self):self.assertAlmostEqual(estimate(replace(self.s,roll_rad=.2,pitch_rad=.1),10)['depth_m'],5-4*math.cos(.2)*math.cos(.1))
    def test_stale(self):self.assertFalse(estimate(self.s,13)['accepted'])
    def test_future(self):self.assertFalse(estimate(self.s,9)['accepted'])
    def test_sync(self):self.assertIn('unsynchronized',estimate(replace(self.s,attitude_timestamp_s=9),10)['reasons'])
    def test_alt_sync(self):self.assertFalse(estimate(replace(self.s,altitude_timestamp_s=9),10)['accepted'])
    def test_datum(self):self.assertFalse(estimate(replace(self.s,datum='ellipsoid'),10)['accepted'])
    def test_uncertainty(self):self.assertFalse(estimate(replace(self.s,altitude_sigma_m=2),10)['accepted'])
    def test_water_validation(self):self.assertEqual(estimate(replace(self.s,water_return_validated=False),10)['depth_m'],None)
    def test_range(self):self.assertFalse(estimate(replace(self.s,slant_range_m=.1),10)['accepted'])
    def test_tilt_bound(self):self.assertFalse(estimate(replace(self.s,roll_rad=.5),10)['accepted'])
    def test_nan(self):
        with self.assertRaises(ValueError):estimate(replace(self.s,slant_range_m=float('nan')),10)
        with self.assertRaises(ValueError):estimate(self.s,float('nan'))
    def test_negative_sigma(self):
        with self.assertRaises(ValueError):estimate(replace(self.s,range_sigma_m=-1),10)
    def test_interval(self):
        e=estimate(self.s,10);self.assertLess(e['interval_95_m'][0],1);self.assertGreater(e['interval_95_m'][1],1)
    def test_replay(self):self.assertEqual(episode(4),episode(4));self.assertNotEqual(episode(4),episode(5))
    def test_nonnegative(self):self.assertTrue(all(r['truth_m']>=0 for r in episode(4)))
    def test_causality(self):
        rows=episode(4);a=features(rows,10);rows[11]['gauge_m']=999;self.assertEqual(a,features(rows,10))
    def test_split(self):
        m=train(range(3));metrics,rows=evaluate(m,range(1000,1002));self.assertFalse(set(m['train_seeds'])&{r['seed'] for r in rows});self.assertTrue(math.isfinite(metrics['model_mae_m']))
    def test_model(self):
        m=train(range(3));self.assertEqual(len(m['coefficients']),5);self.assertGreaterEqual(predict(m,episode(7),30),0)
    def test_normalize(self):
        a=normalize(dict(mavpackettype='GLOBAL_POSITION_INT',time_boot_ms=1000,lat=330000000,lon=-960000000,alt=123000,relative_alt=5000),4);self.assertEqual(a['altitude_m'],123);self.assertEqual(a['datum'],'MSL');self.assertEqual(a['relative_alt_m'],5)
    def test_range_orientation(self):
        x=normalize(dict(mavpackettype='DISTANCE_SENSOR',time_boot_ms=1000,current_distance=250,id=1,orientation=0),4);self.assertFalse(x['usable_downward']);self.assertEqual(x['slant_range_m'],2.5)
    def test_bounds(self):
        with self.assertRaises(ValueError):episode(-1)
        with self.assertRaises(ValueError):episode(1,storm=100)
if __name__=='__main__':unittest.main()
