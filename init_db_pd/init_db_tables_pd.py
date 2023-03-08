import pandas as pd

# Create empty dataframes for each table
naicsCodes = pd.DataFrame(columns=['nid', 'top_category', 'sub_category', 'naics_code'],
                          dtype={'nid': 'int', 'top_category': 'object', 'sub_category': 'object', 'naics_code': 'object'}).set_index('nid')

brandsInfo = pd.DataFrame(columns=['bid', 'nid', 'brand_name'],
                          dtype={'bid': 'int', 'nid': 'int', 'brand_name': 'object'}).set_index('bid')

censusBlockGroups = pd.DataFrame(columns=['cbgid', 'cbg_number'],
                                 dtype={'cbgid': 'int', 'cbg_number': 'object'}).set_index('cbgid')

locationInfo = pd.DataFrame(columns=['locid', 'nid', 'bid', 'cbgid', 'placekey', 'location_name',
                                     'latitude', 'longitude', 'street_address', 'city', 'region', 'postal_code', 'phone_number'],
                            dtype={'locid': 'int', 'nid': 'int', 'bid': 'int', 'cbgid': 'int',
                                   'placekey': 'object', 'location_name': 'object', 'latitude': 'object', 'longitude': 'object',
                                   'street_address': 'object', 'city': 'object', 'region': 'object', 'postal_code': 'object',
                                   'phone_number': 'object'}).set_index('locid')

visitsInfo = pd.DataFrame(columns=['vid', 'locid', 'week_begin', 'raw_visit_counts', 'raw_visitor_counts', 'distance_from_home',
                                   'median_dwell', 'normalized_visits_by_state_scaling', 'normalized_visits_by_region_naics_visits',
                                   'normalized_visits_by_region_naics_visitors', 'normalized_visits_by_total_visits',
                                   'normalized_visits_by_total_visitors'],
                          dtype={'vid': 'int', 'locid': 'int', 'week_begin': 'object', 'raw_visit_counts': 'int',
                                 'raw_visitor_counts': 'int', 'distance_from_home': 'int', 'median_dwell': 'float',
                                 'normalized_visits_by_state_scaling': 'float', 'normalized_visits_by_region_naics_visits': 'float',
                                 'normalized_visits_by_region_naics_visitors': 'float', 'normalized_visits_by_total_visits': 'float',
                                 'normalized_visits_by_total_visitors': 'float'}).set_index('vid')

visitsType = pd.DataFrame(columns=['vtid', 'locid', 'vid', 'cbgid', 'visit_count', 'home_work_ind'],
                          dtype={'vtid': 'int', 'locid': 'int', 'vid': 'int', 'cbgid': 'int',
                                 'visit_count': 'int', 'home_work_ind': 'object'}).set_index('vtid')

devices = pd.DataFrame({'did': [1, 2],
                        'device_type': ['android', 'ios']},
                       columns=['did', 'device_type'],
                       dtype={'did': 'int', 'device_type': 'object'}).set_index('did')


deviceLog = pd.DataFrame(columns=['dlid', 'vid', 'did', 'user_count'],
                          dtype={'dlid': 'int', 'vid': 'int', 'did': 'int', 'user_count': 'int'}).set_index('dlid')

categories = pd.DataFrame(columns=['cid', 'category_name'],
                          dtype={'cid': 'int', 'category_name': 'object'}).set_index('cid')

categoriesXref = pd.DataFrame(columns=['cxid', 'locid', 'cid'],
                              dtype={'cxid': 'int', 'locid': 'int', 'cid': 'int'}).set_index('cxid')

relatedBrands = pd.DataFrame(columns=['blid', 'bid', 'vid', 'visit_count', 'day_week_ind'],
                              dtype={'blid': 'int', 'bid': 'int', 'vid': 'int', 'visit_count': 'int', 'day_week_ind': 'object'}).set_index('blid')

