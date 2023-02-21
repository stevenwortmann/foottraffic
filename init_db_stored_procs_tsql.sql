ALTER PROCEDURE [dbo].[insertFootTrafficRecord](
	@a_placekey VARCHAR(max),
	@c_locationname VARCHAR(max),
	@e_brands VARCHAR(max),
	@f_topcategory VARCHAR(max),
	@g_subcategory VARCHAR(max),
	@h_naicscode INT,
	@i_latitude FLOAT,
	@j_longitude FLOAT,
	@k_streetaddress VARCHAR(max),
	@l_city VARCHAR(max),
	@m_region VARCHAR(max),
	@n_postalcode INT,
	@p_phonenumber BIGINT,
	@w_daterangestart VARCHAR(max),
	@y_rawvisitcounts INT,
	@z_rawvisitorcounts INT,
	@ac_poicbg BIGINT,
	@ah_distancefromhome INT,
	@ai_mediumdwell FLOAT,
	@an_normvisits_statescaling FLOAT,
	@ao_normvisits_regionnaicsvisits FLOAT,
	@ap_normvisits_regionnaicsvisitors FLOAT,
	@aq_normvisits_totalvisits FLOAT,
	@ar_normvisits_totalvisitors FLOAT
)
AS
BEGIN
DECLARE @nidout INT;
DECLARE @bidout INT;
DECLARE @cbgidout INT;
DECLARE @locidout INT;
DECLARE @vidout INT;

  BEGIN

    IF (SELECT COUNT(1) FROM naicsCodes WHERE naics_code=@h_naicscode)=1 
      BEGIN
        SET @nidout=(SELECT nid FROM naicsCodes WHERE naics_code=@h_naicscode);
      END;
    ELSE
      BEGIN
		INSERT INTO naicsCodes(naics_code, top_category, sub_category)
		VALUES (@h_naicscode, @f_topcategory, @g_subcategory);
		SET @nidout=(SELECT TOP 1 nid FROM naicsCodes ORDER BY nid DESC);
      END;

	IF (SELECT COUNT(1) FROM brandsInfo WHERE brand_name=@e_brands)=1
		BEGIN
			IF (SELECT nid FROM brandsInfo WHERE brand_name=@e_brands) IS NULL
				BEGIN
					UPDATE brandsInfo SET nid=@nidout WHERE brand_name=@e_brands;
				END;
			SET @bidout=(SELECT bid FROM brandsInfo WHERE brand_name=@e_brands);
		END;
	ELSE
		BEGIN
			INSERT INTO brandsInfo(nid, brand_name)
			VALUES (@nidout, @e_brands);
			SET @bidout=(SELECT TOP 1 bid FROM brandsInfo ORDER BY bid DESC);
		END;

    IF (SELECT COUNT(1) FROM censusBlockGroups WHERE cbg_number=@ac_poicbg)=1
      BEGIN
		    SET @cbgidout=(SELECT cbgid FROM censusBlockGroups WHERE cbg_number=@ac_poicbg);
      END;

    ELSE
      BEGIN
        INSERT INTO censusBlockGroups(cbg_number)
        VALUES (@ac_poicbg);
		    SET @cbgidout=(SELECT TOP 1 cbgid FROM censusBlockGroups ORDER BY cbgid DESC);
      END;

    IF (SELECT COUNT(1) FROM locationInfo WHERE placekey=@a_placekey)=1
      BEGIN
		    SET @locidout=(SELECT locid FROM locationInfo WHERE placekey=@a_placekey);
      END;
    ELSE
      BEGIN
        INSERT INTO locationInfo(nid, bid, cbgid, placekey, location_name, latitude, longitude, street_address, city, region, postal_code, phone_number)
        VALUES (@nidout, @bidout, @cbgidout, @a_placekey, @c_locationname, @i_latitude, @j_longitude, @k_streetaddress, @l_city, @m_region, @n_postalcode, @p_phonenumber);
		    SET @locidout=(SELECT TOP 1 locid FROM locationInfo ORDER BY locid DESC);
      END;

    IF (SELECT COUNT(1) FROM visitsInfo WHERE (locid=@locidout AND week_begin=@w_daterangestart))=1 
      BEGIN
		    SET @vidout=(SELECT vid FROM visitsInfo WHERE (locid=@locidout AND week_begin=@w_daterangestart));
      END;
    ELSE
      BEGIN
        INSERT INTO visitsInfo(locid, week_begin, raw_visit_counts, raw_visitor_counts, distance_from_home, median_dwell, normalized_visits_by_state_scaling,
          normalized_visits_by_region_naics_visits, normalized_visits_by_region_naics_visitors, normalized_visits_by_total_visits, normalized_visits_by_total_visitors)
        VALUES (@locidout, @w_daterangestart, @y_rawvisitcounts, @z_rawvisitorcounts, @ah_distancefromhome, @ai_mediumdwell, @an_normvisits_statescaling,
          @ao_normvisits_regionnaicsvisits, @ap_normvisits_regionnaicsvisitors, @aq_normvisits_totalvisits, @ar_normvisits_totalvisitors);
		    SET @vidout=(SELECT TOP 1 vid FROM visitsInfo ORDER BY vid DESC);
      END;
    END;
END;

----------------------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------------------

