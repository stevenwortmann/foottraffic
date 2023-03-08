# Define a function to get the next available primary key for a given dataframe
def get_next_pk(df):
    if df.empty:
        return 1
    else:
        return df.index.max() + 1
    
# Define a function to add a new record to the naicsCodes dataframe if it doesn't already exist
def add_to_naicsCodes(row, naicsCodes):
    existing_row = naicsCodes.loc[(naicsCodes['naics_code'] == row['naics_code']) &
                                  (naicsCodes['top_category'] == row['top_category']) &
                                  (naicsCodes['sub_category'] == row['sub_category'])]
    if existing_row.empty:
        nid = get_next_pk(naicsCodes)
        naicsCodes.loc[nid] = [row['naics_code'], row['top_category'], row['sub_category']]
        return nid
    else:
        return existing_row.index[0]

# Define a function to add a new record to the brandsInfo dataframe if it doesn't already exist
def add_to_brandsInfo(row, brandsInfo, nid):
    existing_row = brandsInfo.loc[(brandsInfo['brand_name'] == row['brands'])]
    if existing_row.empty:
        bid = get_next_pk(brandsInfo)
        brandsInfo.loc[bid] = [nid, row['brands']]
        return bid
    else:
        if len(existing_row.index) > 0:
            return existing_row.index[0]
        else:
            return None

# Define a function to add a new record to the censusBlockGroups dataframe if it doesn't already exist
def add_to_censusBlockGroups(row, censusBlockGroups):
    existing_row = censusBlockGroups.loc[censusBlockGroups['cbg_number'] == row['poi_cbg']]
    if existing_row.empty:
        cbgid = get_next_pk(censusBlockGroups)
        censusBlockGroups.loc[cbgid] = [row['poi_cbg']]
        return cbgid
    else:
        return existing_row.index[0]

# Define a function to add a new record to the locationInfo dataframe if it doesn't already exist
def add_to_locationInfo(row, locationInfo, nid, bid, cbgid):
    existing_row = locationInfo.loc[locationInfo['placekey'] == row['placekey']]
    if existing_row.empty:
        locid = get_next_pk(locationInfo)
        locationInfo.loc[locid] = [nid, bid, cbgid, row['placekey'], row['location_name'], row['latitude'],
                                    row['longitude'], row['street_address'], row['city'], row['region'], row['postal_code'], row['phone_number']]
        return locid
    else:
        return existing_row.index[0]

# Define a function to add a new record to the visitsInfo dataframe if it doesn't already exist
def add_to_visitsInfo(row, visitsInfo, locid):
    existing_row = visitsInfo.loc[(visitsInfo['locid'] == locid) &
                                  (visitsInfo['week_begin'] == row['date_range_start'])]
    if existing_row.empty:
        vid = get_next_pk(visitsInfo)
        visitsInfo.loc[vid] = [locid, row['date_range_start'], row['raw_visit_counts'], row['raw_visitor_counts'], row['distance_from_home'],
                                   row['median_dwell'], row['normalized_visits_by_state_scaling'], row['normalized_visits_by_region_naics_visits'],
                                   row['normalized_visits_by_region_naics_visitors'], row['normalized_visits_by_total_visits'],
                                   row['normalized_visits_by_total_visitors']]
        return vid
    else:
        return existing_row.index[0]

# Define a function to add a new 'home' record to the visitsType dataframe if it doesn't already exist
def add_to_visitsType_home(locid, vid, cbgid_loc, cbg_h, cbg_h_count, visitsType, censusBlockGroups):
    cbgid_h = add_to_censusBlockGroups(cbg_h, censusBlockGroups) # fetch origin cbgid from censusBlockGroups, or create new cbgid
    existing_row = visitsType.loc[(visitsType['vid'] == vid) &
                                  (visitsType['cbgid_orig'] == cbgid_h) &
                                  (visitsType['cbgid_loc'] == cbgid_loc)]
    if existing_row.empty:
        vtid = get_next_pk(visitsType)
        visitsType.loc[vtid] = [locid, vid, cbgid_loc, cbgid_h, cbg_h_count, 'h']
        return vtid
    else:
        return existing_row.index[0]

