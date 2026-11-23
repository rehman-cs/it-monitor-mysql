CREATE DATABASE it_monitor;
USE it_monitor;

CREATE TABLE devices (
  device_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY ,
  name VARCHAR(50) NOT NULL,
  ip_address VARCHAR(50) NOT NULL,
  device_type VARCHAR(30) NOT NULL,
  location VARCHAR(50) NOT NULL,
  port INT DEFAULT NULL
  ) ;

CREATE TABLE checks (
  check_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  device_id INT NOT NULL,
  check_time DATETIME NOT NULL,
  status VARCHAR(10) NOT NULL,
  response_ms INT DEFAULT NULL,
  port_status VARCHAR(10) DEFAULT NULL,
  FOREIGN KEY (device_id) REFERENCES devices (device_id) ON DELETE CASCADE
  );

CREATE TABLE system_stats (
  stat_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY ,
  stat_time DATETIME NOT NULL,
  cpu_percent DECIMAL(5,2) NOT NULL,
  ram_percent DECIMAL(5,2) NOT NULL,
  disk_percent DECIMAL(5,2) NOT NULL
  );
