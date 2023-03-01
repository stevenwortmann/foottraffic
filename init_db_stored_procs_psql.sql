CREATE OR REPLACE PROCEDURE insertBrandsDay(
    a_placekey VARCHAR,
    w_daterangestart DATE,
    ak_relatedsamedaybrand VARCHAR,
    ak_relatedsamedaybrand_cnt INT,
    day_week_ind CHAR
)

LANGUAGE plpgsql
AS $$

DECLARE 
    vidout INT;
    bidout INT;
    locidout INT;

BEGIN
    IF EXISTS (SELECT 1 FROM brandsInfo WHERE brand_name=ak_relatedsamedaybrand)
    THEN
        SELECT bid INTO bidout FROM brandsInfo WHERE brand_name = ak_relatedsamedaybrand;
    ELSE
        INSERT INTO brandsInfo (brand_name)
            VALUES (ak_relatedsamedaybrand)
        SELECT LASTVAL() INTO bidout;
    END IF;

    IF EXISTS (SELECT 1 FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=a_placekey AND v.week_begin=w_daterangestart))
    THEN
        SELECT vid INTO vidout FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=a_placekey AND v.week_begin=w_daterangestart);
        INSERT INTO relatedBrands(bid, vid, visit_count, day_week_ind)
            VALUES (bidout, vidout, ak_relatedsamedaybrand_cnt, 'd')
            ON CONFLICT (vid, bid) DO NOTHING;
    END IF;
END;


CREATE OR REPLACE PROCEDURE insertBrandsWeek(
    a_placekey VARCHAR,
    w_daterangestart VARCHAR,
    ak_relatedsameweekbrand VARCHAR,
    ak_relatedsameweekbrand_cnt INT,
    day_week_ind CHAR
)

LANGUAGE plpgsql
AS $$

DECLARE 
    vidout INT;
    bidout INT;

BEGIN
    IF EXISTS (SELECT 1 FROM brandsInfo WHERE brand_name=ak_relatedsameweekbrand)
    THEN
        SELECT bid INTO bidout FROM brandsInfo WHERE brand_name = ak_relatedsameweekbrand;
    ELSE
        INSERT INTO brandsInfo (brand_name)
            VALUES (ak_relatedsameweekbrand)
        SELECT LASTVAL() INTO bidout;
    END IF;

    IF EXISTS (SELECT 1 FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=a_placekey AND v.week_begin=w_daterangestart))
    THEN
        SELECT vid INTO vidout FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=a_placekey AND v.week_begin=w_daterangestart);
        INSERT INTO relatedBrands(bid, vid, visit_count, day_week_ind)
            VALUES (bidout, vidout, ak_relatedsameweekbrand_cnt, 'w')
            ON CONFLICT (vid, bid) DO NOTHING;
    END IF;
END;


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
CREATE OR REPLACE PROCEDURE insertDeviceCount( -- 'device_name' field fully populated with init_db_tables
	 a_placekey VARCHAR,
	 w_daterangestart VARCHAR,
	 am_devicetype VARCHAR,
	 am_devicetype_cnt INT
)
AS 
$$
DECLARE didout INT;
DECLARE vidout INT;

BEGIN

  IF (SELECT 1 FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=a_placekey AND v.week_begin=w_daterangestart))
    THEN
        SELECT vid INTO vidout FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=a_placekey AND v.week_begin=w_daterangestart);
        SELECT did INTO didout FROM devices WHERE (device_name=am_devicetype);
        INSERT INTO deviceLog(did, vid, user_count)
            VALUES (didout, vidout, am_devicetype_cnt);
    END IF;
END;


CREATE OR REPLACE PROCEDURE insertFootTrafficRecord(
    a_placekey VARCHAR(20),
    c_locationname VARCHAR(100),
    e_brands VARCHAR(100),
    f_topcategory VARCHAR(100),
    g_subcategory VARCHAR(100),
    h_naicscode INT,
    i_latitude FLOAT,
    j_longitude FLOAT,
    k_streetaddress VARCHAR(100),
    l_city VARCHAR(50),
    m_region VARCHAR(5),
    n_postalcode INT,
    p_phonenumber BIGINT,
    w_daterangestart DATE,
    y_rawvisitcounts INT,
    z_rawvisitorcounts INT,
    ac_poicbg BIGINT,
    ah_distancefromhome INT,
    ai_mediumdwell FLOAT,
    an_normvisits_statescaling FLOAT,
    ao_normvisits_regionnaicsvisits FLOAT,
    ap_normvisits_regionnaicsvisitors FLOAT,
    aq_normvisits_totalvisits FLOAT,
    ar_normvisits_totalvisitors FLOAT
)

LANGUAGE plpgsql
AS $$

DECLARE
  nidout INT;
  bidout INT;
  cbgidout INT;
  locidout INT;
  vidout INT;

