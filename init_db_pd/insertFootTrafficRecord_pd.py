import pandas as pd
import json

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
def add_to_brandsInfo(brand_name, brandsInfo, nid):
    existing_row = brandsInfo.loc[(brandsInfo['brand_name'] == brand_name)]
    if existing_row.empty:
        bid = get_next_pk(brandsInfo)
        brandsInfo.loc[bid] = [nid, brand_name]
        return bid
    else:
        if len(existing_row.index) > 0:
            if pd.isnull(existing_row['nid'].iloc[0]):
                existing_row.at[existing_row.index[0], 'nid'] = nid
                return existing_row.index[0]
            else:
                return existing_row.index[0]
        else:
            return None

# Define a function to add a new record to the censusBlockGroups dataframe if it doesn't already exist
def add_to_censusBlockGroups(poi_cbg, censusBlockGroups):
    existing_row = censusBlockGroups.loc[censusBlockGroups['cbg_number'] == poi_cbg]
    if existing_row.empty:
        cbgid = get_next_pk(censusBlockGroups)
        censusBlockGroups.loc[cbgid] = poi_cbg
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

# Define a function to add a new record to the categories dataframe if it doesn't already exist
def add_to_categories(category_name, categories):
    existing_row = categories.loc[categories['category_name'] == category_name]
    if existing_row.empty:
        cid = get_next_pk(categories)
        categories.loc[cid] = category_name
        return cid
    else:
        return existing_row.index[0]

# Define a function to add a new record to the categoriesXref dataframe if it doesn't already exist
def add_to_categoriesXref(locid, cid, categoriesXref):
    existing_row = categoriesXref.loc[(categoriesXref['locid'] == locid) &
                                      (categoriesXref['cid'] == cid)]
    if existing_row.empty:
        cxid = get_next_pk(categoriesXref)
        categoriesXref.loc[cxid] = [locid, cid]
        return cxid
    else:
        return existing_row.index[0]
    
def add_to_relatedBrands_day(vid, brand_name, visit_count, relatedBrands, brandsInfo):
    bid = add_to_brandsInfo(brand_name, brandsInfo, None) # fetch brand id from brandsInfo, or create new brand id (naics id will be null in this case)
    existing_row = relatedBrands.loc[(relatedBrands['vid'] == vid) &
                                  (relatedBrands['bid'] == bid)]
    if existing_row.empty:
        blid = get_next_pk(relatedBrands)
        relatedBrands.loc[blid] = [bid, vid, visit_count, 'd']
        return blid
    else:
        return existing_row.index[0]
    
def add_to_relatedBrands_week(vid, brand_name, visit_count, relatedBrands, brandsInfo):
    bid = add_to_brandsInfo(brand_name, brandsInfo, None) # fetch brand id from brandsInfo, or create new brand id (naics id will be null in this case)
    existing_row = relatedBrands.loc[(relatedBrands['vid'] == vid) &
                                  (relatedBrands['bid'] == bid)]
    if existing_row.empty:
        rbid = get_next_pk(relatedBrands)
        relatedBrands.loc[rbid] = [bid, vid, visit_count, 'w']
        return rbid
    else:
        return existing_row.index[0]
    
def add_to_deviceLog(vid, device_name, device_count, devices):
    did = devices.loc[devices['device_type'] == device_name]
    if did.empty: # new non-ios/android device
        new_did = get_next_pk(devices)
        devices.loc[new_did] = device_name
        did = new_did
    else:
        did = did.index[0]
    existing_row = deviceLog.loc[(deviceLog['did'] == did) &
                                 (deviceLog['vid'] == vid)]
    if existing_row.empty:
        dlid = get_next_pk(deviceLog)
        deviceLog.loc[dlid] = [vid, did, device_count]
        return dlid
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
    bid = add_to_brandsInfo(row['brands'], brandsInfo, nid)
    cbgid = add_to_censusBlockGroups(row['poi_cbg'], censusBlockGroups)
    locid = add_to_locationInfo(row, locationInfo, nid, bid, cbgid)
    vid = add_to_visitsInfo(row, visitsInfo, locid)

    for key, value in json.loads(row.visitor_home_cbgs).items():
        add_to_visitsType_home(locid, vid, cbgid, key, value, visitsType, censusBlockGroups)

    for key, value in json.loads(row.visitor_daytime_cbgs).items():
        add_to_visitsType_work(locid, vid, cbgid, key, value, visitsType, censusBlockGroups)

    for key, value in json.loads(row.related_same_day_brand).items():
        add_to_relatedBrands_day(vid, key, value, relatedBrands, brandsInfo)

    for key, value in json.loads(row.related_same_week_brand).items():
        add_to_relatedBrands_week(vid, key, value, relatedBrands, brandsInfo)

    for key, value in json.loads(row.device_type).items():
        add_to_deviceLog(vid, key, value, devices)

    if not pd.isna(row['category_tags']):
        for x in row.category_tags.split(','):
            cid = add_to_categories(x, categories)
            add_to_categoriesXref(locid, cid, categoriesXref)