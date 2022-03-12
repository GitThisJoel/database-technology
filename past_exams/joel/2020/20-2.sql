-- (b)
DROP TABLE IF EXISTS apartments;
CREATE TABLE apartments (
    apartment_id    TEXT,
    building_id     TEXT,
    owner_id        TEXT,
    nbr_of_rooms    INT,
    area            REAL,
    monthly_rent    REAL,
    latest_owner_change_year    INT,
    PRIMARY KEY (apartment_id),
    FOREIGN KEY (building_id) REFERENCES buildings(building_id),
    FOREIGN KEY (owner_id) REFERENCES owners(owner_id)
);

-- (c)
-- Lista ägar-id och namn för de senaste 10 nya medlemmarna i bostadsrättsföreningen 
-- ingen  köper mer än en lägenhet,  
-- alla har olika namn).
SELECT  owner_id, name 
FROM    owners
JOIN    apartments
USING   (owner_id)
ORDER BY latest_owner_change_year DESC
LIMIT   10;

-- (d)
SELECT  name 
FROM    owners
JOIN    apartments
USING   (owner_id)
JOIN    buildings
USING   (building_id)
WHERE   apartments.nbr_of_rooms = 1 AND buildings.address = "Storgatan 1" -- när HAVING när WHERE när ON?
ORDER BY  name;

-- (e)
-- Höj hyran för alla lägenheter på adressen ”Storgatan 1” med 1.8%.

-- !!!!!!!!!!!
UPDATE apartments
SET monthly_rent = 1.018 * monthly_rent
WHERE building_id IN (
        SELECT building_id
        FROM buildings
        WHERE address = "Storgatan 1"
    );

-- (f)
SELECT    owner_id, name
FROM      owners
JOIN      apartments
USING     (owner_id) 
GROUP BY  owner_id
HAVING    count() > 1; -- när HAVING när WHERE när ON?

-- (g)
-- Lista lägenhetsnummer och adress för de lägenheter i vilka inga 
-- reparationer har gjorts efter 2010-01-01
SELECT  apartment_id, address
FROM    repairs
JOIN    apartments
USING   (apartment_id)
JOIN    buildings
USING   (building_id)
GROUP BY  apartment_id
WHERE   year > 2010 AND repair_id IS NULL

-- (h)
-- Lista building_id och total reparationskostnad per hus för reparationer gjorda
-- 2019 – hus som inte har reparerats alls skall få kostnaden 0

-- ???
SELECT building_id, sum(cost) AS total_cost
FROM repairs
JOIN apartments
USING (apartment_id)
JOIN buildings
USING (building_id)
GROUP BY apartment_id
-- How do a default to 0?


-- (i)
-- Ge en lista på samtliga fastigheter (adressen) 
-- och deras totala boyta, sortera efter avtagande boyta. 
-- Observera att det kan finnas fastigheter utan någon boyta 

-- ???? 
SELECT address, sum(area) AS total_area
FROM buildings
JOIN apartments
USING (building_id)
WHERE area NOT NULL
GROUP BY apartment_id
ORDER BY total_area DESC


