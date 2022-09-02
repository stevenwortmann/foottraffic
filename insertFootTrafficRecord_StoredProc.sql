ALTER PROCEDURE insertFootTrafficRecord(
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
	@ac_poicbg VARCHAR(max),
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
        SET @nidout=(SELECT nid FROM naicsCodes WHERE naics_code=@h_naicscode); --error: can't get past if there is same 
      END;
    ELSE
      BEGIN
        INSERT INTO naicsCodes(naics_code, top_category, sub_category)
        VALUES (@h_naicscode, @f_topcategory, @g_subcategory);
        SET @nidout=(SELECT LAST_VALUE(nid) OVER (ORDER BY nid) FROM naicsCodes);
      END;


    IF (SELECT COUNT(1) FROM brandsInfo WHERE brand_name=@e_brands)=1 --filter out nulls in python
      BEGIN
        SET @bidout=(SELECT bid FROM brandsInfo WHERE brand_name=@e_brands);
      END;
    ELSE
      BEGIN
        INSERT INTO brandsInfo(nid, brand_name)
        VALUES (@nidout, @e_brands);
        SET @bidout=(SELECT TOP 1 vid FROM visitsInfo ORDER BY vid DESC);
      END;

    IF (SELECT COUNT(1) FROM censusBlockGroups WHERE cbg_number=@ac_poicbg)=1
      BEGIN
		SET @cbgidout=(SELECT cbgid FROM censusBlockGroups WHERE cbg_number=@ac_poicbg);
      END;

    ELSE
      BEGIN
        INSERT INTO censusBlockGroups(cbg_number)
        VALUES (@ac_poicbg);
		SET @cbgidout=(SELECT TOP 1 vid FROM visitsInfo ORDER BY vid DESC);
      END;

    IF (SELECT COUNT(1) FROM locationInfo WHERE placekey=@a_placekey)=1
      BEGIN
		SET @locidout=(SELECT locid FROM locationInfo WHERE placekey=@a_placekey);
      END;
    ELSE
      BEGIN
        INSERT INTO locationInfo(nid, bid, cbgid, placekey, location_name, brand_name, latitude, longitude, street_address, city, region, postal_code, phone_number)
        VALUES (@nidout, @bidout, @cbgidout, @a_placekey, @c_locationname, @e_brands, @i_latitude, @j_longitude, @k_streetaddress, @l_city, @m_region, @n_postalcode, @p_phonenumber);
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