BEGIN
  IF EXISTS (SELECT 1 FROM naicsCodes WHERE naics_code=h_naicscode) THEN
    SELECT nid INTO nidout FROM naicsCodes WHERE naics_code=h_naicscode;
  ELSE
    INSERT INTO naicsCodes (naics_code, top_category, sub_category)
        VALUES (h_naicscode, f_topcategory, g_subcategory);
    SELECT LASTVAL() INTO nidout;
  END IF;

  IF EXISTS (SELECT 1 FROM brandsInfo WHERE brand_name=e_brands) THEN
    IF (SELECT nid FROM brandsInfo WHERE brand_name=e_brands) IS NULL THEN
      UPDATE brandsInfo SET nid=nidout WHERE brand_name=e_brands;
    END IF;
    SELECT bid INTO bidout FROM brandsInfo WHERE brand_name=e_brands;
  ELSE
    INSERT INTO brandsInfo (nid, brand_name)
        VALUES (nidout, e_brands);
    SELECT LASTVAL() INTO bidout;
  END IF;

  IF EXISTS (SELECT 1 FROM censusBlockGroups WHERE cbg_number=ac_poicbg) THEN
    SELECT cbgid INTO cbgidout FROM censusBlockGroups WHERE cbg_number=ac_poicbg;
  ELSE
    INSERT INTO censusBlockGroups (cbg_number)
        VALUES (ac_poicbg);
    SELECT LASTVAL() INTO cbgidout;
  END IF;

  IF EXISTS (SELECT 1 FROM locationInfo WHERE placekey=a_placekey) THEN
    SELECT locid INTO locidout FROM locationInfo WHERE placekey=a_placekey;
  ELSE
    INSERT INTO locationInfo (nid, bid, cbgid, placekey, location_name, latitude, longitude, street_address, city, region, postal_code, phone_number)
        VALUES (nidout, bidout, cbgidout, a_placekey, c_locationname, i_latitude, j_longitude, k_streetaddress, l_city, m_region, n_postalcode, p_phonenumber);
    SELECT LASTVAL() INTO locidout;
  END IF;

  IF EXISTS (SELECT 1 FROM visitsInfo WHERE locid=locidout AND week_begin=w_daterangestart) THEN
    SELECT vid INTO vidout FROM visitsInfo WHERE (locid=locidout AND week_begin=w_daterangestart);
  ELSE
    INSERT INTO visitsInfo(locid, week_begin, raw_visit_counts, raw_visitor_counts, distance_from_home, median_dwell, normalized_visits_by_state_scaling,
          normalized_visits_by_region_naics_visits, normalized_visits_by_region_naics_visitors, normalized_visits_by_total_visits, normalized_visits_by_total_visitors)
        VALUES (locidout, w_daterangestart, y_rawvisitcounts, z_rawvisitorcounts, ah_distancefromhome, ai_mediumdwell, an_normvisits_statescaling,
          ao_normvisits_regionnaicsvisits, ap_normvisits_regionnaicsvisitors, aq_normvisits_totalvisits, ar_normvisits_totalvisitors);
    SELECT LASTVAL() INTO vidout;


CREATE OR REPLACE PROCEDURE insertHomeVisits(
  a_placekey VARCHAR,
  w_daterangestart DATE,
  ad_visitorhomecbg VARCHAR,
  ad_visitorhomecbg_cnt INT
)
AS $$
DECLARE vidout INT;
DECLARE cbgidout INT;
DECLARE locidout INT;
BEGIN
  SELECT locid INTO locidout FROM locationInfo WHERE placekey=a_placekey;

  IF EXISTS (SELECT 1 FROM censusBlockGroups WHERE cbg_number=ad_visitorhomecbg) THEN
    SELECT cbgid INTO cbgidout FROM censusBlockGroups WHERE cbg_number=ad_visitorhomecbg;
  ELSE
    INSERT INTO censusBlockGroups(cbg_number)
        VALUES (ad_visitorhomecbg);
    SELECT LASTVAL() INTO cbgidout;
  END IF;

  IF EXISTS (SELECT 1 FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=a_placekey AND v.week_begin=w_daterangestart)) THEN
    SELECT vid INTO vidout FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=a_placekey AND v.week_begin=w_daterangestart);
    INSERT INTO visitsType(locid, vid, cbgid, visit_count, home_work_ind)
        VALUES (locidout, vidout, cbgidout, ad_visitorhomecbg_cnt, 'h');
  END IF;
END;


CREATE OR REPLACE PROCEDURE insertHomeVisits(
  a_placekey VARCHAR,
  w_daterangestart DATE,
  ad_visitordaytimecbg VARCHAR,
  ad_visitordaytimecbg_cnt INT
)
AS $$
DECLARE vidout INT;
DECLARE cbgidout INT;
DECLARE locidout INT;
BEGIN
  SELECT locid INTO locidout FROM locationInfo WHERE placekey=a_placekey;

  IF EXISTS (SELECT 1 FROM censusBlockGroups WHERE cbg_number=ad_visitordaytimecbg) THEN
    SELECT cbgid INTO cbgidout FROM censusBlockGroups WHERE cbg_number=ad_visitordaytimecbg;
  ELSE
    INSERT INTO censusBlockGroups(cbg_number)
        VALUES (ad_visitordaytimecbg);
    SELECT LASTVAL() INTO cbgidout;
  END IF;

  IF EXISTS (SELECT 1 FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=a_placekey AND v.week_begin=w_daterangestart)) THEN
    SELECT vid INTO vidout FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=a_placekey AND v.week_begin=w_daterangestart);
    INSERT INTO visitsType(locid, vid, cbgid, visit_count, home_work_ind)
        VALUES (locidout, vidout, cbgidout, ad_visitordaytimecbg_cnt, 'w');
  END IF;
END;
