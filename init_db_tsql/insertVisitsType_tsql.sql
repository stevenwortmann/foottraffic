CREATE OR ALTER PROCEDURE [dbo].[insertVisitsType](
  @locid INT,
  @vid INT,
  @cbgid_loc INT,
  @ad_af_visitorcbg VARCHAR(max),
  @ad_af_visitorcbg_cnt INT,
  home_work_ind CHAR(1)
)
AS
BEGIN

BEGIN

  IF (SELECT COUNT(1) FROM censusBlockGroups WHERE cbg_number=@ad_af_visitorcbg)=1
    BEGIN
      SET @cbgid_orig=(SELECT cbgid FROM censusBlockGroups WHERE cbg_number=@ad_af_visitorcbg);
    END;

  ELSE
    BEGIN
      INSERT INTO censusBlockGroups(cbg_number)
        VALUES (@ad_af_visitorcbg);
      SET @cbgid_orig=SCOPE_IDENTITY();
    END;

  INSERT INTO visitsType(locid, vid, cbgid_loc, cbgid_orig, visit_count, home_work_ind)
    VALUES (@locid, @vid, @cbgid_loc, @cbgid_orig, @ad_af_visitorcbg_cnt, home_work_ind);

END;
END;