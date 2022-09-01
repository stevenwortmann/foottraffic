import os
import json
import numpy as np
import pandas as pd
import pyodbc

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=;'
                      'Database=Foot_Traffic;' # Foot_Traffic DB already initialized
                      'UID=;'
                      'PWD=;'
                      'Trusted_Connection=no;')

cur = conn.cursor()

def initialize_database_tables():
	global conn  
	global cur
	
    sql1 = ('''
        USE [Foot_Traffic]

        DROP TABLE IF EXISTS[dbo].[brandsDay]
        DROP TABLE IF EXISTS[dbo].[brandsWeek]
        DROP TABLE IF EXISTS[dbo].[categoriesXref]
        DROP TABLE IF EXISTS[dbo].[categories]
        DROP TABLE IF EXISTS[dbo].[deviceLog]
        DROP TABLE IF EXISTS[dbo].[devices]
        DROP TABLE IF EXISTS[dbo].[homeVisits]
        DROP TABLE IF EXISTS[dbo].[workVisits]
        DROP TABLE IF EXISTS[dbo].[visitsInfo]
        DROP TABLE IF EXISTS[dbo].[locationInfo]
        DROP TABLE IF EXISTS[dbo].[censusBlockGroups]
        DROP TABLE IF EXISTS[dbo].[brandsInfo]
        DROP TABLE IF EXISTS[dbo].[naicsCodes]

        SET ANSI_NULLS ON
        GO
        SET QUOTED_IDENTIFIER ON
        GO
        CREATE TABLE [dbo].[brandsDay](
        [bdid] [int] IDENTITY(1,1) NOT NULL,
        [bid] [int] NOT NULL,
        [vid] [int] NOT NULL,
        [visit_count] [int] NOT NULL,
        PRIMARY KEY CLUSTERED 
        (
        [bid] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
        ) ON [PRIMARY]
        GO
        SET ANSI_NULLS ON
        GO
        SET QUOTED_IDENTIFIER ON
        GO
        CREATE TABLE [dbo].[brandsInfo](
        [bid] [int] IDENTITY(1,1) NOT NULL,
        [nid] [int] NOT NULL,
        [brand_name] [varchar](max) NOT NULL,
        PRIMARY KEY CLUSTERED 
        (
        [bid] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
        ) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
        GO
        SET ANSI_NULLS ON
        GO
        SET QUOTED_IDENTIFIER ON
        GO
        CREATE TABLE [dbo].[brandsWeek](
        [bwid] [int] IDENTITY(1,1) NOT NULL,
        [bid] [int] NOT NULL,
        [vid] [int] NOT NULL,
        [visit_count] [int] NOT NULL,
        PRIMARY KEY CLUSTERED 
        (
        [bwid] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
        ) ON [PRIMARY]
        GO
        SET ANSI_NULLS ON
        GO
        SET QUOTED_IDENTIFIER ON
        GO
        CREATE TABLE [dbo].[categories](
        [cid] [int] IDENTITY(1,1) NOT NULL,
        [category] [varchar](max) NOT NULL,
        PRIMARY KEY CLUSTERED 
        (
        [cid] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
        ) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
        GO
        SET ANSI_NULLS ON
        GO
        SET QUOTED_IDENTIFIER ON
        GO
        CREATE TABLE [dbo].[categoriesXref](
        [cxid] [int] IDENTITY(1,1) NOT NULL,
        [locid] [int] NOT NULL,
        [cid] [int] NOT NULL,
        PRIMARY KEY CLUSTERED 
        (
        [cxid] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
        ) ON [PRIMARY]
        GO
        SET ANSI_NULLS ON
        GO
        SET QUOTED_IDENTIFIER ON
        GO

        CREATE TABLE [dbo].[censusBlockGroups](
        [cbgid] [int] IDENTITY(1,1) NOT NULL,
        [cbg_number] [int] NOT NULL,
        PRIMARY KEY CLUSTERED 
        (
        [cbgid] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
        ) ON [PRIMARY]
        GO
        SET ANSI_NULLS ON
        GO
        SET QUOTED_IDENTIFIER ON
        GO
        CREATE TABLE [dbo].[deviceLog](
        [dlid] [int] IDENTITY(1,1) NOT NULL,
        [did] [int] NOT NULL,
        [vid] [int] NOT NULL,
        [user_count] [int] NOT NULL,
        PRIMARY KEY CLUSTERED 
        (
        [dlid] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
        ) ON [PRIMARY]
        GO
        SET ANSI_NULLS ON
        GO
        SET QUOTED_IDENTIFIER ON
        GO
        CREATE TABLE [dbo].[devices](
        [did] [int] IDENTITY(1,1) NOT NULL,
        [device_name] [varchar](max) NOT NULL,
        PRIMARY KEY CLUSTERED 
        (
        [did] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
        ) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
        GO
        SET ANSI_NULLS ON
        GO
        SET QUOTED_IDENTIFIER ON
        GO
        CREATE TABLE [dbo].[homeVisits](
        [hvid] [int] IDENTITY(1,1) NOT NULL,
        [vid] [int] NOT NULL,
        [cbgid] [int] NOT NULL,
        [visit_count] [int] NOT NULL,
        PRIMARY KEY CLUSTERED 
        (
        [hvid] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
        ) ON [PRIMARY]
        GO
        SET ANSI_NULLS ON
        GO
        SET QUOTED_IDENTIFIER ON
        GO
        CREATE TABLE [dbo].[locationInfo](
        [locid] [int] IDENTITY(1,1) NOT NULL,
        [nid] [int] NULL,
        [bid] [int] NULL,
        [cbgid] [int] NULL,
        [placekey] [varchar](max) NULL,
        [location_name] [varchar](max) NULL,
        [latitude] [float] NULL,
        [longitude] [float] NULL,
        [street_address] [varchar](max) NULL,
        [city] [varchar](max) NULL,
        [region] [varchar](max) NULL,
        [phone_number] [varchar](max) NULL,
        PRIMARY KEY CLUSTERED 
        (
        [locid] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
        ) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
        GO
        SET ANSI_NULLS ON
        GO
        SET QUOTED_IDENTIFIER ON
        GO
        CREATE TABLE [dbo].[naicsCodes](
        [nid] [int] IDENTITY(1,1) NOT NULL,
        [naics_code] [int] NOT NULL,
        [top_category] [varchar](max) NOT NULL,
        [sub_category] [varchar](max) NULL,
        PRIMARY KEY CLUSTERED 
        (
        [nid] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
        ) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
        GO
        SET ANSI_NULLS ON
        GO
        SET QUOTED_IDENTIFIER ON
        GO
        CREATE TABLE [dbo].[visitsInfo](
        [vid] [int] IDENTITY(1,1) NOT NULL,
        [locid] [int] NOT NULL,
        [week_begin] [date] NOT NULL,
        [raw_visit_counts] [int] NOT NULL,
        [raw_visitor_counts] [int] NOT NULL,
        [distance_from_home] [int] NULL,
        [median_dwell] [float] NULL,
        [normalized_visits_by_state_scaling] [float] NOT NULL,
        [normalized_visits_by_region_naics_visits] [float] NOT NULL,
        [normalized_visits_by_region_naics_visitors] [float] NOT NULL,
        [normalized_visits_by_total_visits] [float] NOT NULL,
        [normalized_visits_by_total_visitors] [float] NOT NULL,
        PRIMARY KEY CLUSTERED 
        (
        [vid] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
        ) ON [PRIMARY]
        GO
        SET ANSI_NULLS ON
        GO
        SET QUOTED_IDENTIFIER ON
        GO
        CREATE TABLE [dbo].[workVisits](
        [wvid] [int] IDENTITY(1,1) NOT NULL,
        [vid] [int] NOT NULL,
        [cbgid] [int] NOT NULL,
        [visit_count] [int] NOT NULL,
        PRIMARY KEY CLUSTERED 
        (
        [wvid] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
        ) ON [PRIMARY]
        GO
        ALTER TABLE [dbo].[brandsDay]  WITH CHECK ADD  CONSTRAINT [FK_brandsDay.bid] FOREIGN KEY([bid])
        REFERENCES [dbo].[brandsInfo] ([bid])
        GO
        ALTER TABLE [dbo].[brandsDay] CHECK CONSTRAINT [FK_brandsDay.bid]
        GO
        ALTER TABLE [dbo].[brandsDay]  WITH CHECK ADD  CONSTRAINT [FK_brandsDay.vid] FOREIGN KEY([vid])
        REFERENCES [dbo].[visitsInfo] ([vid])
        GO
        ALTER TABLE [dbo].[brandsDay] CHECK CONSTRAINT [FK_brandsDay.vid]
        GO
        ALTER TABLE [dbo].[brandsInfo]  WITH CHECK ADD  CONSTRAINT [FK_brandsInfo.nid] FOREIGN KEY([nid])
        REFERENCES [dbo].[naicsCodes] ([nid])
        GO
        ALTER TABLE [dbo].[brandsInfo] CHECK CONSTRAINT [FK_brandsInfo.nid]
        GO
        ALTER TABLE [dbo].[brandsWeek]  WITH CHECK ADD  CONSTRAINT [FK_brandsWeek.bid] FOREIGN KEY([bid])
        REFERENCES [dbo].[brandsInfo] ([bid])
        GO
        ALTER TABLE [dbo].[brandsWeek] CHECK CONSTRAINT [FK_brandsWeek.bid]
        GO
        ALTER TABLE [dbo].[brandsWeek]  WITH CHECK ADD  CONSTRAINT [FK_brandsWeek.vid] FOREIGN KEY([vid])
        REFERENCES [dbo].[visitsInfo] ([vid])
        GO
        ALTER TABLE [dbo].[brandsWeek] CHECK CONSTRAINT [FK_brandsWeek.vid]
        GO
        ALTER TABLE [dbo].[categoriesXref]  WITH CHECK ADD  CONSTRAINT [FK_categoriesXref.locid] FOREIGN KEY([locid])
        REFERENCES [dbo].[locationInfo] ([locid])
        GO
        ALTER TABLE [dbo].[categoriesXref] CHECK CONSTRAINT [FK_categoriesXref.locid]
        GO
        ALTER TABLE [dbo].[categoriesXref]  WITH CHECK ADD  CONSTRAINT [FK_categoriesXref.cid] FOREIGN KEY([cid])
        REFERENCES [dbo].[categories] ([cid])
        GO
        ALTER TABLE [dbo].[categoriesXref] CHECK CONSTRAINT [FK_categoriesXref.cid]
        GO
        ALTER TABLE [dbo].[deviceLog]  WITH CHECK ADD  CONSTRAINT [FK_deviceLog.did] FOREIGN KEY([did])
        REFERENCES [dbo].[devices] ([did])
        GO
        ALTER TABLE [dbo].[deviceLog] CHECK CONSTRAINT [FK_deviceLog.did]
        GO
        ALTER TABLE [dbo].[deviceLog]  WITH CHECK ADD  CONSTRAINT [FK_deviceLog.vid] FOREIGN KEY([vid])
        REFERENCES [dbo].[visitsInfo] ([vid])
        GO
        ALTER TABLE [dbo].[deviceLog] CHECK CONSTRAINT [FK_deviceLog.vid]
        GO
        ALTER TABLE [dbo].[homeVisits]  WITH CHECK ADD  CONSTRAINT [FK_homeVisits.cbgid] FOREIGN KEY([cbgid])
        REFERENCES [dbo].[censusBlockGroups] ([cbgid])
        GO
        ALTER TABLE [dbo].[homeVisits] CHECK CONSTRAINT [FK_homeVisits.cbgid]
        GO
        ALTER TABLE [dbo].[homeVisits]  WITH CHECK ADD  CONSTRAINT [FK_homeVisits.vid] FOREIGN KEY([vid])
        REFERENCES [dbo].[visitsInfo] ([vid])
        GO
        ALTER TABLE [dbo].[homeVisits] CHECK CONSTRAINT [FK_homeVisits.vid]
        GO
        ALTER TABLE [dbo].[locationInfo]  WITH CHECK ADD  CONSTRAINT [FK_locationInfo.bid] FOREIGN KEY([bid])
        REFERENCES [dbo].[brandsInfo] ([bid])
        GO
        ALTER TABLE [dbo].[locationInfo] CHECK CONSTRAINT [FK_locationInfo.bid]
        GO
        ALTER TABLE [dbo].[locationInfo]  WITH CHECK ADD  CONSTRAINT [FK_locationInfo.cbgid ] FOREIGN KEY([cbgid])
        REFERENCES [dbo].[censusBlockGroups] ([cbgid])
        GO
        ALTER TABLE [dbo].[locationInfo] CHECK CONSTRAINT [FK_locationInfo.cbgid ]
        GO
        ALTER TABLE [dbo].[locationInfo]  WITH CHECK ADD  CONSTRAINT [FK_locationInfo.nid] FOREIGN KEY([nid])
        REFERENCES [dbo].[naicsCodes] ([nid])
        GO
        ALTER TABLE [dbo].[locationInfo] CHECK CONSTRAINT [FK_locationInfo.nid]
        GO
        ALTER TABLE [dbo].[visitsInfo]  WITH CHECK ADD  CONSTRAINT [FK_visitsInfo.locid] FOREIGN KEY([locid])
        REFERENCES [dbo].[locationInfo] ([locid])
        GO
        ALTER TABLE [dbo].[visitsInfo] CHECK CONSTRAINT [FK_visitsInfo.locid]
        GO
        ALTER TABLE [dbo].[workVisits]  WITH CHECK ADD  CONSTRAINT [FK_workVisits.cbgid] FOREIGN KEY([cbgid])
        REFERENCES [dbo].[censusBlockGroups] ([cbgid])
        GO
        ALTER TABLE [dbo].[workVisits] CHECK CONSTRAINT [FK_workVisits.cbgid]
        GO
        ALTER TABLE [dbo].[workVisits]  WITH CHECK ADD  CONSTRAINT [FK_workVisits.vid] FOREIGN KEY([vid])
        REFERENCES [dbo].[visitsInfo] ([vid])
        GO
        ALTER TABLE [dbo].[workVisits] CHECK CONSTRAINT [FK_workVisits.vid]
        GO
        USE [master]
        GO
        ALTER DATABASE [Foot_Traffic] SET  READ_WRITE 
        GO
        USE [Foot_Traffic]
        GO
        INSERT INTO devices VALUES ('android');
        INSERT INTO devices VALUES ('ios');
    ''')

    cur.execute(sql1)
    conn.commit()
    cur.close()
    conn.close

