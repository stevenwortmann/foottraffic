CREATE OR REPLACE PROCEDURE insertCategories(
	a_placekey character varying,
	r_categorytag character varying
)
LANGUAGE plpgsql
AS $$
DECLARE
	locidout INT;
	cidout INT;
BEGIN

	IF EXISTS (SELECT COUNT(1) FROM categories WHERE (category=r_categorytag)) THEN
		SELECT cid INTO cidout FROM categories WHERE category=r_categorytag;
	ELSE
		INSERT INTO categories(category)
		    VALUES (r_categorytag);
        SELECT LASTVAL() INTO cidout;
		SELECT locid INTO locidout FROM locationInfo WHERE placekey=a_placekey;
		INSERT INTO categoriesXref(locid, cid)
		    VALUES (locidout, cidout);
	END IF;
END;