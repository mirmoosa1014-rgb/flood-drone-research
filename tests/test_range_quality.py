import unittest
from flood_drone.telemetry import normalize


class RangeQualityTests(unittest.TestCase):
    def test_range_bounds_and_signal_quality(self):
        for distance,quality,usable in [(100,0,True),(500,100,True),(99,100,False),(501,100,False),(250,1,False)]:
            with self.subTest(distance=distance,quality=quality):
                result=normalize(dict(mavpackettype='DISTANCE_SENSOR',time_boot_ms=1000,current_distance=distance,min_distance=100,max_distance=500,id=1,orientation=25,signal_quality=quality),4)
                self.assertIs(result['usable_downward'],usable)

    def test_missing_bounds_are_not_usable(self):
        result=normalize(dict(mavpackettype='DISTANCE_SENSOR',time_boot_ms=1000,current_distance=250,id=1,orientation=25),4)
        self.assertIs(result['usable_downward'],False)
