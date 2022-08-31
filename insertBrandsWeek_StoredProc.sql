CREATE PROCEDURE insertBrandsWeek(
  a_placekey VARCHAR(max),
  w_daterangestart VARCHAR(max),
  al_relatedsameweekbrand VARCHAR(max),
  al_relatedsameweekbrand_cnt INT,
)
AS $$
DECLARE @vidout INT;
DECLARE @bidout INT;

BEGIN

  IF (SELECT COUNT(1) FROM visitsInfo WHERE (placekey=a_placekey AND week_begin=w_daterangestart))=1 
    BEGIN
        SELECT vid INTO @vidout FROM visitsInfo WHERE (placekey=a_placekey AND week_begin=w_daterangestart)
        SELECT bid INTO @bidout FROM brandsInfo WHERE (brand_name=al_relatedsameweekbrand)
        INSERT INTO brandsWeek(vid, bid, visit_count)
        VALUES (@vidout, @bidout, al_relatedsameweekbrand_cnt);
    END IF;
END;