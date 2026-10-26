"""Passive MAVLink normalization. No sends, commands, arm, or mission upload."""
import argparse,json,time

def normalize(message:dict,received_s:float)->dict:
    kind=message.get('mavpackettype')
    if kind=='ATTITUDE':return dict(type='attitude',boot_s=message['time_boot_ms']/1000,received_s=received_s,roll_rad=message['roll'],pitch_rad=message['pitch'])
    if kind=='GLOBAL_POSITION_INT':return dict(type='position',boot_s=message['time_boot_ms']/1000,received_s=received_s,lat=message['lat']/1e7,lon=message['lon']/1e7,altitude_m=message['alt']/1000,datum='MSL',relative_alt_m=message['relative_alt']/1000)
    if kind=='DISTANCE_SENSOR':return dict(type='range',boot_s=message['time_boot_ms']/1000,received_s=received_s,slant_range_m=message['current_distance']/100,sensor_id=message['id'],orientation=message['orientation'],usable_downward=message['orientation']==25)
    return dict(type='ignored',message_type=kind)
def main():
    p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=14550);a=p.parse_args();from pymavlink import mavutil
    conn=mavutil.mavlink_connection(f'udpin:127.0.0.1:{a.port}')
    try:
        while True:
            msg=conn.recv_match(blocking=True,timeout=1)
            if msg and msg.get_type()!='BAD_DATA':print(json.dumps(normalize(msg.to_dict(),time.monotonic())),flush=True)
    except KeyboardInterrupt:pass
    finally:conn.close()
if __name__=='__main__':main()
