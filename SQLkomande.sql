CREATE TABLE satellites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL,  
    x FLOAT NOT NULL,           
    y FLOAT NOT NULL,           
    z FLOAT NOT NULL,           
    last_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE satellites
ADD COLUMN orbital_period FLOAT NOT NULL DEFAULT 5400;


SELECT * FROM satellites

INSERT INTO satellites (name, x, y, z)
VALUES (
    'LEO',
    6771,  -- 6371 km (Earth radius) + 400 km (orbit altitude)
    0,
    0
);

UPDATE satellites
SET orbital_period = 5400 
WHERE id = 1;  


INSERT INTO satellites (name, x, y, z, orbital_period)
VALUES (
    'SOPRANO',
    7000,  
    0,
    0,
    3600
);

UPDATE satellites
SET direction = -1  
WHERE name = 'SOPRANO';

INSERT INTO satellites (name, x, y, z, orbital_period)
VALUES (
    'TEST',
    8000,  
    0,
    0,
    4000
);

ALTER TABLE satellites
ADD COLUMN direction INTEGER NOT NULL DEFAULT 1;


INSERT INTO satellites (name, x, y, z, orbital_period)
VALUES (
    'MECHA',
    12000,  
    0,
    0,
    7000
);

INSERT INTO satellites (name, x, y, z, orbital_period, direction)
VALUES (
    'Moon',
    384400,  
    0,
    0,
    2360592,  
    1  
);

ALTER TABLE satellites ADD COLUMN orbit_type TEXT DEFAULT 'XY';

INSERT INTO satellites (name, x, y, z, orbital_period, direction, orbit_type)
VALUES ('ASMO', 12000, 0, 0, 5400, 1, 'XZ');

INSERT INTO satellites (name, x, y, z, orbital_period, direction, orbit_type)
VALUES ('XY', 7000, 0, 0, 5400, 1, 'XY');


INSERT INTO satellites (name, x, y, z, orbital_period, direction, orbit_type)
VALUES ('YZ', 0, 7000, 0, 5400, 1, 'YZ');

DELETE FROM satellites WHERE name = 'LEO';
