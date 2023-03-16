ALTER PROCEDURE [dbo].[insertBrandsDay](
	@a_placekey VARCHAR(max),
	@w_daterangestart VARCHAR(max),
	@ak_relatedsamedaybrand VARCHAR(max),
	@ak_relatedsamedaybrand_cnt INT
)
AS
BEGIN
DECLARE @vidout INT;
DECLARE @bidout INT;
DECLARE @locidout INT;

BEGIN

	IF (SELECT COUNT(1) FROM brandsInfo WHERE brand_name=@ak_relatedsamedaybrand)=1
		BEGIN
			SET @bidout=(SELECT bid FROM brandsInfo WHERE brand_name=@ak_relatedsamedaybrand);
		END;
	ELSE
		BEGIN
			INSERT INTO brandsInfo(brand_name)
			VALUES (@ak_relatedsamedaybrand);
			SET @bidout=(SELECT TOP 1 bid FROM brandsInfo ORDER BY bid DESC);
		END;


	IF (SELECT COUNT(1) FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart))=1 
	BEGIN
		SET @vidout = (SELECT vid FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart));
		SET @locidout = (SELECT locid FROM locationInfo WHERE placekey=@a_placekey);			
		INSERT INTO relatedBrands(bid, vid, locid, visit_count, day_week_ind)
		VALUES (@bidout, @vidout, @locidout, @ak_relatedsamedaybrand_cnt, 'd');
	END;
END;
END;