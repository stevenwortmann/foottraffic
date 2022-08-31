CREATE PROCEDURE insertDeviceCounts( -- 'device_name' field fully populated with init_db_tables
  a_placekey VARCHAR(max),
  w_daterangestart VARCHAR(max),
  am_devicetype VARCHAR(max),
  am_devicetype_cnt INT,
)
AS $$
DECLARE @didout INT;
DECLARE @vidout INT;

BEGIN

  IF (SELECT COUNT(1) FROM visitsInfo WHERE (placekey=a_placekey AND week_begin=w_daterangestart))=1 
    BEGIN
        SELECT vid INTO @vidout FROM visitsInfo WHERE (placekey=a_placekey AND week_begin=w_daterangestart)
        SELECT did INTO @didout FROM devices WHERE (device_name=am_devicetype)
        INSERT INTO deviceLog(did, vid, user_count)
        VALUES (@didout, @vidout, am_devicetype_cnt);
    END IF;
END;