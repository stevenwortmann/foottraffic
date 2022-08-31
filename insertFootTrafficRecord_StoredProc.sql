CREATE PROCEDURE insertFootTrafficRecord(
  a_placekey VARCHAR(max),
  c_locationname VARCHAR(max),
  e_brands VARCHAR(max),
  f_topcategory VARCHAR(max),
  g_subcategory VARCHAR(max),
  h_naicscode VARCHAR(max),
  i_latitude FLOAT,
  j_longitude FLOAT,
  k_streetaddress VARCHAR(max),
  l_city VARCHAR(max),
  m_region VARCHAR(max),
  n_postalcode VARCHAR(max),
  p_phonenumber VARCHAR(max),
  r_categorytag VARCHAR(max),
  w_daterangestart VARCHAR(max),
  y_rawvisitcounts INT,
  z_rawvisitorcounts INT,
  ac_poicbg VARCHAR(max),
  ad_visitorhomecbg VARCHAR(max),
  ad_visitorhomecbg_cnt INT,
  af_visitordaytimecbg VARCHAR(max),
  af_visitordaytimecbg_cnt INT,
  ah_distancefromhome INT,
  ai_mediumdwell FLOAT,
  ak_relatedsamedaybrand VARCHAR(max),
  ak_relatedsamedaybrand_cnt INT,
  al_relatedsameweekbrand VARCHAR(max),
  al_relatedsameweekbrand_cnt INT,
  am_devicetype VARCHAR(max),
  am_devicetype_cnt INT,
  an_normvisits_statescaling FLOAT,
  ao_normvisits_regionnaicsvisits FLOAT,
  ap_normvisits_totalvisits FLOAT,
  aq_normvisits_totalvisits FLOAT,
  ar_normvisits_totalvisitors FLOAT
)
AS $$
DECLARE @nidout INT;
DECLARE @bidout INT;
DECLARE @cbgidout INT;
DECLARE @locidout INT;
DECLARE @vidout INT;

BEGIN

  IF (SELECT COUNT(1) FROM naicsCodes WHERE naics_code=h_naicscode)=1 THEN
      SELECT nid INTO @nidout FROM naicsCodes WHERE naics_code=h_naicscode;
    ELSE
      INSERT INTO naicsCodes(naics_code, top_category, sub_category)
      VALUES (h_naicscode, f_topcategory, g_subcategory);
      SELECT LAST_VALUE(nid) INTO @nidout;
    END IF;

  IF (e_brands IS NOT NULL) THEN -- Check if cell is populated for record insertion, else skip.
    BEGIN
    IF (SELECT COUNT(1) FROM brandsInfo WHERE brand_name=e_brands)=1 THEN
        SELECT bid INTO bidout FROM brandsInfo WHERE brand_name=e_brands;
      ELSE
        INSERT INTO brandsInfo(nid, brand_name)
        VALUES (@nidout, e_brands);
        SELECT LAST_VALUE(bid) INTO bidout;
    ELSE
      SET e_brands = e_brands
    END IF;

  IF (SELECT COUNT(1) FROM censusBlockGroups WHERE cbg_number=ac_poicbg)=1 THEN
      SELECT cbgid INTO @cbgidout FROM censusBlockGroups WHERE cbg_number=ac_poicbg;
    ELSE
      INSERT INTO censusBlockGroups(cbg_number)
      VALUES (ac_poicbg);
      SELECT LAST_VALUE(cbgid) INTO @cbgidout;
    END IF;

  IF (SELECT COUNT(1) FROM locationInfo WHERE placekey=a_placekey)=1 THEN
      SELECT locid INTO @locidout FROM locationInfo WHERE placekey=a_placekey;
    ELSE
      INSERT INTO locationInfo(nid, bid, cbgid, placekey, location_name, latitude, longitude, street_address, city, region, phone_number)
      VALUES (@nidout, @bidout, @cbgidout, a_placekey, i_latitude, j_longitude, k_streetaddress, l_city, m_region, n_postalcode, p_phonenumber);
      SELECT LAST_VALUE(locid) INTO @locidout;
    END IF;

  IF (SELECT COUNT(1) FROM visitsInfo WHERE (locid=@locidout AND week_begin=w_daterangestart))=1 
    BEGIN
        SELECT vid INTO @vidout FROM visitsInfo WHERE (locid=@locidout AND week_begin=w_daterangestart)
    END
    ELSE
        INSERT INTO visitsInfo(locid, week_begin, raw_visit_counts, raw_visitor_counts, distance_from_home, median_dwell,
                               normalized_visits_by_state_scaling, normalized_visits_by_region_naics_visits, normalized_visits_by_region_naics_visitors,
                               normalized_visits_by_total_visits, normalized_visits_by_total_visitors)
        VALUES (@locidout, w_daterangestart, y_rawvisitcounts, z_rawvisitorcounts, ah_distancefromhome, ai_mediumdwell,
                an_normvisits_statescaling, ao_normvisits_regionnaicsvisits, ap_normvisits_regionnaicsvisitors, aq_normvisits_totalvisits, ar_normvisits_totalvisitors);
        SELECT LAST_VALUE(vid) INTO @vidout;
      END IF;

END;

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