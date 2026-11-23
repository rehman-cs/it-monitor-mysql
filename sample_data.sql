USE it_monitor;
 INSERT INTO devices
 VALUES
 (DEFAULT,
 'This PC',
 '127.0.0.1',
 'PC',
 'Home',
 NULL) ;

 INSERT INTO devices
 VALUES
 (DEFAULT,
 'Home Router',
 '192.168.1.1',
 'Router',
 'Home',
 80) ;

 INSERT INTO devices
 VALUES
 (DEFAULT,
 'Google DNS',
 '8.8.8.8',
 'Server',
 'Internet',
 443) ;

 INSERT INTO devices
 VALUES
 (DEFAULT,
 'Cloudflare DNS',
 '1.1.1.1',
 'Server',
 'Internet',
 443) ;

 INSERT INTO devices
 VALUES
 (DEFAULT,
 'Old Printer',
 '192.168.1.250',
 'Printer',
 'Office',
 NULL) ;



 INSERT INTO checks
 VALUES (DEFAULT,
 1,
 '2026-11-20 09:00:00',
 'ONLINE',
 1,
 NULL);

 INSERT INTO checks
 VALUES (DEFAULT,
 2,
 '2026-11-20 09:00:00',
 'ONLINE',
 3,
 'OPEN');

 INSERT INTO checks
 VALUES (DEFAULT,
 3,
 '2026-11-20 09:00:00',
 'ONLINE',
 41,
 'OPEN');

 INSERT INTO checks
 VALUES (DEFAULT,
 4,
 '2026-11-20 09:00:00',
 'ONLINE',
 38,
 'OPEN');

 INSERT INTO checks
 VALUES (DEFAULT,
 5,
 '2026-11-20 09:00:00',
 'OFFLINE',
 NULL,
 NULL);

 INSERT INTO checks
 VALUES (DEFAULT,
 2,
 '2026-11-21 09:00:00',
 'OFFLINE',
 NULL,
 'CLOSED');

 INSERT INTO checks
 VALUES (DEFAULT,
 3,
 '2026-11-21 09:00:00',
 'ONLINE',
 45,
 'OPEN');

 INSERT INTO checks
 VALUES (DEFAULT,
 5,
 '2026-11-21 09:00:00',
 'OFFLINE',
 NULL,
 NULL);



 INSERT INTO system_stats
 VALUES (DEFAULT,
 '2026-11-20 09:00:00',
 23.50,
 61.20,
 48.00);

 INSERT INTO system_stats
 VALUES (DEFAULT,
 '2026-11-21 09:00:00',
 87.10,
 92.40,
 48.10);
