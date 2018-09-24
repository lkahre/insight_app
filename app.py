from flask import Flask, render_template, request
from calc_probabilities import calc_probabilities
from make_plot import make_plot
from get_varlists import get_varlists
#import matplotlib.pyplot as plt
import numpy as np
import io
import base64

app = Flask(__name__, static_url_path='/static')
@app.route('/', methods=['GET', 'POST']) 
def index():           
    sector_list, admit_class_list, education_level_list = get_varlists()
    return render_template('index.html', admit_class_list=admit_class_list, sector_list=sector_list, education_level_list=education_level_list)

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
    #sector_list = []
    #admit_class_list = []
    #education_level_list = []
    trends = ''
    if request.method == "POST":
        #get url that the user has entered
        try:
            #get user input from home page form
            admit_class = request.form['admit_class']
            edu_level = request.form['edu_level']
            sector = request.form['sector']
            #calculate probabilities
            probs, top3probs = calc_probabilities(admit_class, edu_level, float(sector[:2]))
            #put probability tables to html form
            htmltables = [probs.to_html(classes="probs", index=False), 
                          top3probs.to_html(classes="top3probs", index=False)]
            #make plot
            plotscript, plotdiv = make_plot(probs)
        except:
            errors.append("Unable to get URL. Please make sure it's valid and try again."
                         )
            print("error")
    return render_template('recommendation.html', errors=errors, admit_class = admit_class, sector = sector, edu_level = edu_level, tables=htmltables, plotscript = plotscript, plotdiv=plotdiv)
def hello():
    return "Insight web app created by Lauren Kahre."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
