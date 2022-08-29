CREATE PROCEDURE addFootTrafficRecord(
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
  w_daterangestart VARCHAR(max),
  y_rawvisitcounts INT,
  z_rawvisitorcounts INT,
  ac_poicbg VARCHAR(max),
  ad_visitorhomecbgs VARCHAR(max),
  af_visitordaytimecbgsa VARCHAR(max),
  ah_distancefromhome INT,
  ai_mediumdwell FLOAT,
  ak_relatedsamedaybrand VARCHAR(max),
  al_relatedsameweekbrand VARCHAR(max),
  am_devicetype VARCHAR(max),
  an_normvisits_statescaling FLOAT,
  ao_normvisits_regionnaicsvisits FLOAT,
  ap_normvisits_totalvisits FLOAT,
  aq_normvisits_totalvisits FLOAT,
  ar_normvisits_totalvisitors FLOAT
)
AS $$
DECLARE @locidout INT;
DECLARE @bidout INT;
DECLARE @nidout INT;
DECLARE @vidout INT;

BEGIN

  IF (SELECT COUNT(1) FROM visitsInfo WHERE (placekey=a_pk AND date_range_start=w_ds))=1 
	BEGIN
      SELECT vid INTO @vidout FROM visitsInfo WHERE (placekey=a_pk AND date_range_start=w_ds)
	 END
   ELSE
	BEGIN
      INSERT INTO visitsInfo(placekey,date_range_start,date_range_end,raw_visit_counts,
                  raw_visitor_counts,visits_by_day,visits_by_each_hour,visitor_home_cbgs,
                  visitor_home_aggregation,visitor_daytime_cbgs,visitor_country_of_origin,
                  distance_from_home,median_dwell,bucketed_dwell_times,related_same_day_brand,
                  related_same_week_brand,device_type,normalized_visits_by_state_scaling,
                  normalized_visits_by_region_naics_visits,normalized_visits_by_region_naics_visitors,
                  normalized_visits_by_total_visits,normalized_visits_by_total_visitors)
      VALUES (a_pk,w_ds,x_de,y_rvt,z_rvr,aa_vbd,ab_vbh,ad_vhc,ae_vha,af_vdc,ag_vco,ah_dfh,ai_md,aj_bdt,ak_rsd,
          al_rsw,am_dt,an_nvss,ao_nvrnt,ap_nvnvr,aq_nvtvt,ar_nvtv);
      SELECT LAST_VALUE(vid) INTO @vidout;
	END;

  IF (SELECT COUNT(1) FROM naicsCodes WHERE naics_code=h_nc)=1 THEN
      SELECT nid INTO @nidout FROM naicsCodes WHERE naics_code=h_nc;
    ELSE
      INSERT INTO naicsCodes(top_category,sub_category,naics_code)
      VALUES (f_tc,g_sc,h_nc);
      SELECT LAST_VALUE(nid) INTO @nidout;
    END IF;

  IF (SELECT COUNT(1) FROM brandsInfo WHERE safegraph_brand_ids=d_sbid)=1 THEN
      SELECT bid INTO @bidout FROM brandsInfo WHERE safegraph_brand_ids=d_sbid;
    ELSE
      INSERT INTO brandsInfo(safegraph_brand_ids,brands,nid)
      VALUES (d_sbid,e_bds,@nidout);
      SELECT LAST_VALUE(bid) INTO @bidout;
    END IF;

  IF (SELECT COUNT(1) FROM locationInfo WHERE placekey=a_pk)=1 THEN
      SELECT locid INTO @locidout FROM locationInfo WHERE placekey=a_pk;
    ELSE
      INSERT INTO locationInfo(placekey,parent_placekey,location_name,vid,nid,bid,latitude,longitude,
        naics_code,city,region,street_address,iso_country_code,phone_number,open_hours,category_tags,
        opened_on,closed_on,tracking_closed_since,geometry_type,poi_cbg)
      VALUES (a_pk,b_ppk,c_lo,@vidout,@nidout,@bidout,i_lt,j_lg,k_sa,l_ci,m_rg,n_pc,
          o_cy,p_pn,q_op,r_ct,s_oo,t_co,u_ts,v_gt,ac_cbg);
      SELECT LAST_VALUE(locid) INTO @locidout;
    END IF;

END;
