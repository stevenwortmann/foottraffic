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