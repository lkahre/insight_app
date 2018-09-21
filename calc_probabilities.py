def calc_probabilities(admit_class, education_level, sector):
    import numpy as np
    import pandas as pd
    import math
    import datetime as dt
    from creds import creds
    from sqlalchemy import create_engine
    from sqlalchemy_utils import database_exists, create_database
    import psycopg2
    
    pd.options.display.max_columns = 150
    
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
    
    #Pull model from database
    model_query = """
    SELECT * FROM model_coeff_table;
    """
    model_weights = pd.read_sql_query(model_query,con)
    model_weights = model_weights.drop(columns=['index'])
    
    #Construct user data dictionary for entry variables
    user_data = {'class_of_admission': [admit_class], 
             'foreign_worker_info_education': [education_level], 
             'sector_code': [sector]}
    
    #Initialize user data dummy dataframe
    user_dummy_data = np.zeros([12, len(model_weights.columns.values)], dtype=int)
    user_dummy_df = pd.DataFrame(user_dummy_data, columns=model_weights.columns)

    #Do something clever to automate dummy variable on/off values
    user_coa = 'class_of_admission_' + user_data['class_of_admission'][0]
    user_loe = 'foreign_worker_info_education_' + user_data['foreign_worker_info_education'][0]
    user_sector = 'sector_code_' + str(user_data['sector_code'][0])

    for column in user_dummy_df:
        if user_coa == column:
            user_dummy_df[column] = 1
        if user_loe == column:
            user_dummy_df[column] = 1
        if user_sector == column:
            user_dummy_df[column] = 1
            
    for month in range(1, 13):
        monthstring = 'case_received_month_' + str(float(month))
        user_dummy_df.set_value(month-1, monthstring, 1)
        
    #Apply the model
    prob_accept = np.zeros(12)
    
    for month in range(1, 13):
        user_datamonth = user_dummy_df.iloc[month-1, :] 
        model_result = user_datamonth * model_weights
        prob_accept[month-1] = model_result.sum(axis=1)
        prob_accept[month-1] = math.exp(prob_accept[month-1])
        prob_accept[month-1] = prob_accept[month-1]/(1+prob_accept[month-1])
        prob_accept[month-1] = prob_accept[month-1]*100
        
    prob_accept = np.around(prob_accept, 2)
    months_list = []
    for i in range(1, 13):
        months_list.append(dt.date(2008, i, 1).strftime('%b'))

    result_df = pd.DataFrame({'Month': months_list, 'Probability': prob_accept})
    top3_df = result_df.nlargest(3, 'Probability')
    
    return result_df, top3_df