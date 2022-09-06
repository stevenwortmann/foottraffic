ALTER PROCEDURE insertDeviceCount( -- 'device_name' field fully populated with init_db_tables
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
		SET @vidout = (SELECT TOP 1 vid FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart) ORDER BY vid DESC);	
		SET @didout = (SELECT TOP 1 did FROM devices WHERE (device_name=@am_devicetype) ORDER BY did DESC);
        INSERT INTO deviceLog(did, vid, user_count)
        VALUES (@didout, @vidout, @am_devicetype_cnt);
    END;
END;
END;