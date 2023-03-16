import os
import json
import numpy as np
import pandas as pd
import pyodbc
import time

def initialize_database_tables():
	global conn  
	global cur
	
    sql1 = ('''
        USE [Foot_Traffic]

        DROP TABLE IF EXISTS[dbo].[relatedBrands]
        DROP TABLE IF EXISTS[dbo].[categoriesXref]
        DROP TABLE IF EXISTS[dbo].[categories]
        DROP TABLE IF EXISTS[dbo].[deviceLog]
        DROP TABLE IF EXISTS[dbo].[devices]
        DROP TABLE IF EXISTS[dbo].[visitsType]
        DROP TABLE IF EXISTS[dbo].[visitsInfo]
        DROP TABLE IF EXISTS[dbo].[locationInfo]
        DROP TABLE IF EXISTS[dbo].[censusBlockGroups]
        DROP TABLE IF EXISTS[dbo].[brandsInfo]
        DROP TABLE IF EXISTS[dbo].[naicsCodes]

        GO

        SET ANSI_NULLS ON
        GO
        SET QUOTED_IDENTIFIER ON
        GO
        CREATE TABLE [dbo].[brandsInfo](
        [bid] [int] IDENTITY(1,1) NOT NULL,
        [nid] [int] NULL,
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
        [cbg_number] [bigint] NOT NULL,
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
        CREATE TABLE [dbo].[devices](
        [did] [int] IDENTITY(1,1) NOT NULL,
        [device_name] [varchar](10) NOT NULL,
        PRIMARY KEY CLUSTERED 
        (
        [did] ASC
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
        CREATE TABLE [dbo].[locationInfo](
        [locid] [int] IDENTITY(1,1) NOT NULL,
        [nid] [int] NULL,
        [bid] [int] NULL,
        [cbgid] [int] NULL,
        [placekey] [varchar](19) NOT NULL,
        [location_name] [varchar](max) NOT NULL,
        [latitude] [float] NULL,
        [longitude] [float] NULL,
        [street_address] [varchar](max) NOT NULL,
        [city] [varchar](max) NOT NULL,
        [region] [char](5) NOT NULL,
        [postal_code] [varchar](5) NOT NULL,
        [phone_number] [varchar](15) NULL,
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
        [naics_code] [varchar](10) NOT NULL,
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
        CREATE TABLE [dbo].[relatedBrands](
        [rbid] [int] IDENTITY(1,1) NOT NULL,
        [bid] [int] NOT NULL,
        [vid] [int] NOT NULL,
        [locid] [int] NOT NULL,
        [visit_count] [int] NOT NULL,
        [day_week_ind] [char](1) NOT NULL,
        PRIMARY KEY CLUSTERED 
        (
        [rbid] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
        ) ON [PRIMARY]
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
        CREATE TABLE [dbo].[visitsType](
        [vtid] [int] IDENTITY(1,1) NOT NULL,
        [locid] [int] NOT NULL,
        [vid] [int] NOT NULL,
        [cbgid_loc] [int] NOT NULL,
        [cbgid_orig] [int] NOT NULL,
        [visit_count] [int] NOT NULL,
        [home_work_ind] [char](1) NOT NULL,
        PRIMARY KEY CLUSTERED 
        (
        [vtid] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
        ) ON [PRIMARY]
        GO
        ALTER TABLE [dbo].[brandsInfo]  WITH CHECK ADD  CONSTRAINT [FK_brandsInfo.nid] FOREIGN KEY([nid])
        REFERENCES [dbo].[naicsCodes] ([nid])
        GO
        ALTER TABLE [dbo].[brandsInfo] CHECK CONSTRAINT [FK_brandsInfo.nid]
        GO
        ALTER TABLE [dbo].[categoriesXref]  WITH CHECK ADD  CONSTRAINT [FK_categoriesXref.cid] FOREIGN KEY([cid])
        REFERENCES [dbo].[categories] ([cid])
        GO
        ALTER TABLE [dbo].[categoriesXref] CHECK CONSTRAINT [FK_categoriesXref.cid]
        GO
        ALTER TABLE [dbo].[categoriesXref]  WITH CHECK ADD  CONSTRAINT [FK_categoriesXref.locid] FOREIGN KEY([locid])
        REFERENCES [dbo].[locationInfo] ([locid])
        GO
        ALTER TABLE [dbo].[categoriesXref] CHECK CONSTRAINT [FK_categoriesXref.locid]
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
        ALTER TABLE [dbo].[relatedBrands]  WITH CHECK ADD  CONSTRAINT [FK_relatedBrands.bid] FOREIGN KEY([bid])
        REFERENCES [dbo].[brandsInfo] ([bid])
        GO
        ALTER TABLE [dbo].[relatedBrands] CHECK CONSTRAINT [FK_relatedBrands.bid]
        GO
        ALTER TABLE [dbo].[relatedBrands]  WITH CHECK ADD  CONSTRAINT [FK_relatedBrands.locid] FOREIGN KEY([locid])
        REFERENCES [dbo].[locationInfo] ([locid])
        GO
        ALTER TABLE [dbo].[relatedBrands] CHECK CONSTRAINT [FK_relatedBrands.locid]
        GO
        ALTER TABLE [dbo].[relatedBrands]  WITH CHECK ADD  CONSTRAINT [FK_relatedBrands.vid] FOREIGN KEY([vid])
        REFERENCES [dbo].[visitsInfo] ([vid])
        GO
        ALTER TABLE [dbo].[relatedBrands] CHECK CONSTRAINT [FK_relatedBrands.vid]
        GO
        ALTER TABLE [dbo].[visitsInfo]  WITH CHECK ADD  CONSTRAINT [FK_visitsInfo.locid] FOREIGN KEY([locid])
        REFERENCES [dbo].[locationInfo] ([locid])
        GO
        ALTER TABLE [dbo].[visitsInfo] CHECK CONSTRAINT [FK_visitsInfo.locid]
        GO
        ALTER TABLE [dbo].[visitsType]  WITH CHECK ADD  CONSTRAINT [FK_visitsType.locid] FOREIGN KEY([locid])
        REFERENCES [dbo].[locationInfo] ([locid])
        GO
        ALTER TABLE [dbo].[visitsType] CHECK CONSTRAINT [FK_visitsType.locid]
        GO
        ALTER TABLE [dbo].[visitsType]  WITH CHECK ADD  CONSTRAINT [FK_visitsType.vid] FOREIGN KEY([vid])
        REFERENCES [dbo].[visitsInfo] ([vid])
        GO
        ALTER TABLE [dbo].[visitsType] CHECK CONSTRAINT [FK_visitsType.vid]
        GO
        ALTER TABLE [dbo].[visitsType]  WITH CHECK ADD  CONSTRAINT [FK_visitsType.cbgid_loc] FOREIGN KEY([cbgid_loc])
        REFERENCES [dbo].[censusBlockGroups] ([cbgid])
        GO
        ALTER TABLE [dbo].[visitsType] CHECK CONSTRAINT [FK_visitsType.cbgid_loc]
        GO
        ALTER TABLE [dbo].[visitsType]  WITH CHECK ADD  CONSTRAINT [FK_visitsType.cbgid_orig] FOREIGN KEY([cbgid_orig])
        REFERENCES [dbo].[censusBlockGroups] ([cbgid])
        GO
        ALTER TABLE [dbo].[visitsType] CHECK CONSTRAINT [FK_visitsType.cbgid_orig]
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
        CREATE OR ALTER PROCEDURE [dbo].[insertRelatedBrands_Day](
        @a_placekey VARCHAR(max),
        @w_daterangestart VARCHAR(max),
        @ak_relatedsamedaybrand VARCHAR(max),
        @ak_relatedsamedaybrand_cnt INT
        )
        AS
        BEGIN
        DECLARE @vidout INT;
        DECLARE @bidout INT;
        DECLARE @locidout INT;

        BEGIN

        IF (SELECT COUNT(1) FROM brandsInfo WHERE brand_name=@ak_relatedsamedaybrand)=1
        BEGIN
            SET @bidout=(SELECT bid FROM brandsInfo WHERE brand_name=@ak_relatedsamedaybrand);
        END;
        ELSE
        BEGIN
            INSERT INTO brandsInfo(brand_name)
            VALUES (@ak_relatedsamedaybrand);
            SET @bidout=(SELECT TOP 1 bid FROM brandsInfo ORDER BY bid DESC);
        END;


        IF (SELECT COUNT(1) FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart))=1 
        BEGIN
        SET @vidout = (SELECT TOP 1 vid FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart));
        SET @locidout = (SELECT TOP 1 locid FROM locationInfo WHERE placekey=@a_placekey);			
        INSERT INTO relatedBrands(bid, vid, locid, visit_count, day_week_ind)
        VALUES (@bidout, @vidout, @locidout, @ak_relatedsamedaybrand_cnt, 'd');
        END;
        END;
        END;
	    ''')
	
	sql2=('''
        CREATE OR ALTER PROCEDURE [dbo].[insertRelatedBrands_Week](
        @a_placekey VARCHAR(max),
        @w_daterangestart VARCHAR(max),
        @al_relatedsameweekbrand VARCHAR(max),
        @al_relatedsameweekbrand_cnt INT
        )
        AS
        BEGIN
        DECLARE @vidout INT;
        DECLARE @bidout INT;
        DECLARE @locidout INT;

        BEGIN

        IF (SELECT COUNT(1) FROM brandsInfo WHERE brand_name=@al_relatedsameweekbrand)=1
        BEGIN
        SET @bidout=(SELECT bid FROM brandsInfo WHERE brand_name=@al_relatedsameweekbrand);
        END;
        ELSE
        BEGIN
        INSERT INTO brandsInfo(brand_name)
        VALUES (@al_relatedsameweekbrand);
        SET @bidout=(SELECT TOP 1 bid FROM brandsInfo ORDER BY bid DESC);
        END;


        IF (SELECT COUNT(1) FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart))=1 
        BEGIN
        SET @vidout = (SELECT TOP 1 vid FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart));
        SET @locidout = (SELECT TOP 1 locid FROM locationInfo l WHERE l.placekey=@a_placekey);			
        INSERT INTO relatedBrands(bid, vid, locid, visit_count, day_week_ind)
        VALUES (@bidout, @vidout, @locidout, @al_relatedsameweekbrand_cnt, 'w');
        END;
        END;
        END;
	    ''')
	
	sql3=('''
        CREATE OR ALTER PROCEDURE [dbo].[insertCategories](
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
        SET @cidout=(SELECT cid FROM categories WHERE category=@r_categorytag)
        END;
        ELSE
        BEGIN
        INSERT INTO categories(category)
        VALUES (@r_categorytag);
        SET @cidout=(SELECT TOP 1 cid FROM categories ORDER BY cid DESC);
        SET @locidout=(SELECT locid FROM locationInfo WHERE placekey=@a_placekey);
        INSERT INTO categoriesXref(locid, cid)
        VALUES (@locidout, @cidout);
        END;
        END;
        END;
	    ''')
	
	sql4=('''
        CREATE OR ALTER PROCEDURE [dbo].[insertDeviceCount]( -- 'device_name' field fully populated with init_db_tables
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
        SET @vidout = (SELECT vid FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart));	
        SET @didout = (SELECT did FROM devices WHERE (device_name=@am_devicetype));
        INSERT INTO deviceLog(did, vid, user_count)
        VALUES (@didout, @vidout, @am_devicetype_cnt);
        END;
        END;
        END;
	    ''')
	
	sql5=('''
        CREATE OR ALTER PROCEDURE [dbo].[insertFootTrafficRecord](
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
        @ac_poicbg BIGINT,
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
        SET @nidout=(SELECT nid FROM naicsCodes WHERE naics_code=@h_naicscode);
        END;
        ELSE
        BEGIN
        INSERT INTO naicsCodes(naics_code, top_category, sub_category)
        VALUES (@h_naicscode, @f_topcategory, @g_subcategory);
        SET @nidout=(SELECT TOP 1 nid FROM naicsCodes ORDER BY nid DESC);
        END;

        IF (SELECT COUNT(1) FROM brandsInfo WHERE brand_name=@e_brands)=1
        BEGIN
        IF (SELECT nid FROM brandsInfo WHERE brand_name=@e_brands) IS NULL
        BEGIN
        UPDATE brandsInfo SET nid=@nidout WHERE brand_name=@e_brands;
        END;
        SET @bidout=(SELECT bid FROM brandsInfo WHERE brand_name=@e_brands);
        END;
        ELSE
        BEGIN
        INSERT INTO brandsInfo(nid, brand_name)
        VALUES (@nidout, @e_brands);
        SET @bidout=(SELECT TOP 1 bid FROM brandsInfo ORDER BY bid DESC);
        END;

        IF (SELECT COUNT(1) FROM censusBlockGroups WHERE cbg_number=@ac_poicbg)=1
        BEGIN
        SET @cbgidout=(SELECT cbgid FROM censusBlockGroups WHERE cbg_number=@ac_poicbg);
        END;

        ELSE
        BEGIN
        INSERT INTO censusBlockGroups(cbg_number)
        VALUES (@ac_poicbg);
        SET @cbgidout=(SELECT TOP 1 cbgid FROM censusBlockGroups ORDER BY cbgid DESC);
        END;

        IF (SELECT COUNT(1) FROM locationInfo WHERE placekey=@a_placekey)=1
        BEGIN
        SET @locidout=(SELECT locid FROM locationInfo WHERE placekey=@a_placekey);
        END;
        ELSE
        BEGIN
        INSERT INTO locationInfo(nid, bid, cbgid, placekey, location_name, latitude, longitude, street_address, city, region, postal_code, phone_number)
        VALUES (@nidout, @bidout, @cbgidout, @a_placekey, @c_locationname, @i_latitude, @j_longitude, @k_streetaddress, @l_city, @m_region, @n_postalcode, @p_phonenumber);
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
	    ''')
	
	sql6=('''
        CREATE OR ALTER PROCEDURE [dbo].[insertVisitsType_Home](
        @a_placekey VARCHAR(max),
        @ac_poicbg BIGINT,
        @w_daterangestart VARCHAR(max),
        @ad_visitorhomecbg VARCHAR(max),
        @ad_visitorhomecbg_cnt INT
        )
        AS
        BEGIN
        DECLARE @vidout INT;
        DECLARE @cbgidout INT;
        DECLARE @locidout INT;

        BEGIN

        SET @locidout=(SELECT locid FROM locationInfo WHERE placekey=@a_placekey) 

        IF (SELECT COUNT(1) FROM censusBlockGroups WHERE cbg_number=@ad_visitorhomecbg)=1
        BEGIN
            SET @cbgidout=(SELECT cbgid FROM censusBlockGroups WHERE cbg_number=@ad_visitorhomecbg);
        END;

        ELSE
        BEGIN
            INSERT INTO censusBlockGroups(cbg_number)
            VALUES (@ad_visitorhomecbg);
            SET @cbgidout=(SELECT TOP 1 cbgid FROM censusBlockGroups ORDER BY cbgid DESC);
        END;

        IF (SELECT COUNT(1) FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart))=1 
        BEGIN
                SET @vidout = (SELECT TOP 1 vid FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart) ORDER BY vid DESC);	
            INSERT INTO visitsType(locid, vid, cbgid_loc, cbgid_orig, visit_count, home_work_ind)
            VALUES (@locidout, @vidout, @ac_poicbg, @cbgidout, @ad_visitorhomecbg_cnt, 'h');
        END;
        END;
        END;
	    ''')
	
	sql7=('''
        CREATE OR ALTER PROCEDURE [dbo].[insertVisitsType_Work](
        @a_placekey VARCHAR(max),
        @ac_poicbg BIGINT,
        @w_daterangestart VARCHAR(max),
        @af_visitordaytimecbg BIGINT,
        @af_visitordaytimecbg_cnt INT
        )
        AS
        BEGIN
        DECLARE @vidout INT;
        DECLARE @cbgidout INT;
        DECLARE @locidout INT;

        BEGIN

        SET @locidout=(SELECT locid FROM locationInfo WHERE placekey=@a_placekey) 

        IF (SELECT COUNT(1) FROM censusBlockGroups WHERE cbg_number=@af_visitordaytimecbg)=1
        BEGIN
        SET @cbgidout=(SELECT cbgid FROM censusBlockGroups WHERE cbg_number=@af_visitordaytimecbg);
        END;

        ELSE
        BEGIN
        INSERT INTO censusBlockGroups(cbg_number)
        VALUES (@af_visitordaytimecbg);
        SET @cbgidout=(SELECT TOP 1 cbgid FROM censusBlockGroups ORDER BY cbgid DESC);
        END;

        IF (SELECT COUNT(1) FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart))=1 
        BEGIN
            SET @vidout = (SELECT TOP 1 vid FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart) ORDER BY vid DESC);	
        INSERT INTO visitsType(locid, vid, cbgid_loc, cbgid_orig, visit_count, home_work_ind)
        VALUES (@locidout, @vidout, @ac_poicbg, @cbgidout, @af_visitordaytimecbg_cnt, 'w');
        END;
        END;
        END;
	    ''')

	for query in [sql1,sql2,sql3,sql4,sql5,sql6,sql7]
		cur.execute(query)
		conn.commit()
    cur.close()
    conn.close

