def get_varlists():
    from sqlalchemy import create_engine
    from sqlalchemy_utils import database_exists, create_database
    import psycopg2
    import pandas as pd
    from creds import creds
    from countrydict import us_abbrev_state
    
    username = creds['username']
    password = creds['password']
    host = creds['host']
    port = creds['port']
    db_name = creds['db_name']

    engine = create_engine( 'postgresql://{}:{}@{}:{}/{}'.format(username, 
                                                                 password, 
                                                                 host, 
                                                                 port, 
                                                                 db_name))
    if not database_exists(engine.url):
        create_database(engine.url)
    
    con = None
    con = psycopg2.connect(database = db_name, user = username, host=host, password=password)
    
    sector_all_query = """
    SELECT * FROM sector_code_dict;
    """
    admit_class_query = """
    SELECT DISTINCT class_of_admission FROM visa_data_table;
    """
    education_level_query = """
    SELECT DISTINCT foreign_worker_info_education FROM visa_data_table;
    """
    citizen_country_query = """
    SELECT DISTINCT country_of_citizenship FROM visa_data_table;
    """
    work_state_query = """
    SELECT DISTINCT job_info_work_state FROM visa_data_table;
    """
    sector_list = pd.read_sql_query(sector_all_query,con)
    education_level_list = pd.read_sql_query(education_level_query, con)
    admit_class_list = pd.read_sql_query(admit_class_query,con)
    citizen_country_list = pd.read_sql_query(citizen_country_query,con)
    work_state_list = pd.read_sql_query(work_state_query,con)
    
    citizen_country_list.dropna(axis=0, inplace=True)
    work_state_list.dropna(axis=0, inplace=True)

    sector_list['full_string'] = (sector_list['Sector'].map(str) + ' ' 
                                  + sector_list['Name'].map(str))
    sector_list = sector_list.drop(columns=['index', 'Sector', 'Name', 'sectorcode_int'])
    
    sector_list = sorted(sector_list['full_string'].tolist())
    #education_level_list = education_level_list['foreign_worker_info_education'].tolist()
    education_level_list = ['Doctorate', "Master's", "Bachelor's", "Associate's", 'High School',
                            'Other', 'None']
    citizen_country_list = sorted(citizen_country_list['country_of_citizenship'].tolist())
    #admit_class_list = admit_class_list['class_of_admission'].tolist()
    admit_class_list = ['H-1B', 'Other', 'Not in USA']
    
    state_list = []
    for abbrev in us_abbrev_state:
        statestring = abbrev + ' ' + us_abbrev_state[abbrev]
        state_list.append(statestring)
    
    for i in range(len(citizen_country_list)):
        citizen_country_list[i] = citizen_country_list[i].title()        
        
    #education_level_list.pop(1)   #remove null value if taken automatically from databaseS
    
    return sector_list, admit_class_list, education_level_list, citizen_country_list, state_list