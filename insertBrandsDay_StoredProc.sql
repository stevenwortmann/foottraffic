CREATE PROCEDURE insertBrandsDay(
  a_placekey VARCHAR(max),
  w_daterangestart VARCHAR(max),
  ak_relatedsamedaybrand VARCHAR(max),
  ak_relatedsamedaybrand_cnt INT,
)
AS $$
DECLARE @vidout INT;
DECLARE @bidout INT;

BEGIN

  IF (SELECT COUNT(1) FROM visitsInfo WHERE (placekey=a_placekey AND week_begin=w_daterangestart))=1 
    BEGIN
        SELECT vid INTO @vidout FROM visitsInfo WHERE (placekey=a_placekey AND week_begin=w_daterangestart)
        SELECT bid INTO @bidout FROM brandsInfo WHERE (brand_name=ak_relatedsamedaybrand)
        INSERT INTO brandsDay(vid, bid, visit_count)
        VALUES (@vidout, @bidout, ak_relatedsamedaybrand_cnt);
    END IF;
END;