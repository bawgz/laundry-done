from mpu6050 import mpu6050
import time
import math
import os
import uuid
import datetime
from twilio.rest import Client
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import RunLog
from models import SensorReading

is_in_cycle = False

mpu = mpu6050(0x68)
accel_similar_max = 30
gyro_similar_max = 30

gyro_diff_max = 10
accel_diff_max = 10

gyro_tolerance = 0.25
accel_tolerance = 0.25

prev_accel = mpu.get_accel_data()
accel_similar_for_count = 0
accel_diff_for_count = 0
prev_gyro = mpu.get_gyro_data()
gyro_similar_for_count = 0
gyro_diff_for_count = 0

engine = create_engine("postgresql://root:password@localhost/laundry_monitor")
run_log_id = uuid.uuid4()

with Session(engine) as session:

    run_log = RunLog(
        id=run_log_id,
        start_time=datetime.datetime.now(),
        machine_type="washer",
        sensor_address=68
    )

    session.add(run_log)

    session.commit()

    while True:

        accel_data = mpu.get_accel_data()
        accel_sensor_reading = SensorReading(
            id=uuid.uuid4(),
            run_log_id=run_log_id,
            x=accel_data['x'],
            y=accel_data['y'],
            z=accel_data['z'],
            sensor_type='accel',
            timestamp=datetime.datetime.now()
        )

        session.add(accel_sensor_reading)

        if math.isclose(accel_data['x'], prev_accel['x'], abs_tol=accel_tolerance) and math.isclose(accel_data['y'], prev_accel['y'], abs_tol=accel_tolerance) and math.isclose(accel_data['z'], prev_accel['z'], abs_tol=accel_tolerance):
            accel_similar_for_count += 1
            accel_diff_for_count = 0
        else:
            accel_similar_for_count = 0
            accel_diff_for_count += 1

        print("Acc X Diff: "+str(abs(accel_data['x'] - prev_accel['x'])))
        print("Acc Y Diff: "+str(abs(accel_data['y'] - prev_accel['y'])))
        print("Acc Z Diff: "+str(abs(accel_data['z'] - prev_accel['z'])))
        print()

        prev_accel = accel_data

        gyro_data = mpu.get_gyro_data()
        gyro_sensor_reading = SensorReading(
            id=uuid.uuid4(),
            run_log_id=run_log_id,
            x=gyro_data['x'],
            y=gyro_data['y'],
            z=gyro_data['z'],
            sensor_type='gyro',
            timestamp=datetime.datetime.now()
        )

        session.add(gyro_sensor_reading)
        session.commit()

        if math.isclose(gyro_data['x'], prev_gyro['x'], abs_tol=gyro_tolerance) and math.isclose(gyro_data['y'], prev_gyro['y'], abs_tol=gyro_tolerance) and math.isclose(gyro_data['z'], prev_gyro['z'], abs_tol=gyro_tolerance):
            gyro_similar_for_count += 1
            gyro_diff_for_count = 0
        else:
            gyro_similar_for_count = 0
            gyro_diff_for_count += 1

        print("Gyro X Diff: "+str(abs(gyro_data['x'] - prev_gyro['x'])))
        print("Gyro Y Diff: "+str(abs(gyro_data['y'] - prev_gyro['y'])))
        print("Gyro Z Diff: "+str(abs(gyro_data['z'] - prev_gyro['z'])))
        print()

        prev_gyro = gyro_data

        if is_in_cycle and (gyro_similar_for_count >= gyro_similar_max or accel_similar_for_count >= accel_similar_max):
            print("gyro_similar_for_count: " + str(gyro_similar_for_count) +
                  " accel_similar_for_count: " + str(accel_similar_for_count))
            print("DONE!!!!!!!!! @ " + str(time.time()))

            account_sid = os.environ['TWILIO_ACCOUNT_SID']
            auth_token = os.environ['TWILIO_AUTH_TOKEN']
            from_num = os.environ['TWILIO_FROM_NUM']
            to_num = os.environ['TWILIO_TO_NUM']
            client = Client(account_sid, auth_token)

            message = client.messages \
                .create(
                    body='Your laundry is done!!!!!!!',
                    from_=from_num,  # ex: '+15017122661'
                    to=to_num  # ex: '+15558675310'
                )

            print(message.sid)

            is_in_cycle = False
            gyro_similar_for_count = 0
            gyro_diff_for_count = 0
            accel_similar_for_count = 0
            accel_diff_for_count = 0
        elif not is_in_cycle and (gyro_diff_for_count >= gyro_diff_max or accel_diff_for_count >= accel_diff_max):
            is_in_cycle = True
            gyro_similar_for_count = 0
            gyro_diff_for_count = 0
            accel_similar_for_count = 0
            accel_diff_for_count = 0

        print("Is in cycle: " + str(is_in_cycle))
        print("-------------------------------")
        time.sleep(1)
