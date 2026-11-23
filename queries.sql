USE it_monitor;

-- 1) Availability per device in percent (worst device first)
SELECT
d.name,
d.ip_address,
COUNT(c.check_id) AS total_checks,
SUM(c.status='ONLINE') AS online_checks,
ROUND(SUM(c.status='ONLINE')*100/COUNT(c.check_id),1) AS availability_percent,
ROUND(AVG(c.response_ms),1) AS average_ms
FROM devices d
JOIN checks c
    ON c.device_id=d.device_id
    GROUP BY d.device_id, d.name, d.ip_address
    ORDER BY availability_percent ASC;

-- 2) Outages per day
SELECT
DATE(c.check_time) AS day,
COUNT(*) AS offline_checks
FROM checks c
WHERE c.status='OFFLINE'
    GROUP BY DATE(c.check_time)
    ORDER BY day;

-- 3) Devices that were offline at least once
SELECT
d.name,
d.device_type,
d.location,
COUNT(*) AS times_offline,
MAX(c.check_time) AS last_time_offline
FROM devices d
JOIN checks c
    ON c.device_id=d.device_id
WHERE c.status='OFFLINE'
    GROUP BY d.device_id, d.name, d.device_type, d.location
    ORDER BY times_offline DESC;

-- 4) Average and highest load of this PC
SELECT
ROUND(AVG(cpu_percent),1) AS average_cpu,
MAX(cpu_percent) AS highest_cpu,
ROUND(AVG(ram_percent),1) AS average_ram,
MAX(ram_percent) AS highest_ram,
MAX(disk_percent) AS highest_disk
FROM system_stats;
