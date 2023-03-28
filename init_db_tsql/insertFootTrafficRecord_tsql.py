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

        DROP TABLE IF EXISTS[dbo].[visitsType]
        DROP TABLE IF EXISTS[dbo].[relatedBrands]
        DROP TABLE IF EXISTS[dbo].[categoriesXref]
        DROP TABLE IF EXISTS[dbo].[categories]
        DROP TABLE IF EXISTS[dbo].[deviceLog]
        DROP TABLE IF EXISTS[dbo].[devices]
        DROP TABLE IF EXISTS[dbo].[visitsInfo]
        DROP TABLE IF EXISTS[dbo].[locationInfo]
        DROP TABLE IF EXISTS[dbo].[brandsInfo]
        DROP TABLE IF EXISTS[dbo].[censusBlockGroups]
        DROP TABLE IF EXISTS[dbo].[naicsCodes]

        /****** Object:  Table [dbo].[brandsInfo]    Script Date: 3/24/2023 1:25:34 PM ******/
        SET ANSI_NULLS ON
        GO
        SET QUOTED_IDENTIFIER ON
        GO
        CREATE TABLE [dbo].[brandsInfo](
        [bid] [int] IDENTITY(1,1) NOT NULL,
        [nid] [int] NULL,
        [brand_name] [varchar](max) NOT NULL,
        CONSTRAINT [PK_brandsInfo.bid] PRIMARY KEY CLUSTERED 
        (
        [bid] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
        ) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
        GO
        /****** Object:  Table [dbo].[categories]    Script Date: 3/24/2023 1:25:34 PM ******/
        SET ANSI_NULLS ON
        GO
        SET QUOTED_IDENTIFIER ON
        GO
        CREATE TABLE [dbo].[categories](
        [cid] [int] IDENTITY(1,1) NOT NULL,
        [category] [varchar](max) NOT NULL,
        CONSTRAINT [PK_categories.cid] PRIMARY KEY CLUSTERED 
        (
        [cid] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
        ) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
        GO
        /****** Object:  Table [dbo].[categoriesXref]    Script Date: 3/24/2023 1:25:34 PM ******/
        SET ANSI_NULLS ON
        GO
        SET QUOTED_IDENTIFIER ON
        GO
        CREATE TABLE [dbo].[categoriesXref](
        [cxid] [int] IDENTITY(1,1) NOT NULL,
        [locid] [int] NOT NULL,
        [cid] [int] NOT NULL,
        CONSTRAINT [PK_categoriesXref.cxid] PRIMARY KEY CLUSTERED 
        (
        [cxid] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
        ) ON [PRIMARY]
        GO
        /****** Object:  Table [dbo].[censusBlockGroups]    Script Date: 3/24/2023 1:25:34 PM ******/
        SET ANSI_NULLS ON
        GO
        SET QUOTED_IDENTIFIER ON
        GO
        CREATE TABLE [dbo].[censusBlockGroups](
        [cbgid] [int] IDENTITY(1,1) NOT NULL,
        [cbg_number] [bigint] NOT NULL,
        CONSTRAINT [PK_censusBlockGroups.cbgid] PRIMARY KEY CLUSTERED 
        (
        [cbgid] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
        ) ON [PRIMARY]
        GO
        /****** Object:  Table [dbo].[deviceLog]    Script Date: 3/24/2023 1:25:34 PM ******/
        SET ANSI_NULLS ON
        GO
        SET QUOTED_IDENTIFIER ON
        GO
        CREATE TABLE [dbo].[deviceLog](
        [dlid] [int] IDENTITY(1,1) NOT NULL,
        [did] [int] NOT NULL,
        [vid] [int] NOT NULL,
        [user_count] [int] NOT NULL,
        CONSTRAINT [PK_deviceLog.dlid] PRIMARY KEY CLUSTERED 
        (
        [dlid] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
        ) ON [PRIMARY]
        GO
        /****** Object:  Table [dbo].[devices]    Script Date: 3/24/2023 1:25:34 PM ******/
        SET ANSI_NULLS ON
        GO
        SET QUOTED_IDENTIFIER ON
        GO
        CREATE TABLE [dbo].[devices](
        [did] [int] IDENTITY(1,1) NOT NULL,
        [device_name] [varchar](10) NOT NULL,
        CONSTRAINT [PK_devices.did] PRIMARY KEY CLUSTERED 
        (
        [did] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
        ) ON [PRIMARY]
        GO
        /****** Object:  Table [dbo].[locationInfo]    Script Date: 3/24/2023 1:25:34 PM ******/
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
        CONSTRAINT [PK_locationInfo.locid] PRIMARY KEY CLUSTERED 
        (
        [locid] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
        ) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
        GO
        /****** Object:  Table [dbo].[naicsCodes]    Script Date: 3/24/2023 1:25:34 PM ******/
        SET ANSI_NULLS ON
        GO
        SET QUOTED_IDENTIFIER ON
        GO
        CREATE TABLE [dbo].[naicsCodes](
        [nid] [int] IDENTITY(1,1) NOT NULL,
        [naics_code] [varchar](10) NOT NULL,
        [top_category] [varchar](max) NOT NULL,
        [sub_category] [varchar](max) NULL,
        CONSTRAINT [PK_naicsCodes.nid] PRIMARY KEY CLUSTERED 
        (
        [nid] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
        ) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
        GO
        /****** Object:  Table [dbo].[relatedBrands]    Script Date: 3/24/2023 1:25:34 PM ******/
        SET ANSI_NULLS ON
        GO
        SET QUOTED_IDENTIFIER ON
        GO
        CREATE TABLE [dbo].[relatedBrands](
        [rbid] [int] IDENTITY(1,1) NOT NULL,
        [vid] [int] NOT NULL,
        [locid] [int] NOT NULL,
        [bid_loc] [int] NOT NULL,
        [bid_rel] [int] NOT NULL,
        [visit_count] [int] NOT NULL,
        [day_week_ind] [char](1) NOT NULL,
        CONSTRAINT [PK_relatedBrands.rbid] PRIMARY KEY CLUSTERED 
        (
        [rbid] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
        ) ON [PRIMARY]
        GO
        /****** Object:  Table [dbo].[visitsInfo]    Script Date: 3/24/2023 1:25:34 PM ******/
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
        CONSTRAINT [PK_visitsInfo.vid] PRIMARY KEY CLUSTERED 
        (
        [vid] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
        ) ON [PRIMARY]
        GO
        /****** Object:  Table [dbo].[visitsType]    Script Date: 3/24/2023 1:25:34 PM ******/
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
        CONSTRAINT [PK_visitsType.vtid] PRIMARY KEY CLUSTERED 
        (
        [vtid] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
        ) ON [PRIMARY]
        GO
        /****** Object:  Index [categories_locationInfo_uix]    Script Date: 3/24/2023 1:25:34 PM ******/
        CREATE UNIQUE NONCLUSTERED INDEX [categories_locationInfo_uix] ON [dbo].[categoriesXref]
        (
        [locid] ASC,
        [cid] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
        GO
        /****** Object:  Index [visitsInfo_devices_uix]    Script Date: 3/24/2023 1:25:34 PM ******/
        CREATE UNIQUE NONCLUSTERED INDEX [visitsInfo_devices_uix] ON [dbo].[deviceLog]
        (
        [did] ASC,
        [vid] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
        GO
        /****** Object:  Index [naicsCodes_brandsInfo_censusBlockGroups_uix]    Script Date: 3/24/2023 1:25:34 PM ******/
        CREATE UNIQUE NONCLUSTERED INDEX [naicsCodes_brandsInfo_censusBlockGroups_uix] ON [dbo].[locationInfo]
        (
        [nid] ASC,
        [bid] ASC,
        [cbgid] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
        GO
        /****** Object:  Index [brandsInfo_locationInfo_visitsInfo_uix]    Script Date: 3/24/2023 1:25:34 PM ******/
        CREATE UNIQUE NONCLUSTERED INDEX [brandsInfo_locationInfo_visitsInfo_uix] ON [dbo].[relatedBrands]
        (
        [vid] ASC,
        [locid] ASC,
        [bid_loc] ASC,
        [bid_rel] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
        GO
        /****** Object:  Index [locationInfo_visitsInfo_censusBlockGroups_uix]    Script Date: 3/24/2023 1:25:34 PM ******/
        CREATE UNIQUE NONCLUSTERED INDEX [locationInfo_visitsInfo_censusBlockGroups_uix] ON [dbo].[visitsType]
        (
        [locid] ASC,
        [vid] ASC,
        [cbgid_loc] ASC,
        [cbgid_orig] ASC
        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
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
        ALTER TABLE [dbo].[relatedBrands]  WITH CHECK ADD  CONSTRAINT [FK_relatedBrands.bid_loc] FOREIGN KEY([bid_loc])
        REFERENCES [dbo].[brandsInfo] ([bid])
        GO
        ALTER TABLE [dbo].[relatedBrands] CHECK CONSTRAINT [FK_relatedBrands.bid_loc]
        GO
        ALTER TABLE [dbo].[relatedBrands]  WITH CHECK ADD  CONSTRAINT [FK_relatedBrands.bid_rel] FOREIGN KEY([bid_rel])
        REFERENCES [dbo].[brandsInfo] ([bid])
        GO
        ALTER TABLE [dbo].[relatedBrands] CHECK CONSTRAINT [FK_relatedBrands.bid_rel]
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
        CREATE OR ALTER PROCEDURE [dbo].[insertRelatedBrands](
        @a_placekey VARCHAR(max),
        @vid INT,
        @locid INT,
        @bid_loc INT,
        @w_daterangestart VARCHAR(max),
        @ak_al_relatedbrand VARCHAR(max),
        @ak_al_relatedbrand_cnt INT,
        @day_week_ind CHAR(1)
        )
        AS
        BEGIN
        DECLARE @bid_rel INT;

        BEGIN

        IF EXISTS (SELECT 1 FROM brandsInfo WHERE brand_name = @ak_al_relatedbrand)
        BEGIN
        SET @bid_rel=(SELECT bid FROM brandsInfo WHERE brand_name=@ak_al_relatedbrand);
        END;
        ELSE
        BEGIN
        INSERT INTO brandsInfo(brand_name)
        VALUES (@ak_al_relatedbrand);
        SET @bid_rel=SCOPE_IDENTITY();
        END;

        INSERT INTO relatedBrands(vid, locid, bid_loc, bid_rel, visit_count, day_week_ind)
        VALUES (@vid, @locid, @bid_loc, @bid_rel, @ak_al_relatedbrand_cnt, @day_week_ind);

        END;
        END;
        ''')

    sql2=('''
        ALTER PROCEDURE [dbo].[insertCategories](
        @locid INT,
        @r_categorytag VARCHAR(max)
        )
        AS
        BEGIN
        DECLARE @cidout INT;

        BEGIN

        IF EXISTS (SELECT 1 FROM categories WHERE (category=@r_categorytag))
        BEGIN
        SET @cidout=(SELECT cid FROM categories WHERE category=@r_categorytag);
        END;
        ELSE
        BEGIN
        INSERT INTO categories(category)
        VALUES (@r_categorytag);
        SET @cidout=SCOPE_IDENTITY();
        INSERT INTO categoriesXref(locid, cid)
        VALUES (@locid, @cidout);
        END;
        END;
        END;
        ''')

    sql3=('''
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

    sql4=('''
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
	    SELECT @nidout AS nidout, @bidout AS bidout, @locidout AS locidout, @cbgidout AS cbgidout, @vidout AS vidout;
        END;
        END;
        ''')

    sql5=('''
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
        ''')

    for query in [sql1,sql2,sql3,sql4,sql5]:
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

    sql_insertVisitsType='''EXECUTE [insertVisitsType] 
        @locid=?
        ,@vid=?
        ,@cbgid_loc=?
        ,@ad_af_visitorcbg=?
        ,@ad_af_visitorcbg_cnt=?
        ,home_work_ind=?
    '''

    sql_insertRelatedBrands='''EXECUTE [insertRelatedBrands] 
        @vid=?
        ,@locid=?
        ,@bid_loc=?
        ,@ak_al_relatedbrand=?
        ,@ak_al_relatedbrand_cnt=?
        ,@day_week_ind=?
    '''

    sql_insertDeviceCount='''EXECUTE [insertDeviceCount] 
        @a_placekey=?
        ,@w_daterangestart=?
        ,@am_devicetype=?
        ,@am_devicetype_cnt=?
    '''

    sql_insertCategories='''EXECUTE [insertCategories] 
        @locid=?
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
        row = cur.fetchone()
        nid, bid, locid, cbgid, vid = row['nidout'], row['bidout'], row['locidout'], row['cbgidout'], row['vidout']
        cur.commit()
        print(row.location_name[:20]+', '+row.street_address+', '+row.city+', '+row.region+' '+str(row.postal_code)+'... '+
             row.date_range_start+": "+str(int(row.normalized_visits_by_state_scaling))+' total visitors...')

        for key, value in json.loads(row.visitor_home_cbgs).items():
            if (key[0]).isalpha() is True: pass
            else:
                values_insertVisitsType_Home = (locid, vid, cbgid, key, int(value), 'h')
                cur.execute(sql_insertVisitsType, values_insertVisitsType_Home)
                cur.commit()
                #print(x)

        for key, value in json.loads(row.visitor_daytime_cbgs).items():
            if (key[0]).isalpha() is True: pass
            else:
                values_insertVisitsType_Work = (locid, vid, cbgid, key, int(value), 'w')
                cur.execute(sql_insertVisitsType, values_insertVisitsType_Work)
                cur.commit()
                #print(x)

        for key, value in json.loads(row.related_same_day_brand).items():
            if (key[0]).isalpha() is True: pass
            else:
                values_insertRelatedBrands_Day = (vid, locid, bid, key, int(value), 'd')
                cur.execute(sql_insertRelatedBrands, values_insertRelatedBrands_Day)
                cur.commit()
                #print(x)

        for key, value in json.loads(row.related_same_week_brand).items():
            if (key[0]).isalpha() is True: pass
            else:
                values_insertRelatedBrands_Week = (vid, locid, bid, key, int(value), 'w')
                cur.execute(sql_insertRelatedBrands, values_insertRelatedBrands_Week)
                cur.commit()
                #print(x)

        for key, value in json.loads(row.device_type).items:
            values_insertDeviceCount = (row.placekey, row.date_range_start, key, int(value))
            cur.execute(sql_insertDeviceCount, values_insertDeviceCount)
            cur.commit()
            #print(x)

        if not pd.isna(row['category_tags']):
            for x in str(row.category_tags).split(','):
                if x != '0':
                    values_insertCategories = (locid, x)
                    cur.execute(sql_insertCategories, values_insertCategories)
                    cur.commit()
                    #print(x)

def main():
    driver = '{SQL Server}'
    server = ''
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