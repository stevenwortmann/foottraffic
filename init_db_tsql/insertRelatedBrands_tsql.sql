CREATE OR ALTER PROCEDURE [dbo].[insertRelatedBrands](
	@a_placekey VARCHAR(max),
	@w_daterangestart VARCHAR(max),
	@ak_al_relatedbrand VARCHAR(max),
	@ak_al_relatedbrand_cnt INT,
	@day_week_ind CHAR(1)
)
AS
BEGIN

DECLARE @vidout INT;
DECLARE @bidout INT;
DECLARE @locidout INT;

BEGIN
	IF (SELECT COUNT(1) FROM brandsInfo WHERE brand_name=@ak_al_relatedbrand)=1
		BEGIN
			SET @bidout=(SELECT bid FROM brandsInfo WHERE brand_name=@ak_al_relatedbrand);
		END;
	ELSE
		BEGIN
			INSERT INTO brandsInfo(brand_name)
			VALUES (@ak_al_relatedbrand);
			SET @bidout=(SELECT TOP 1 bid FROM brandsInfo ORDER BY bid DESC);
		END;

	IF (SELECT COUNT(1) FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart))=1 
	BEGIN
		SET @vidout = (SELECT TOP 1 vid FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart));
		SET @locidout = (SELECT TOP 1 locid FROM locationInfo WHERE placekey=@a_placekey);
		-- Check if day_week_ind is 'd' for 'same-day'
		IF @day_week_ind = 'd'
		BEGIN
			INSERT INTO relatedBrands(bid, vid, locid, visit_count, day_week_ind)
			VALUES (@bidout, @vidout, @locidout, @ak_al_relatedbrand_cnt, 'd');
		END;
		-- Check if day_week_ind is 'w' for 'same-week'
		ELSE IF @day_week_ind = 'w'
		BEGIN
			INSERT INTO relatedBrands(bid, vid, locid, visit_count, day_week_ind)
			VALUES (@bidout, @vidout, @locidout, @ak_al_relatedbrand_cnt, 'w');
		END;
	END;
END;

END;