ALTER PROCEDURE [dbo].[insertCategories](
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

----------------------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------------------

ALTER PROCEDURE [dbo].[insertDeviceCount]( -- 'device_name' field fully populated with init_db_tables
	@a_placekey VARCHAR(max),
	@w_daterangestart VARCHAR(max),
	@am_devicetype VARCHAR(max),
	@am_devicetype_cnt INT
)
AS
BEGIN
DECLARE @didout INT;
DECLARE @vidout INT;

BEGIN

  IF (SELECT COUNT(1) FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart))=1 
    BEGIN
		SET @vidout = (SELECT vid FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart));	
		SET @didout = (SELECT did FROM devices WHERE (device_name=@am_devicetype));
        INSERT INTO deviceLog(did, vid, user_count)
        VALUES (@didout, @vidout, @am_devicetype_cnt);
    END;
END;
END;

----------------------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------------------

ALTER PROCEDURE [dbo].[insertHomeVisits](
  @a_placekey VARCHAR(max),
  @w_daterangestart VARCHAR(max),
  @ad_visitorhomecbg VARCHAR(max),
  @ad_visitorhomecbg_cnt INT
)
AS
BEGIN
DECLARE @vidout INT;
DECLARE @cbgidout INT;
DECLARE @locidout INT;

BEGIN

  SET @locidout=(SELECT locid FROM locationInfo WHERE placekey=@a_placekey) 

  IF (SELECT COUNT(1) FROM censusBlockGroups WHERE cbg_number=@ad_visitorhomecbg)=1
    BEGIN
      SET @cbgidout=(SELECT cbgid FROM censusBlockGroups WHERE cbg_number=@ad_visitorhomecbg);
    END;

  ELSE
    BEGIN
      INSERT INTO censusBlockGroups(cbg_number)
      VALUES (@ad_visitorhomecbg);
      SET @cbgidout=(SELECT TOP 1 cbgid FROM censusBlockGroups ORDER BY cbgid DESC);
    END;

  IF (SELECT COUNT(1) FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart))=1 
    BEGIN
        SET @vidout = (SELECT TOP 1 vid FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart) ORDER BY vid DESC);	
        INSERT INTO homeVisits(locid, vid, cbgid, visit_count)
        VALUES (@locidout, @vidout, @cbgidout, @ad_visitorhomecbg_cnt);
    END;
END;
END;

----------------------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------------------

ALTER PROCEDURE [dbo].[insertWorkVisits](
	@a_placekey VARCHAR(max),
	@w_daterangestart VARCHAR(max),
	@af_visitordaytimecbg BIGINT,
	@af_visitordaytimecbg_cnt INT
)
AS
BEGIN
DECLARE @vidout INT;
DECLARE @cbgidout INT;
DECLARE @locidout INT;

BEGIN

  SET @locidout=(SELECT locid FROM locationInfo WHERE placekey=@a_placekey) 

  IF (SELECT COUNT(1) FROM censusBlockGroups WHERE cbg_number=@af_visitordaytimecbg)=1
    BEGIN
      SET @cbgidout=(SELECT cbgid FROM censusBlockGroups WHERE cbg_number=@af_visitordaytimecbg);
    END;

  ELSE
    BEGIN
      INSERT INTO censusBlockGroups(cbg_number)
      VALUES (@af_visitordaytimecbg);
      SET @cbgidout=(SELECT TOP 1 cbgid FROM censusBlockGroups ORDER BY cbgid DESC);
    END;

  IF (SELECT COUNT(1) FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart))=1 
    BEGIN
		SET @vidout = (SELECT TOP 1 vid FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart) ORDER BY vid DESC);	
        INSERT INTO workVisits(locid, vid, cbgid, visit_count)
        VALUES (@locidout, @vidout, @cbgidout, @af_visitordaytimecbg_cnt);
    END;
END;
END;

----------------------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------------------

ALTER PROCEDURE [dbo].[insertBrandsWeek](
	@a_placekey VARCHAR(max),
	@w_daterangestart VARCHAR(max),
	@al_relatedsameweekbrand VARCHAR(max),
	@al_relatedsameweekbrand_cnt INT
)
AS
BEGIN
DECLARE @vidout INT;
DECLARE @bidout INT;
DECLARE @locidout INT;

BEGIN

	IF (SELECT COUNT(1) FROM brandsInfo WHERE brand_name=@al_relatedsameweekbrand)=1
		BEGIN
			SET @bidout=(SELECT bid FROM brandsInfo WHERE brand_name=@al_relatedsameweekbrand);
		END;
	ELSE
		BEGIN
			INSERT INTO brandsInfo(brand_name)
			VALUES (@al_relatedsameweekbrand);
			SET @bidout=(SELECT TOP 1 bid FROM brandsInfo ORDER BY bid DESC);
		END;


	IF (SELECT COUNT(1) FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart))=1 
	BEGIN
		SET @vidout = (SELECT TOP 1 vid FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart));
		SET @locidout = (SELECT TOP 1 locid FROM locationInfo l WHERE l.placekey=@a_placekey);		
		INSERT INTO brandsWeek(vid, bid, locid, visit_count)
		VALUES (@vidout, @bidout, @locidout, @al_relatedsameweekbrand_cnt);
	END;
END;
END;

----------------------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------------------

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
		INSERT INTO brandsDay(vid, bid, locid, visit_count)
		VALUES (@vidout, @bidout, @locidout, @ak_relatedsamedaybrand_cnt);
	END;
END;
END;