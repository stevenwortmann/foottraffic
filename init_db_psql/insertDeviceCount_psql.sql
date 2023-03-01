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