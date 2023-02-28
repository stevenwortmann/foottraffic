CREATE OR REPLACE PROCEDURE insertFootTrafficRecord(
    a_placekey VARCHAR,
    c_locationname VARCHAR,
    e_brands VARCHAR,
    f_topcategory VARCHAR,
    g_subcategory VARCHAR,
    h_naicscode INT,
    i_latitude FLOAT,
    j_longitude FLOAT,
    k_streetaddress VARCHAR,
    l_city VARCHAR,
    m_region VARCHAR,
    n_postalcode INT,
    p_phonenumber BIGINT,
    w_daterangestart VARCHAR,
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
  IF EXISTS (SELECT 1 FROM naicsCodes WHERE naics_code=h_naicscode)
  THEN
    SELECT nid INTO nidout FROM naicsCodes WHERE naics_code=h_naicscode;
  ELSE
    INSERT INTO naicsCodes (naics_code, top_category, sub_category)
        VALUES (h_naicscode, f_topcategory, g_subcategory);
    SELECT LASTVAL() INTO nidout;
  END IF;

  IF EXISTS (SELECT 1 FROM brandsInfo WHERE brand_name=e_brands)
  THEN
    IF (SELECT nid FROM brandsInfo WHERE brand_name=e_brands) IS NULL
    THEN
      UPDATE brandsInfo SET nid=nidout WHERE brand_name=e_brands;
    END IF;
    SELECT bid INTO bidout FROM brandsInfo WHERE brand_name=e_brands;
  ELSE
    INSERT INTO brandsInfo (nid, brand_name)
        VALUES (nidout, e_brands);
    SELECT LASTVAL() INTO bidout;
  END IF;

  IF EXISTS (SELECT 1 FROM censusBlockGroups WHERE cbg_number=ac_poicbg)
  THEN
    SELECT cbgid INTO cbgidout FROM censusBlockGroups WHERE cbg_number=ac_poicbg;
  ELSE
    INSERT INTO censusBlockGroups (cbg_number)
        VALUES (ac_poicbg);
    SELECT LASTVAL() INTO cbgidout;
  END IF;






  IF EXISTS (SELECT 1 FROM locationInfo WHERE placekey=a_placekey)
  THEN
    SELECT locid INTO locidout FROM locationInfo WHERE placekey=a_placekey;
  ELSE
    INSERT INTO locationInfo (nid, bid, cbgid, placekey, location_name, latitude, longitude, street_address, city, region, postal_code, phone_number)
        VALUES (nidout, bidout, cbgidout, a_placekey, c_locationname, i_latitude, j_longitude, k_streetaddress, l_city, m_region, n_postalcode, p_phonenumber);
    SELECT LASTVAL() INTO locidout;
  END IF;

  IF EXISTS (SELECT 1 FROM visitsInfo WHERE locid=locidout AND week_begin=w_daterangestart)
  THEN
    SELECT vid INTO vidout FROM visitsInfo WHERE (locid=locidout AND week_begin=w_daterangestart);
  ELSE
    INSERT INTO visitsInfo(locid, week_begin, raw_visit_counts, raw_visitor_counts, distance_from_home, median_dwell, normalized_visits_by_state_scaling,
          normalized_visits_by_region_naics_visits, normalized_visits_by_region_naics_visitors, normalized_visits_by_total_visits, normalized_visits_by_total_visitors)
        VALUES (@locidout, @w_daterangestart, @y_rawvisitcounts, @z_rawvisitorcounts, @ah_distancefromhome, @ai_mediumdwell, @an_normvisits_statescaling,
          @ao_normvisits_regionnaicsvisits, @ap_normvisits_regionnaicsvisitors, @aq_normvisits_totalvisits, @ar_normvisits_totalvisitors);
    SELECT LASTVAL() INTO vidout;