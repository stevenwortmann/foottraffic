CREATE PROCEDURE insertCategories(
	@a_placekey VARCHAR(max),
	@r_categorytag VARCHAR(max)
)
AS
BEGIN
DECLARE @locidout INT;
DECLARE @cidout INT;

BEGIN

	IF (SELECT COUNT(1) FROM categories WHERE (category=@r_categorytag))=1 
		BEGIN
			SELECT cid INTO cidout FROM categories WHERE (category=@r_categorytag)
		END
	ELSE
		BEGIN
			INSERT INTO categories(category)
			VALUES (@r_categorytag)
			SELECT @cidout = LAST_VALUE(cid) OVER (ORDER BY cid) FROM categories;
			SELECT @locidout = LAST_VALUE(locid) OVER (ORDER BY locid) FROM locationInfo;
			INSERT INTO categoriesXref(locid, cid)
			VALUES (@locidout, @cidout);
		END
END;