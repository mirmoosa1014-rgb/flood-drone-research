"""Passive MAVLink normalization. No sends, commands, arm, or mission upload."""
import argparse,json,time

def normalize(message:dict,received_s:float)->dict:
    kind=message.get('mavpackettype')
    if kind=='ATTITUDE':return dict(type='attitude',boot_s=message['time_boot_ms']/1000,received_s=received_s,roll_rad=message['roll'],pitch_rad=message['pitch'])
    if kind=='GLOBAL_POSITION_INT':return dict(type='position',boot_s=message['time_boot_ms']/1000,received_s=received_s,lat=message['lat']/1e7,lon=message['lon']/1e7,altitude_m=message['alt']/1000,datum='MSL',relative_alt_m=message['relative_alt']/1000)
    if kind=='DISTANCE_SENSOR':
        distance=message['current_distance'];minimum=message.get('min_distance');maximum=message.get('max_distance');quality=message.get('signal_quality',0)
        # MAVLink quality 0 is unknown; 1 explicitly marks an invalid return.
        valid=all(type(v) is int and 0<=v<=65535 for v in (distance,minimum,maximum)) and minimum<=distance<=maximum and quality!=1
        return dict(type='range',boot_s=message['time_boot_ms']/1000,received_s=received_s,slant_range_m=distance/100,sensor_id=message['id'],orientation=message['orientation'],signal_quality=quality,range_valid=valid,usable_downward=message['orientation']==25 and valid)
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
