import unittest
try:
    from fastapi.testclient import TestClient
    from flood_drone.api import app
except ImportError:TestClient=None
@unittest.skipIf(TestClient is None,'Install requirements.txt for FastAPI checks')
class API(unittest.TestCase):
    def setUp(self):self.c=TestClient(app)
    def test_health(self):self.assertFalse(self.c.get('/api/health').json()['flight_commands'])
    def test_demo(self):self.assertEqual(len(self.c.get('/api/demo').json()['samples']),120)
    def test_bounds(self):self.assertEqual(self.c.get('/api/demo?storm=200').status_code,422)
    def test_bad_telemetry(self):self.assertEqual(self.c.post('/api/telemetry',json={'bad':1}).status_code,422)
    def test_no_commands(self):self.assertIn(self.c.post('/api/arm').status_code,(404,405))
