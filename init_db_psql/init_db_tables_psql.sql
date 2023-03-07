CREATE TABLE IF NOT EXISTS naicsCodes (
    nid INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    top_category VARCHAR(100) NOT NULL,
    sub_category VARCHAR(100),
    naics_code VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS brandsInfo (
    bid INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nid INT REFERENCES naicsCodes (nid) ON DELETE CASCADE,
    brand_name VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS censusBlockGroups (
    cbgid INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    cbg_number VARCHAR(12) NOT NULL
);

CREATE TABLE IF NOT EXISTS locationInfo (
    locid INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nid INT REFERENCES naicsCodes (nid) ON DELETE CASCADE,
    bid INT REFERENCES brandsInfo (bid) ON DELETE CASCADE,
    cbgid INT REFERENCES censusBlockGroups (cbgid) ON DELETE CASCADE,
    placekey VARCHAR(20) NOT NULL,
    location_name VARCHAR(100) NOT NULL,
    latitude VARCHAR(15) NOT NULL,
    longitude VARCHAR(15) NOT NULL,
    street_address VARCHAR(10) NOT NULL,
    city VARCHAR(50) NOT NULL,
    region VARCHAR(5) NOT NULL,
    postal_code VARCHAR(5) NOT NULL,
    phone_number VARCHAR(11)
);

CREATE TABLE IF NOT EXISTS visitsInfo (
    vid INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    locid INT REFERENCES locationInfo (locid) ON DELETE CASCADE,
    week_begin DATE NOT NULL,
    raw_visit_counts INT NOT NULL,
    raw_visitor_counts INT NOT NULL,
    distance_from_home INT NOT NULL,
    median_dwell FLOAT,
    normalized_visits_by_state_scaling FLOAT NOT NULL,
    normalized_visits_by_region_naics_visits FLOAT NOT NULL,
    normalized_visits_by_region_naics_visitors FLOAT NOT NULL,
    normalized_visits_by_total_visits FLOAT NOT NULL,
    normalized_visits_by_total_visitors FLOAT NOT NULL
);

CREATE TABLE IF NOT EXISTS visitsType (
    vtid INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    locid INT REFERENCES locationInfo (locid) ON DELETE CASCADE,
    vid INT REFERENCES visitsInfo (vid) ON DELETE CASCADE,
    cbgid INT REFERENCES censusBlockGroups (cbgid) ON DELETE CASCADE,
    visit_count INT NOT NULL,
    home_work_ind CHAR(1)
);

CREATE TABLE IF NOT EXISTS devices (
    did INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    device_type VARCHAR(7) NOT NULL
);

CREATE TABLE IF NOT EXISTS deviceLog (
    dlid INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    vid INT REFERENCES visitsInfo (vid) ON DELETE CASCADE,
    did INT REFERENCES devices (did) ON DELETE CASCADE,
    user_count INT NOT NULL
);

CREATE TABLE IF NOT EXISTS categories (
    cid INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS categoriesXref (
    cxid INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    locid INT REFERENCES locationInfo (locid) ON DELETE CASCADE,
    cid INT REFERENCES categoriesInfo (cid) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS relatedBrands (
    blid INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    bid INT REFERENCES brandsInfo (bid) ON DELETE CASCADE,
    vid INT REFERENCES visitsInfo (vid) ON DELETE CASCADE,
    visit_count INT NOT NULL,
    day_week_ind CHAR(1)
);

INSERT INTO devices (device_type) VALUES ('android') ON CONFLICT DO NOTHING;
INSERT INTO devices (device_type) VALUES ('ios') ON CONFLICT DO NOTHING;