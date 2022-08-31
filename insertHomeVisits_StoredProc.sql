CREATE PROCEDURE insertHomeVisits(
  a_placekey VARCHAR(max),
  w_daterangestart VARCHAR(max),
  ad_visitorhomecbg VARCHAR(max),
  ad_visitorhomecbg_cnt INT,
)
AS $$
DECLARE @vidout INT;
DECLARE @cbgidout INT;

BEGIN

  IF (SELECT COUNT(1) FROM visitsInfo WHERE (placekey=a_placekey AND week_begin=w_daterangestart))=1 
    BEGIN
        SELECT vid INTO @vidout FROM visitsInfo WHERE (placekey=a_placekey AND week_begin=w_daterangestart)
        SELECT cbgid INTO @cbgidout FROM censusBlockGroups WHERE (cbg_number=ad_visitorhomecbg)
        INSERT INTO homeVisits(vid, cbgid, visit_count)
        VALUES (@vidout, @cbgidout, ad_visitorhomecbg_cnt);
    END IF;
END;