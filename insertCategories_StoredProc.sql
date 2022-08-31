CREATE PROCEDURE insertCategories(
  a_placekey VARCHAR(max),
  r_categorytag VARCHAR(max),
)
AS $$
DECLARE @locidout INT;
DECLARE @cidout INT;

BEGIN

  IF (SELECT COUNT(1) FROM categories WHERE (category=r_categorytag))=1 
    BEGIN
        SELECT cid INTO @cidout FROM categories WHERE (category=r_categorytag)
    END
    ELSE
        INSERT INTO categories(category)
        VALUES (r_categorytag)
        SELECT LAST_VALUE(cid) INTO @cidout;
        SELECT loccid INTO @locidout FROM locationInfo WHERE (placekey=a_placekey)
        INSERT INTO categoriesXref(locid, cid)
        VALUES (@locidout, @cidout);
      END IF;
END;