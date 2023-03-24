CREATE OR ALTER PROCEDURE [dbo].[insertRelatedBrands](
	@vid INT,
	@locid INT,
	@bid_loc INT,
	@ak_al_relatedbrand VARCHAR(max),
	@ak_al_relatedbrand_cnt INT,
    @day_week_ind CHAR(1)
)
AS
BEGIN
DECLARE @bid_rel INT;

BEGIN

	IF EXISTS (SELECT 1 FROM brandsInfo WHERE brand_name = @ak_al_relatedbrand)
		BEGIN
			SET @bid_rel=(SELECT bid FROM brandsInfo WHERE brand_name=@ak_al_relatedbrand);
		END;
	ELSE
		BEGIN
			INSERT INTO brandsInfo(brand_name)
				VALUES (@ak_al_relatedbrand);
			SET @bid_rel=SCOPE_IDENTITY();
		END;

	INSERT INTO relatedBrands(vid, locid, bid_loc, bid_rel, visit_count, day_week_ind)
		VALUES (@vid, @locid, @bid_loc, @bid_rel, @ak_al_relatedbrand_cnt, @day_week_ind);

END;
END;