CREATE PROCEDURE insertFootTrafficRecord(
	@a_placekey VARCHAR(max),
	@c_locationname VARCHAR(max),
	@e_brands VARCHAR(max),
	@f_topcategory VARCHAR(max),
	@g_subcategory VARCHAR(max),
	@h_naicscode VARCHAR(max),
	@i_latitude FLOAT,
	@j_longitude FLOAT,
	@k_streetaddress VARCHAR(max),
	@l_city VARCHAR(max),
	@m_region VARCHAR(max),
	@n_postalcode VARCHAR(max),
	@p_phonenumber VARCHAR(max),
	@r_categorytag VARCHAR(max),
	@w_daterangestart VARCHAR(max),
	@y_rawvisitcounts INT,
	@z_rawvisitorcounts INT,
	@ac_poicbg VARCHAR(max),
	@ad_visitorhomecbg VARCHAR(max),
	@ad_visitorhomecbg_cnt INT,
	@af_visitordaytimecbg VARCHAR(max),
	@af_visitordaytimecbg_cnt INT,
	@ah_distancefromhome INT,
	@ai_mediumdwell FLOAT,
	@ak_relatedsamedaybrand VARCHAR(max),
	@ak_relatedsamedaybrand_cnt INT,
	@al_relatedsameweekbrand VARCHAR(max),
	@al_relatedsameweekbrand_cnt INT,
	@am_devicetype VARCHAR(max),
	@am_devicetype_cnt INT,
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
		  SELECT nid INTO nidout FROM naicsCodes WHERE naics_code=@h_naicscode;
		END
	ELSE
		BEGIN
			INSERT INTO naicsCodes(naics_code, top_category, sub_category)
			VALUES (@h_naicscode, @f_topcategory, @g_subcategory);
			SELECT @nidout = LAST_VALUE(nid) OVER (ORDER BY nid) FROM naicsCodes;
		END
    END;


    IF (SELECT COUNT(1) FROM brandsInfo WHERE brand_name=@e_brands)=1 --filter out nulls in python
		BEGIN
			SELECT bid INTO bidout FROM brandsInfo WHERE brand_name=@e_brands;
		END
    ELSE
		BEGIN
			INSERT INTO brandsInfo(nid, brand_name)
			VALUES (@nidout, @e_brands);
			SELECT @bidout = LAST_VALUE(bid) OVER (ORDER BY bid) FROM brandsInfo;
		END
    END;

	IF (SELECT COUNT(1) FROM censusBlockGroups WHERE cbg_number=@ac_poicbg)=1
		BEGIN
			SELECT cbgid INTO cbgidout FROM censusBlockGroups WHERE cbg_number=@ac_poicbg;
		END
    ELSE
		BEGIN
			INSERT INTO censusBlockGroups(cbg_number)
			VALUES (@ac_poicbg);
			SELECT @cbgidout = LAST_VALUE(cbgid) OVER (ORDER BY cbgid) FROM censusBlockGroups;
		END
    END;

	IF (SELECT COUNT(1) FROM locationInfo WHERE placekey=@a_placekey)=1
		BEGIN
			SELECT locid INTO locidout FROM locationInfo WHERE placekey=@a_placekey;
		END
	ELSE
		BEGIN
			INSERT INTO locationInfo(nid, bid, cbgid, placekey, location_name, latitude, longitude, street_address, city, region, phone_number)
			VALUES (@nidout, @bidout, @cbgidout, @a_placekey, @i_latitude, @j_longitude, @k_streetaddress, @l_city, @m_region, @n_postalcode, @p_phonenumber);
			SELECT @locidout = LAST_VALUE(locid) OVER (ORDER BY locid) FROM locationInfo;
		END
	END;

	IF (SELECT COUNT(1) FROM visitsInfo WHERE (locid=@locidout AND week_begin=@w_daterangestart))=1 
		BEGIN
			SELECT vid INTO vidout FROM visitsInfo WHERE (locid=@locidout AND week_begin=@w_daterangestart)
		END
	ELSE
		BEGIN
			INSERT INTO visitsInfo(locid, week_begin, raw_visit_counts, raw_visitor_counts, distance_from_home, median_dwell, normalized_visits_by_state_scaling,
				normalized_visits_by_region_naics_visits, normalized_visits_by_region_naics_visitors, normalized_visits_by_total_visits, normalized_visits_by_total_visitors)
			VALUES (@locidout, @w_daterangestart, @y_rawvisitcounts, @z_rawvisitorcounts, @ah_distancefromhome, @ai_mediumdwell, @an_normvisits_statescaling,
				@ao_normvisits_regionnaicsvisits, @ap_normvisits_regionnaicsvisitors, @aq_normvisits_totalvisits, @ar_normvisits_totalvisitors);
			SELECT @vidout = LAST_VALUE(vid) OVER (ORDER BY vid) FROM visitsInfo;
		END
	END
END;

----------------------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------------------

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

----------------------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------------------

CREATE PROCEDURE insertDeviceCounts( -- 'device_name' field fully populated with init_db_tables
	@a_placekey VARCHAR(max),
	@w_daterangestart VARCHAR(max),
	@am_devicetype VARCHAR(max),
	@am_devicetype_cnt INT,
)
AS
BEGIN
DECLARE @didout INT;
DECLARE @vidout INT;

BEGIN

  IF (SELECT COUNT(1) FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart))=1 
    BEGIN
		SELECT @vidout = LAST_VALUE(vid) OVER (ORDER BY vid) FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart);
		SELECT @didout = LAST_VALUE(did) OVER (ORDER BY did) FROM devices WHERE (device_name=@am_devicetype);
        INSERT INTO deviceLog(did, vid, user_count)
        VALUES (@didout, @vidout, @am_devicetype_cnt);
    END;
