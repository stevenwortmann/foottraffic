ALTER PROCEDURE insertCategories(
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
			SET @cidout=(SELECT cid FROM categories WHERE category=@r_categorytag)
		END;
	ELSE
		BEGIN
			INSERT INTO categories(category)
			VALUES (@r_categorytag);
			SET @cidout=(SELECT TOP 1 cid FROM categories ORDER BY cid DESC);
			SET @locidout=(SELECT locid FROM locationInfo WHERE placekey=@a_placekey);
			INSERT INTO categoriesXref(locid, cid)
			VALUES (@locidout, @cidout);
		END;
END;
END;