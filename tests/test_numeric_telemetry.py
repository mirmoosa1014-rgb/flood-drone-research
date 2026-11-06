import unittest
from dataclasses import replace
from flood_drone.core import Sample, estimate


class NumericTelemetry(unittest.TestCase):
    def test_numeric_booleans_are_not_measurements(self):
        sample = Sample(10,10,10,4,0,0,5,0,water_return_validated=True)
        for name in ('timestamp_s','attitude_timestamp_s','altitude_timestamp_s',
                     'slant_range_m','roll_rad','pitch_rad','altitude_m','road_elevation_m',
                     'altitude_sigma_m','range_sigma_m','baseline_sigma_m','attitude_sigma_rad'):
            for value in (True, '1', None):
                with self.subTest(name=name,value=value), self.assertRaises(ValueError):
                    estimate(replace(sample, **{name:value}),10)
        with self.assertRaises(ValueError): estimate(sample,True)
