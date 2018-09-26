from flask import Flask, render_template, request
from calc_probabilities import calc_probabilities
from make_plot import make_plot
from get_varlists import get_varlists
#import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import io
import base64

def highlight_cols(s):
    color = 'lightblue'
    return 'background-color: %s' %color 

app = Flask(__name__, static_url_path='/static')
@app.route('/', methods=['GET', 'POST']) 
def index():           
    sector_list, admit_class_list, education_level_list, citizen_country_list, state_list = get_varlists()
    return render_template('index.html', admit_class_list=admit_class_list, sector_list=sector_list, education_level_list=education_level_list, state_list=state_list, citizen_country_list=citizen_country_list)

@app.route('/recommendation', methods=['GET', 'POST']) 
def recommendation():
    errors = []
    letters = []
    admit_class = []
    sector = []
    edu_level = []
    probs = []
    htmltables = []
    titles = []
    plotscript = []
    plotdiv = []
    agent_used = []
    trends = ''
    if request.method == "POST":
        #get url that the user has entered
        try:
            #get user input from home page form
            admit_class = request.form['admit_class']
            edu_level = request.form['edu_level']
            sector = request.form['sector']
            agent_used = request.form['agent_used']
            work_state = request.form['work_state']
            citizen_country = request.form['citizen_country']

            #calculate probabilities
            probs, top3probs = calc_probabilities(admit_class, edu_level, float(sector[:2]), 
                                                  agent_used, work_state[:2], 
                                                 citizen_country.upper())
            #put probability tables to html form
            #probstrans = probs.transpose()
            htmltables.append(
                            probs.style
                            .applymap(highlight_cols, subset=pd.IndexSlice[[0, 2, 4, 6, 8, 10], :])
                            .set_properties(**{'text-align':'center', 'width':'300px'})
                            .hide_index()
                            .set_table_attributes('align="center"')
                            .render()
                            )
            htmltables.append(
                            top3probs.style
                            .set_properties(**{'text-align':'center', 'width':'150px'})
                            .set_table_attributes('align="center"')
                            .render()
                            )
            #make plot
            plotscript, plotdiv = make_plot(probs)
        except:
            errors.append("Unable to get URL. Please make sure it's valid and try again."
                         )
            print("error")
    return render_template('recommendation.html', errors=errors, admit_class = admit_class, 
                           sector = sector, edu_level = edu_level, agent_used = agent_used,
                           work_state = work_state, citizen_country = citizen_country,
                           tables=htmltables, plotscript = plotscript, plotdiv=plotdiv)
def hello():
    return "Insight web app created by Lauren Kahre."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
