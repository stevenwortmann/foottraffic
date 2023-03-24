USE [Foot_Traffic]

DROP TABLE IF EXISTS[dbo].[visitsType]
DROP TABLE IF EXISTS[dbo].[relatedBrands]
DROP TABLE IF EXISTS[dbo].[categoriesXref]
DROP TABLE IF EXISTS[dbo].[categories]
DROP TABLE IF EXISTS[dbo].[devices]
DROP TABLE IF EXISTS[dbo].[deviceLog]
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
	[bid] [int] NOT NULL,
	[vid] [int] NOT NULL,
	[locid] [int] NOT NULL,
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
	[bid] ASC,
	[vid] ASC,
	[locid] ASC
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