def poiRecordInsertion(file):
	global conn
	global cur

    sql_insertFootTrafficRecord='''EXECUTE [insertFootTrafficRecord]
       @a_placekey=?
      ,@c_locationname=?
      ,@e_brands=?
      ,@f_topcategory=?
      ,@g_subcategory=?
      ,@h_naicscode=?
      ,@i_latitude=?
      ,@j_longitude=?
      ,@k_streetaddress=?
      ,@l_city=?
      ,@m_region=?
      ,@n_postalcode=?
      ,@p_phonenumber=?
      ,@w_daterangestart=?
      ,@y_rawvisitcounts=?
      ,@z_rawvisitorcounts=?
      ,@ac_poicbg=?
      ,@ah_distancefromhome=?
      ,@ai_mediumdwell=?
      ,@an_normvisits_statescaling=?
      ,@ao_normvisits_regionnaicsvisits=?
      ,@ap_normvisits_regionnaicsvisitors=?
      ,@aq_normvisits_totalvisits=?
      ,@ar_normvisits_totalvisitors=?
    '''

    sql_insertVisitsType_Home='''EXECUTE [insertVisitsType_Home] 
       @a_placekey=?
	  ,@ac_poicbg=?
      ,@w_daterangestart=?
      ,@ad_visitorhomecbg=?
      ,@ad_visitorhomecbg_cnt=?
    '''

    sql_insertVisitsType_Work='''EXECUTE [insertVisitsType_Work] 
       @a_placekey=?
	  ,@ac_poicbg=?
      ,@w_daterangestart=?
      ,@af_visitordaytimecbg=?
      ,@af_visitordaytimecbg_cnt=?
    '''

    sql_insertRelatedBrands_Day='''EXECUTE [insertBrandsDay] 
       @a_placekey=?
      ,@w_daterangestart=?
      ,@ak_relatedsamedaybrand=?
      ,@ak_relatedsamedaybrand_cnt=?
    '''

    sql_insertRelatedBrands_Week='''EXECUTE [insertBrandsWeek] 
       @a_placekey=?
      ,@w_daterangestart=?
      ,@al_relatedsameweekbrand=?
      ,@al_relatedsameweekbrand_cnt=?
    '''

    sql_insertDeviceCount='''EXECUTE [insertDeviceCount] 
       @a_placekey=?
      ,@w_daterangestart=?
      ,@am_devicetype=?
      ,@am_devicetype_cnt=?
    '''

    sql_insertCategories='''EXECUTE [insertCategories] 
       @a_placekey=?
      ,@r_categorytag=?
    '''

    for row in file.itertuples():
        values_insertFootTrafficRecord = (row.placekey, row.location_name, row.brands, row.top_category, row.sub_category,
                                          int(row.naics_code), row.latitude, row.longitude, row.street_address, row.city,
                                          row.region, int(row.postal_code), int(row.phone_number), row.date_range_start,
                                          int(row.raw_visit_counts), int(row.raw_visitor_counts), int(row.poi_cbg),
                                          int(row.distance_from_home), row.median_dwell, row.normalized_visits_by_state_scaling,
                                          row.normalized_visits_by_region_naics_visits, row.normalized_visits_by_region_naics_visitors,
                                          row.normalized_visits_by_total_visits,row.normalized_visits_by_total_visitors )
        cur.execute(sql_insertFootTrafficRecord, values_insertFootTrafficRecord)
        cur.commit()
        print(row.location_name[:20]+', '+row.street_address+', '+row.city+', '+row.region+' '+str(row.postal_code)+'... '+
             row.date_range_start+": "+str(int(row.normalized_visits_by_state_scaling))+' total visitors...')

        for x in row.visitor_home_cbgs.split(','):
            if x!= "{}":
                x = (x.replace("{","")).replace('''"''',"").replace("}","").split(':')
                if (x[0][0]).isalpha() is True: pass
                else:
                    values_insertVisitsType_Home = (row.placekey, row.poi_cbg, row.date_range_start, int(x[0]), int(x[1]))
                    cur.execute(sql_insertVisitsType_Home, values_insertVisitsType_Home)
                    cur.commit()
                    #print(x)

        for x in row.visitor_daytime_cbgs.split(','):
            if x!= "{}":
                x = (x.replace("{","")).replace('''"''',"").replace("}","").split(':')
                if (x[0][0]).isalpha() is True: pass
                else:
                    values_insertVisitsType_Work = (row.placekey, row.poi_cbg, row.date_range_start, int(x[0]), int(x[1]))
                    cur.execute(sql_insertVisitsType_Work, values_insertVisitsType_Work)
                    cur.commit()
                    #print(x)

        for x in row.related_same_day_brand.split(',"'):
            if x!= "{}":
                x = (x.replace('{"',"")).replace('\\',"").replace("}","").split('":')
                if (x[1][0]).isalpha() is True: pass
                else:
                    values_insertBrandsDay = (row.placekey, row.date_range_start, x[0], int(x[1]))
                    cur.execute(sql_insertBrandsDay, values_insertBrandsDay)
                    cur.commit()
                    #print(x)

        for x in row.related_same_week_brand.split(',"'):
            if x!= "{}":
                x = (x.replace('{"',"")).replace('\\',"").replace("}","").split('":')
                if (x[1][0]).isalpha() is True: pass
                else:
                    values_insertRelatedBrands_Week = (row.placekey, row.date_range_start, x[0], int(x[1]))
                    cur.execute(sql_insertRelatedBrands_Week, values_insertRelatedBrands_Week)
                    cur.commit()
                    #print(x)

        for x in row.device_type.split(','):
            if x!= "{}":
                x = (x.replace("{","")).replace('''"''',"").replace("}","").split(':')
                values_insertDeviceCount = (row.placekey, row.date_range_start, x[0], int(x[1]))
                cur.execute(sql_insertDeviceCount, values_insertDeviceCount)
                cur.commit()
                #print(x)

        for x in str(row.category_tags).split(','):
            if x != '0':
                values_insertCategories = (row.placekey, x)
                cur.execute(sql_insertCategories, values_insertCategories)
                cur.commit()
                #print(x)

def main():
    driver = '{SQL Server}'
    server = 'PDTTESQLDEV01'
    db = 'Foot_Traffic' # blank database already created
    user = ''
    password = ''

    while True:
        time.sleep(.001)
        if not conn:  # No connection yet? Connect.
            conn = pyodbc.connect(driver=driver, server=server, database=db,
                            user=user, password=password, trusted_connection='yes')
            cur = conn.cursor()
            initialize_database_tables()
            initialize_database_stored_procs() #initialize database resources before insertion
        try:
            poiRecordInsertion(raw_csv) # csv passed through
        except pyodbc.Error as pe:
            print("Error:", pe)
            if pe.args[0] == "08S01":  # Communication error.
                # Nuke the connection and retry.
                try:
                    conn.close()
                except:
                    pass
                conn = pyodbc.connect(driver=driver, server=server, database=db,
                            user=user, password=password, trusted_connection='yes')
                cur = conn.cursor()
                continue
            raise  # Re-raise any other exception