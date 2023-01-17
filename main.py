from mpu6050 import mpu6050
import time
import math
import os
from twilio.rest import Client

in_cycle_sleep_seconds = 5
out_of_cycle_sleep_seconds = 30

is_in_cycle = False

mpu = mpu6050(0x68)
accel_similar_max = 6
gyro_similar_max = 6

gyro_tolerance = 0.25
accel_tolerance = 0.15

prev_accel = mpu.get_accel_data()
accel_similar_for_count = 0
prev_gyro = mpu.get_gyro_data()
gyro_similar_for_count = 0

while True:
    print("Temp : "+str(mpu.get_temp()))
    print()

    accel_data = mpu.get_accel_data()

    if math.isclose(accel_data['x'], prev_accel['x'], abs_tol=accel_tolerance) and math.isclose(accel_data['y'], prev_accel['y'], abs_tol=accel_tolerance) and math.isclose(accel_data['z'], prev_accel['z'], abs_tol=accel_tolerance):
        accel_similar_for_count += 1
    else:
        accel_similar_for_count = 0

    print("Acc X Diff: "+str(abs(accel_data['x'] - prev_accel['x'])))
    print("Acc Y Diff: "+str(abs(accel_data['y'] - prev_accel['y'])))
    print("Acc Z Diff: "+str(abs(accel_data['z'] - prev_accel['z'])))
    print()

    prev_accel = accel_data

    gyro_data = mpu.get_gyro_data()

    if math.isclose(gyro_data['x'], prev_gyro['x'], abs_tol=gyro_tolerance) and math.isclose(gyro_data['y'], prev_gyro['y'], abs_tol=gyro_tolerance) and math.isclose(gyro_data['z'], prev_gyro['z'], abs_tol=gyro_tolerance):
        gyro_similar_for_count += 1
    else:
        gyro_similar_for_count = 0

    print("Gyro X Diff: "+str(abs(gyro_data['x'] - prev_gyro['x'])))
    print("Gyro Y Diff: "+str(abs(gyro_data['y'] - prev_gyro['y'])))
    print("Gyro Z Diff: "+str(abs(gyro_data['z'] - prev_gyro['z'])))
    print()
    print("-------------------------------")

    prev_gyro = gyro_data

    if gyro_similar_for_count < gyro_similar_max and accel_similar_for_count < accel_similar_max:
        if is_in_cycle:
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

        is_in_cycle = not is_in_cycle
        print("Is in cycle: " + str(is_in_cycle))

    time.sleep(
        in_cycle_sleep_seconds if is_in_cycle else out_of_cycle_sleep_seconds)