def initialize_database_stored_procs():
	global conn
	global cur

	sql1=('''
		CREATE PROCEDURE insertBrandsDay(
		@a_placekey VARCHAR(max),
		@w_daterangestart VARCHAR(max),
		@ak_relatedsamedaybrand VARCHAR(max),
		@ak_relatedsamedaybrand_cnt INT
		)
		AS
		BEGIN
		DECLARE @vidout INT;
		DECLARE @bidout INT;

		BEGIN

		IF (SELECT COUNT(1) FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart))=1 
		BEGIN
		SELECT @vidout = LAST_VALUE(vid) OVER (ORDER BY vid) FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart);
		SELECT @bidout = LAST_VALUE(bid) OVER (ORDER BY bid) FROM brandsInfo WHERE (brand_name=@ak_relatedsamedaybrand);
		INSERT INTO brandsDay(vid, bid, visit_count)
		VALUES (@vidout, @bidout, @ak_relatedsamedaybrand_cnt);
		END;
		END;
		END;
	    ''')
	
	sql2=('''
		CREATE PROCEDURE insertBrandsWeek(
		@a_placekey VARCHAR(max),
		@w_daterangestart VARCHAR(max),
		@al_relatedsameweekbrand VARCHAR(max),
		@al_relatedsameweekbrand_cnt INT
		)
		AS
		BEGIN
		DECLARE @vidout INT;
		DECLARE @bidout INT;

		BEGIN

		IF (SELECT COUNT(1) FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart))=1 
		BEGIN
		SELECT @vidout = LAST_VALUE(vid) OVER (ORDER BY vid) FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart);
		SELECT @bidout = LAST_VALUE(bid) OVER (ORDER BY bid) FROM brandsInfo WHERE (brand_name=@al_relatedsameweekbrand);
		INSERT INTO brandsWeek(vid, bid, visit_count)
		VALUES (@vidout, @bidout, @al_relatedsameweekbrand_cnt);
		END;
		END;
		END;
	    ''')
	
	sql3=('''
		CREATE PROCEDURE insertCategories(
		@a_placekey VARCHAR(max),
		@r_categorytag VARCHAR(max)
		)
		AS
		BEGIN
		DECLARE @locidout INT;
		DECLARE @cidout INT;

		BEGIN

		IF (SELECT COUNT(1) FROM categories WHERE (category=@r_categorytag))=1 
		BEGIN
		SELECT cid INTO cidout FROM categories WHERE (category=@r_categorytag)
		END;
		ELSE
		BEGIN
		INSERT INTO categories(category)
		VALUES (@r_categorytag)
		SELECT @cidout = LAST_VALUE(cid) OVER (ORDER BY cid) FROM categories;
		SELECT @locidout = LAST_VALUE(locid) OVER (ORDER BY locid) FROM locationInfo;
		INSERT INTO categoriesXref(locid, cid)
		VALUES (@locidout, @cidout);
		END;
		END;
		END;
	    ''')
	
	sql4=('''
		CREATE PROCEDURE insertDeviceCount( -- 'device_name' field fully populated with init_db_tables
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
		SELECT @vidout = LAST_VALUE(vid) OVER (ORDER BY vid) FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart);
		SELECT @didout = LAST_VALUE(did) OVER (ORDER BY did) FROM devices WHERE (device_name=@am_devicetype);
		INSERT INTO deviceLog(did, vid, user_count)
		VALUES (@didout, @vidout, @am_devicetype_cnt);
		END;
		END;
		END;
	    ''')
	
	sql5=('''
		CREATE PROCEDURE insertFootTrafficRecord(
		@a_placekey VARCHAR(max),
		@c_locationname VARCHAR(max),
		@e_brands VARCHAR(max),
		@f_topcategory VARCHAR(max),
		@g_subcategory VARCHAR(max),
		@h_naicscode VARCHAR(max),
		@i_latitude FLOAT,
		@j_longitude FLOAT,
		@k_streetaddress VARCHAR(max),
		@l_city VARCHAR(max),
		@m_region VARCHAR(max),
		@n_postalcode VARCHAR(max),
		@p_phonenumber VARCHAR(max),
		@r_categorytag VARCHAR(max),
		@w_daterangestart VARCHAR(max),
		@y_rawvisitcounts INT,
		@z_rawvisitorcounts INT,
		@ac_poicbg VARCHAR(max),
		@ad_visitorhomecbg VARCHAR(max),
		@ad_visitorhomecbg_cnt INT,
		@af_visitordaytimecbg VARCHAR(max),
		@af_visitordaytimecbg_cnt INT,
		@ah_distancefromhome INT,
		@ai_mediumdwell FLOAT,
		@ak_relatedsamedaybrand VARCHAR(max),
		@ak_relatedsamedaybrand_cnt INT,
		@al_relatedsameweekbrand VARCHAR(max),
		@al_relatedsameweekbrand_cnt INT,
		@am_devicetype VARCHAR(max),
		@am_devicetype_cnt INT,
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
		SELECT nid INTO nidout FROM naicsCodes WHERE naics_code=@h_naicscode;
		END;
		ELSE
		BEGIN
		INSERT INTO naicsCodes(naics_code, top_category, sub_category)
		VALUES (@h_naicscode, @f_topcategory, @g_subcategory);
		SELECT @nidout = LAST_VALUE(nid) OVER (ORDER BY nid) FROM naicsCodes;
		END;


		IF (SELECT COUNT(1) FROM brandsInfo WHERE brand_name=@e_brands)=1 --filter out nulls in python
		BEGIN
		SELECT bid INTO bidout FROM brandsInfo WHERE brand_name=@e_brands;
		END;
		ELSE
		BEGIN
		INSERT INTO brandsInfo(nid, brand_name)
		VALUES (@nidout, @e_brands);
		SELECT @bidout = LAST_VALUE(bid) OVER (ORDER BY bid) FROM brandsInfo;
		END;

		IF (SELECT COUNT(1) FROM censusBlockGroups WHERE cbg_number=@ac_poicbg)=1
		BEGIN
		SELECT cbgid INTO cbgidout FROM censusBlockGroups WHERE cbg_number=@ac_poicbg;
		END;

		ELSE
		BEGIN
		INSERT INTO censusBlockGroups(cbg_number)
		VALUES (@ac_poicbg);
		SELECT @cbgidout = LAST_VALUE(cbgid) OVER (ORDER BY cbgid) FROM censusBlockGroups;
		END;

		IF (SELECT COUNT(1) FROM locationInfo WHERE placekey=@a_placekey)=1
		BEGIN
		SELECT locid INTO locidout FROM locationInfo WHERE placekey=@a_placekey;
		END;

		ELSE
		BEGIN
		INSERT INTO locationInfo(nid, bid, cbgid, placekey, location_name, latitude, longitude, street_address, city, region, phone_number)
		VALUES (@nidout, @bidout, @cbgidout, @a_placekey, @i_latitude, @j_longitude, @k_streetaddress, @l_city, @m_region, @n_postalcode, @p_phonenumber);
		SELECT @locidout = LAST_VALUE(locid) OVER (ORDER BY locid) FROM locationInfo;
		END;

		IF (SELECT COUNT(1) FROM visitsInfo WHERE (locid=@locidout AND week_begin=@w_daterangestart))=1 
		BEGIN
		SELECT vid INTO vidout FROM visitsInfo WHERE (locid=@locidout AND week_begin=@w_daterangestart)
		END;

		ELSE
		BEGIN
		INSERT INTO visitsInfo(locid, week_begin, raw_visit_counts, raw_visitor_counts, distance_from_home, median_dwell, normalized_visits_by_state_scaling,
		normalized_visits_by_region_naics_visits, normalized_visits_by_region_naics_visitors, normalized_visits_by_total_visits, normalized_visits_by_total_visitors)
		VALUES (@locidout, @w_daterangestart, @y_rawvisitcounts, @z_rawvisitorcounts, @ah_distancefromhome, @ai_mediumdwell, @an_normvisits_statescaling,
		@ao_normvisits_regionnaicsvisits, @ap_normvisits_regionnaicsvisitors, @aq_normvisits_totalvisits, @ar_normvisits_totalvisitors);
		SELECT @vidout = LAST_VALUE(vid) OVER (ORDER BY vid) FROM visitsInfo;
		END;
		END;
		END;
	    ''')
	
	sql6=('''
		CREATE PROCEDURE insertHomeVisits(
		@a_placekey VARCHAR(max),
		@w_daterangestart VARCHAR(max),
		@ad_visitorhomecbg VARCHAR(max),
		@ad_visitorhomecbg_cnt INT
		)
		AS
		BEGIN
		DECLARE @vidout INT;
		DECLARE @cbgidout INT;

		BEGIN

		IF (SELECT COUNT(1) FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart))=1 
		BEGIN
		SELECT @vidout = LAST_VALUE(vid) OVER (ORDER BY vid) FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart);
		SELECT @cbgidout = LAST_VALUE(cbgid) OVER (ORDER BY cbgid) FROM censusBlockGroups WHERE (cbg_number=@ad_visitorhomecbg);
		INSERT INTO homeVisits(vid, cbgid, visit_count)
		VALUES (@vidout, @cbgidout, @ad_visitorhomecbg_cnt);
		END;
		END;
		END;
	    ''')
	
	sql7=('''
		CREATE PROCEDURE insertWorkVisits(
		@a_placekey VARCHAR(max),
		@w_daterangestart VARCHAR(max),
		@af_visitordaytimecbg VARCHAR(max),
		@af_visitordaytimecbg_cnt INT
		)
		AS
		BEGIN
		DECLARE @vidout INT;
		DECLARE @cbgidout INT;

		BEGIN

		IF (SELECT COUNT(1) FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart))=1 
		BEGIN
		SELECT @vidout = LAST_VALUE(vid) OVER (ORDER BY vid) FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart);
		SELECT @cbgidout = LAST_VALUE(cbgid) OVER (ORDER BY cbgid) FROM censusBlockGroups WHERE (cbg_number=@af_visitordaytimecbg);
		INSERT INTO homeVisits(vid, cbgid, visit_count)
		VALUES (@vidout, @cbgidout, @af_visitordaytimecbg_cnt);
		END;
		END;
		END;
	    ''')

	for query in [sql1,sql2,sql3,sql4,sql5,sql6,sql7]
		cur.execute(query)
		conn.commit()
    cur.close()
    conn.close

