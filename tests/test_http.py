import unittest,subprocess,sys,time,json,urllib.request,socket
from urllib.error import HTTPError
from flood_drone.core import ROOT
class HTTP(unittest.TestCase):
    def test_server(self):
        with socket.socket() as probe:
            probe.bind(('127.0.0.1',0));port=probe.getsockname()[1]
        proc=subprocess.Popen([sys.executable,'-m','flood_drone.server','--port',str(port)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        try:
            url=f'http://127.0.0.1:{port}'
            for i in range(30):
                try:
                    with urllib.request.urlopen(url+'/api/health',timeout=1) as response:health=json.load(response)
                    break
                except OSError:time.sleep(.05)
            else:self.fail('Local HTTP server did not start')
            self.assertTrue(health['ok']);self.assertFalse(health['flight_commands'])
            with urllib.request.urlopen(url+'/api/demo?seed=2026',timeout=5) as response:replay=json.load(response)
            self.assertEqual(len(replay['samples']),120)
            for payload in [None, 'not an object', 7, True, [], {}]:
                with self.subTest(payload=payload):
                    request=urllib.request.Request(url+'/api/telemetry',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'})
                    with self.assertRaises(HTTPError) as error:
                        urllib.request.urlopen(request,timeout=5)
                    with error.exception as response:
                        self.assertEqual(response.code,422)
                        self.assertEqual(json.load(response),{'error':'Malformed telemetry'})
            with urllib.request.urlopen(url+'/api/health',timeout=5) as response:
                self.assertTrue(json.load(response)['ok'])
            if (ROOT/'frontend/dist/index.html').exists():
                with urllib.request.urlopen(url,timeout=5) as response:self.assertIn('Crossing Observatory',response.read().decode())
        finally:proc.terminate();proc.wait(timeout=5)
