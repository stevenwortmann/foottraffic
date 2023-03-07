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
                                                       row['longitude'], row['street_address'], row['city'],
                                                       row['region'], row['postal_code'], row['phone_number']]

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
                 usecols=list(raw_columns.keys()), dtype=raw_columns
                 ).dropna(subset=['date_range_start'])

df['date_range_start'] = pd.to_datetime(df['date_range_start'].str.slice(stop=10), format='%Y-%m-%d')
df['naics_code'] = df['naics_code'].str[:-2]
df['poi_cbg'] = df['poi_cbg'].str[:-2]

# Iterate over each row in the raw csv and update the dataframes accordingly
for index, row in filename.iterrows():
    nid = add_to_naicsCodes(row, naicsCodes)
    bid = add_to_brandsInfo(row, brandsInfo, nid)
    cbgid = add_to_censusBlockGroups(row, censusBlockGroups)
    add_to_locationInfo(row, locationInfo, naicsCodes, brandsInfo, censusBlockGroups)