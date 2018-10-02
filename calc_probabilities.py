def calc_probabilities(admit_class, education_level, sector, agent_used): #, 
                       #work_state): #, citizen_country): #, business_size):
    import numpy as np
    import pandas as pd
    import math
    import datetime as dt
    #from creds import creds
    from sqlalchemy import create_engine
    from sqlalchemy_utils import database_exists, create_database
    from urllib.parse import urlparse
    import os
    import psycopg2
    
    #pd.options.display.max_columns = 150
    database_url = os.environ.get('DATABASE_URL', None)
    result = urlparse(database_url)
    username = result.username
    password = result.password
    host = result.hostname
    port = '5432'
    db_name = result.path[1:]
    
    con = None
    con = psycopg2.connect(database = db_name, user = username, host=host, password=password)
    
    #Pull model from database
    model_query = """
    SELECT * FROM model_coeff_table;
    """
    model_weights = pd.read_sql_query(model_query,con)
    model_weights = model_weights.drop(columns=['index'])
    print(model_weights)
    
    #Construct user data dictionary for entry variables
    user_data = {'class_of_admission': [admit_class], 
             'foreign_worker_info_education': [education_level], 
             'sector_code': [sector]} #, 'job_info_work_state': [work_state]}
    #'country_of_citizenship':[citizen_country], 'business_type': [business_size]}
    
    #Initialize user data dummy dataframe
    user_dummy_data = np.zeros([12, len(model_weights.columns.values)], dtype=int)
    user_dummy_df = pd.DataFrame(user_dummy_data, columns=model_weights.columns)

    #Do something clever to automate dummy variable on/off values
    user_coa = 'class_of_admission_' + user_data['class_of_admission'][0]
    user_loe = 'foreign_worker_info_education_' + user_data['foreign_worker_info_education'][0]
    user_sector = 'sector_code_' + str(user_data['sector_code'][0])
    #user_state = 'job_info_work_state_' + str(user_data['job_info_work_state'][0])
    #user_country = 'country_of_citizenship_' + str(user_data['country_of_citizenship'][0])
    #user_busisize = 'business_type_' + str(user_data['business_type'][0])
    
    #Initialize agent case; no agent case already at zero
    if agent_used == 'yes':
        user_dummy_df['agent_used_1'] = 1

    for column in user_dummy_df:
        if user_coa == column:
            user_dummy_df[column] = 1
        if user_loe == column:
            user_dummy_df[column] = 1
        if user_sector == column:
            user_dummy_df[column] = 1
        #if user_state == column:
        #    user_dummy_df[column] = 1
        #if user_country == column:
        #    user_dummy_df[column] = 1
        #if user_busisize == column:
        #    user_dummy_df[column] = 1
            
    for month in range(1, 13):
        monthstring = 'case_received_month_' + str(float(month))
        user_dummy_df.set_value(month-1, monthstring, 1)
        
    #Apply the model
    prob_accept = np.zeros(12)
    
    for month in range(1, 13):
        user_datamonth = user_dummy_df.iloc[month-1, :]
        model_result = user_datamonth * model_weights
        #Probabilites 
        prob_accept[month-1] = model_result.sum(axis=1)
        prob_accept[month-1] = math.exp(prob_accept[month-1])
        prob_accept[month-1] = prob_accept[month-1]/(1+prob_accept[month-1])
        prob_accept[month-1] = prob_accept[month-1]*100
        
    prob_accept = np.around(prob_accept, 2)
    
    #months_list = []
    months_list_fullname = []
    for i in range(1, 13):
        #months_list.append(dt.date(2008, i, 1).strftime('%b'))
        months_list_fullname.append(dt.date(2008, i, 1).strftime('%B'))

    result_df = pd.DataFrame({'Month': months_list_fullname, 
                              'Percent Chance': prob_accept})
    top3_df = result_df.nlargest(3, 'Percent Chance')
    bot3_df = result_df.nsmallest(3, 'Percent Chance')
    #top3_dfnum = len(top3_df)
    top3_df.index = range(1, 4)
    bot3_df.index = range(1, 4)
    #result_df = result_df.style.set_properties(**{'text-align': 'center'})
    #result_df.render()
    
    return result_df, top3_df, bot3_df