def get_varlists():
    from sqlalchemy import create_engine
    from sqlalchemy_utils import database_exists, create_database
    import psycopg2
    #Connect to database
    username = 'postgres'
    password = 'Charge!0n'     # change this
    host     = 'localhost'
    port     = '5432'            # default port that postgres listens on
    db_name  = 'visa_data'

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
    education_class_query = """
    SELECT DISTINCT foreign_worker_info_education FROM visa_data_table;
    """
    sector_list = pd.read_sql_query(sector_all_query,con)
    education_class_list = pd.read_sql_query(education_class_query, con)
    admit_class_list = pd.read_sql_query(admit_class_query,con)

    sector_list['full_string'] = (sector_list['Sector'].map(str) + ' ' 
                                  + sector_list['Name'].map(str))
    sector_list = sector_list.drop(columns=['index', 'Sector', 'Name', 'sectorcode_int'])
    
    sector_list = sector_list['full_string'].tolist()
    education_class_list = education_class_list['foreign_worker_education'].tolist()
    admit_class_list = admit_class_list['class_of_admission'].tolist()
    
    return (sector_list, admit_class_list, education_level_list)