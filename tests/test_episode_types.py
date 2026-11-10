import unittest
from flood_drone.core import episode
class EpisodeTypes(unittest.TestCase):
 def test_bad_seed_or_steps(self):
  for args in [(True,120),(1.5,120),(1,10.5)]:
   with self.subTest(args=args),self.assertRaises(ValueError):episode(*args)
 def test_bad_storm(self):
  with self.assertRaises(ValueError):episode(1,storm=True)
