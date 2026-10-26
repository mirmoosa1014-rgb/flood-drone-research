"""Dependency-free loopback server for the same engine and built frontend."""
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from urllib.parse import urlsplit,parse_qs
from .core import ROOT,Sample,demo,estimate
import json,argparse
class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(ROOT/'frontend/dist'),**kwargs)
    def reply(self,code,data):
        blob=json.dumps(data,allow_nan=False).encode();self.send_response(code);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(blob)));self.end_headers();self.wfile.write(blob)
    def do_GET(self):
        p=urlsplit(self.path);q=parse_qs(p.query)
        if p.path=='/api/health':return self.reply(200,dict(ok=True,mode='research',flight_commands=False))
        if p.path=='/api/demo':
            try:return self.reply(200,demo(int(q.get('seed',['2026'])[0]),float(q.get('storm',['1'])[0])))
            except (ValueError,OverflowError):return self.reply(422,dict(error='Invalid bounded scenario'))
        return super().do_GET()
    def do_POST(self):
        if self.path!='/api/telemetry':return self.reply(404,{'error':'Unknown endpoint'})
        try:
            n=int(self.headers.get('Content-Length','0'))
            if not 0<n<10000:return self.reply(413,{'error':'Telemetry body must be below 10kB'})
            body=json.loads(self.rfile.read(n));now=body.pop('now_s');return self.reply(200,estimate(Sample(**body),now))
        except (ValueError,TypeError,KeyError):return self.reply(422,{'error':'Malformed telemetry'})
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=8106);a=p.parse_args();print(f'Flood Drone research workbench http://127.0.0.1:{a.port}',flush=True);ThreadingHTTPServer(('127.0.0.1',a.port),Handler).serve_forever()
