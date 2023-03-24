ALTER PROCEDURE [dbo].[insertCategories](
	@locid INT,
	@r_categorytag VARCHAR(max)
)
AS
BEGIN
DECLARE @cidout INT;

BEGIN

	IF EXISTS (SELECT 1 FROM categories WHERE (category=@r_categorytag))
		BEGIN
			SET @cidout=(SELECT cid FROM categories WHERE category=@r_categorytag);
		END;
	ELSE
		BEGIN
			INSERT INTO categories(category)
				VALUES (@r_categorytag);
			SET @cidout=SCOPE_IDENTITY();
			INSERT INTO categoriesXref(locid, cid)
				VALUES (@locid, @cidout);
		END;
END;
END;