END;

----------------------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------------------

CREATE PROCEDURE insertHomeVisits(
  @a_placekey VARCHAR(max),
  @w_daterangestart VARCHAR(max),
  @ad_visitorhomecbg VARCHAR(max),
  @ad_visitorhomecbg_cnt INT,
)
AS
BEGIN
DECLARE @vidout INT;
DECLARE @cbgidout INT;

BEGIN

  IF (SELECT COUNT(1) FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart))=1 
    BEGIN
		SELECT @vidout = LAST_VALUE(vid) OVER (ORDER BY vid) FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart);
		SELECT @cbgidout = LAST_VALUE(cbgid) OVER (ORDER BY cbgid) FROM censusBlockGroups WHERE (cbg_number=@ad_visitorhomecbg);
        INSERT INTO homeVisits(vid, cbgid, visit_count)
        VALUES (@vidout, @cbgidout, @ad_visitorhomecbg_cnt);
    END;
END;

----------------------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------------------

CREATE PROCEDURE insertWorkVisits(
	@a_placekey VARCHAR(max),
	@w_daterangestart VARCHAR(max),
	@af_visitordaytimecbg VARCHAR(max),
	@af_visitordaytimecbg_cnt INT,
)
AS
BEGIN
DECLARE @vidout INT;
DECLARE @cbgidout INT;

BEGIN

  IF (SELECT COUNT(1) FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart))=1 
    BEGIN
		SELECT @vidout = LAST_VALUE(vid) OVER (ORDER BY vid) FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart);
		SELECT @cbgidout = LAST_VALUE(cbgid) OVER (ORDER BY cbgid) FROM censusBlockGroups WHERE (cbg_number=@af_visitordaytimecbg);
        INSERT INTO homeVisits(vid, cbgid, visit_count)
        VALUES (@vidout, @cbgidout, @af_visitordaytimecbg_cnt);
    END;
END;

----------------------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------------------

CREATE PROCEDURE insertBrandsWeek(
	@a_placekey VARCHAR(max),
	@w_daterangestart VARCHAR(max),
	@al_relatedsameweekbrand VARCHAR(max),
	@al_relatedsameweekbrand_cnt INT,
)
AS
BEGIN
DECLARE @vidout INT;
DECLARE @bidout INT;

BEGIN

  IF (SELECT COUNT(1) FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart))=1 
    BEGIN
        SELECT @vidout = LAST_VALUE(vid) OVER (ORDER BY vid) FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart);
		SELECT @bidout = LAST_VALUE(bid) OVER (ORDER BY bid) FROM brandsInfo WHERE (brand_name=@al_relatedsameweekbrand);
        INSERT INTO brandsWeek(vid, bid, visit_count)
        VALUES (@vidout, @bidout, @al_relatedsameweekbrand_cnt);
    END;
END;

----------------------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------------------

CREATE PROCEDURE insertBrandsDay(
	@a_placekey VARCHAR(max),
	@w_daterangestart VARCHAR(max),
	@ak_relatedsamedaybrand VARCHAR(max),
	@ak_relatedsamedaybrand_cnt INT,
)
AS
BEGIN
DECLARE @vidout INT;
DECLARE @bidout INT;

BEGIN

  IF (SELECT COUNT(1) FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart))=1 
    BEGIN
        SELECT @vidout = LAST_VALUE(vid) OVER (ORDER BY vid) FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart);
		SELECT @bidout = LAST_VALUE(bid) OVER (ORDER BY bid) FROM brandsInfo WHERE (brand_name=@ak_relatedsamedaybrand);
        INSERT INTO brandsDay(vid, bid, visit_count)
        VALUES (@vidout, @bidout, @ak_relatedsamedaybrand_cnt);
    END;
END;