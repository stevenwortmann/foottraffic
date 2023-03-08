import pandas as pd

# Create empty dataframes for each table
naicsCodes = pd.DataFrame(columns=['nid', 'naics_code', 'top_category', 'sub_category']).set_index('nid')

brandsInfo = pd.DataFrame(columns=['bid', 'nid', 'brand_name']).set_index('bid')

censusBlockGroups = pd.DataFrame(columns=['cbgid', 'cbg_number']).set_index('cbgid')

locationInfo = pd.DataFrame(columns=['locid', 'nid', 'bid', 'cbgid', 'placekey', 'location_name',
                                     'latitude', 'longitude', 'street_address', 'city', 'region', 'postal_code', 'phone_number']).set_index('locid')

visitsInfo = pd.DataFrame(columns=['vid', 'locid', 'week_begin', 'raw_visit_counts', 'raw_visitor_counts', 'distance_from_home',
                                   'median_dwell', 'normalized_visits_by_state_scaling', 'normalized_visits_by_region_naics_visits',
                                   'normalized_visits_by_region_naics_visitors', 'normalized_visits_by_total_visits',
                                   'normalized_visits_by_total_visitors']).set_index('vid')

visitsType = pd.DataFrame(columns=['vtid', 'locid', 'vid', 'cbgid', 'visit_count', 'home_work_ind']).set_index('vtid')

devices = pd.DataFrame({'did': [1, 2],
                        'device_type': ['android', 'ios']}).set_index('did')

deviceLog = pd.DataFrame(columns=['dlid', 'vid', 'did', 'user_count']).set_index('dlid')

categories = pd.DataFrame(columns=['cid', 'category_name']).set_index('cid')

categoriesXref = pd.DataFrame(columns=['cxid', 'locid', 'cid']).set_index('cxid')

relatedBrands = pd.DataFrame(columns=['blid', 'bid', 'vid', 'visit_count', 'day_week_ind']).set_index('blid')