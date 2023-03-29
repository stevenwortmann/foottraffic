ALTER PROCEDURE [dbo].[insertDeviceCount]( -- 'device_name' field fully populated with init_db_tables
	@vid INT,
	@am_devicetype VARCHAR(max),
	@am_devicetype_cnt INT
)
AS
BEGIN
DECLARE @did INT;

BEGIN

SET @did = (SELECT did FROM devices WHERE (device_name=@am_devicetype));
INSERT INTO deviceLog(did, vid, user_count)
    VALUES (@did, @vid, @am_devicetype_cnt);
END;
END;