create table run_log (
    id uuid primary key,
    start_time timestamptz,
    machine_type text,
    sensor_address integer
);

create table sensor_readings (
    id uuid primary key,
    run_log_id uuid,
    x decimal,
    y decimal,
    z decimal,
    sensor_type text,
    timestamp timestamptz
);