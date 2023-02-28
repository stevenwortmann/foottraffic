CREATE OR REPLACE PROCEDURE insertBrandsWeek(
    a_placekey VARCHAR,
    w_daterangestart VARCHAR,
    ak_relatedsameweekbrand VARCHAR,
    ak_relatedsameweekbrand_cnt INT,
    day_week_ind CHAR
)

LANGUAGE plpgsql
AS $$

DECLARE 
    vidout INT;
    bidout INT;
    locidout INT;

BEGIN
    IF EXISTS (SELECT 1 FROM brandsInfo WHERE brand_name=ak_relatedsameweekbrand)
    THEN
        SELECT bid INTO bidout FROM brandsInfo WHERE brand_name = ak_relatedsameweekbrand;
    ELSE
        INSERT INTO brandsInfo (brand_name)
            VALUES (ak_relatedsameweekbrand)
        SELECT LASTVAL() INTO bidout;
    END IF;

    IF EXISTS (SELECT 1 FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=a_placekey AND v.week_begin=w_daterangestart))
    THEN
        SELECT vid INTO vidout FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=a_placekey AND v.week_begin=w_daterangestart);
        INSERT INTO relatedBrands(bid, vid, visit_count, day_week_ind)
            VALUES (bidout, vidout, ak_relatedsameweekbrand_cnt, 'w')
            ON CONFLICT (vid, bid) DO NOTHING;
    END IF;
END;