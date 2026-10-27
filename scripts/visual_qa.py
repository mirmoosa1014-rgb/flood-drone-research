"""Run the built app and Playwright checks without touching model/evidence data."""
from pathlib import Path
import argparse,json,os,socket,subprocess,sys,tempfile,time,urllib.request
root=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=8106);args=p.parse_args()
if not (root/'frontend/dist/index.html').exists():raise SystemExit('Build first: cd frontend && npm ci && npm run build')
with socket.socket() as probe:
    try:probe.bind(('127.0.0.1',args.port))
    except OSError as e:raise SystemExit(f'Port {args.port} unavailable; choose --port: {e}')
with tempfile.TemporaryFile(mode='w+t') as log:
    proc=subprocess.Popen([sys.executable,'-m','flood_drone.server','--port',str(args.port)],cwd=root,stdout=log,stderr=log)
    try:
        endpoint=f'http://127.0.0.1:{args.port}'
        for _ in range(100):
            if proc.poll() is not None:
                log.seek(0);raise RuntimeError('Server stopped: '+log.read())
            try:
                with urllib.request.urlopen(endpoint+'/api/health',timeout=.5) as response:
                    if json.load(response).get('ok'):break
            except OSError:time.sleep(.05)
        else:raise RuntimeError('Server did not become ready')
        env=os.environ.copy();env['APP_URL']=endpoint
        result=subprocess.run(['node','scripts/browser.mjs'],cwd=root/'frontend',env=env)
        if result.returncode:raise SystemExit(result.returncode)
    finally:
        proc.terminate()
        try:proc.wait(timeout=5)
        except subprocess.TimeoutExpired:proc.kill();proc.wait()