# Define a function to add a new 'work' record to the visitsType dataframe if it doesn't already exist
def add_to_visitsType_work(locid, vid, cbgid_loc, cbg_w, cbg_w_count, visitsType, censusBlockGroups):
    cbgid_w = add_to_censusBlockGroups(cbg_w, censusBlockGroups) # fetch origin cbgid from censusBlockGroups, or create new cbgid
    existing_row = visitsType.loc[(visitsType['vid'] == vid) &
                                  (visitsType['cbgid_orig'] == cbgid_w) &
                                  (visitsType['cbgid_loc'] == cbgid_loc)]
    if existing_row.empty:
        vtid = get_next_pk(visitsType)
        visitsType.loc[vtid] = [locid, vid, cbgid_loc, cbgid_w, cbg_w_count, 'w']
        return vtid
    else:
        return existing_row.index[0]

raw_columns = {
    'placekey': str,
    'location_name': str,
    'brands': str,
    'top_category': str,
    'sub_category': str,
    'naics_code': str,
    'latitude': str,
    'longitude': str,
    'street_address': str,
    'city': str,
    'region': str,
    'postal_code': str,
    'phone_number': str,
    'category_tags': str,
    'date_range_start': str,
    'raw_visit_counts': 'float64',
    'raw_visitor_counts': 'float64',
    'poi_cbg': str,
    'visitor_home_cbgs': str,
    'visitor_daytime_cbgs': str,
    'distance_from_home': 'float64',
    'median_dwell': 'float64',
    'related_same_day_brand': str,
    'related_same_week_brand': str,
    'device_type': str,
    'normalized_visits_by_state_scaling': 'float64',
    'normalized_visits_by_region_naics_visits': 'float64',
    'normalized_visits_by_region_naics_visitors': 'float64',
    'normalized_visits_by_total_visits': 'float64',
    'normalized_visits_by_total_visitors': 'float64'
}

df = pd.read_csv(r"path\to\csv_file.csv",
                 usecols=list(raw_columns.keys()), dtype=raw_columns, nrows=50
                 ).dropna(subset=['date_range_start'])

df['date_range_start'] = pd.to_datetime(df['date_range_start'].str.slice(stop=10), format='%Y-%m-%d')

for col in df.columns:
    if df[col].dtype == 'object':  # check if column contains strings
        df[col] = df[col].str.rstrip('.0')

# Iterate over each row in the raw csv and update the dataframes accordingly
for index, row in df.iterrows():
    nid = add_to_naicsCodes(row, naicsCodes)
    bid = add_to_brandsInfo(row, brandsInfo, nid)
    cbgid = add_to_censusBlockGroups(row['poi_cbg'], censusBlockGroups)
    locid = add_to_locationInfo(row, locationInfo, nid, bid, cbgid)
    vid = add_to_visitsInfo(row, visitsInfo, locid)
    for x in row.visitor_home_cbgs.split(','):
            if x!= "{}":
                x = (x.replace("{","")).replace('''"''',"").replace("}","").split(':')
                if (x[0][0]).isalpha() is True:
                    pass # exclude non-US districts/blocks
                else:
                     add_to_visitsType_home(locid, vid, cbgid, x[0], x[1], visitsType, censusBlockGroups)
    for x in row.visitor_daytime_cbgs.split(','):
            if x!= "{}":
                x = (x.replace("{","")).replace('''"''',"").replace("}","").split(':')
                if (x[0][0]).isalpha() is True:
                    pass # exclude non-US districts/blocks
                else:
                     add_to_visitsType_work(locid, vid, cbgid, x[0], x[1], visitsType, censusBlockGroups)