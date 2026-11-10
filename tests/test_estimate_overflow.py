import unittest,math
from dataclasses import replace
from flood_drone.core import Sample,estimate
class EstimateOverflow(unittest.TestCase):
 def test_large_uncertainty_is_rejected_without_overflow(self):
  s=Sample(0,0,0,2,0,0,3,0,altitude_sigma_m=1e200,water_return_validated=True)
  r=estimate(s,0);self.assertFalse(r['accepted']);self.assertTrue(math.isfinite(r['sigma_m']))
 def test_overflowed_depth_is_not_serialized(self):
  s=Sample(0,0,0,2,0,0,1e308,-1e308,water_return_validated=True)
  with self.assertRaises(ValueError):estimate(s,0)
