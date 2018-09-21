from flask import Flask, render_template, request
from calc_probabilities import calc_probabilities
from get_varlists import get_varlists
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

app = Flask(__name__, static_url_path='/static')
@app.route('/', methods=['GET', 'POST']) 
def index():
    errors = []
    letters = []
    admit_class = []
    sector = []
    edu_level = []
    probs = []
    htmltables = []
    titles = []
    plot_url = []
    #sector_list = []
    #admit_class_list = []
    #education_level_list = []
    trends = ''
    if request.method == "POST":
        #get url that the user has entered
        try:
            #sector_list, admit_class_list, education_level_list = getvarlists() 
            admit_class = request.form['admit_class']
            edu_level = request.form['edu_level']
            sector = request.form['sector']
            sector = float(sector[:2])
            probs, top3probs = calc_probabilities(admit_class, edu_level, sector)
            htmltables = [probs.to_html(classes="probs"), top3probs.to_html(classes="top3probs")]
            titles = ['Probabilities by Month', 'Top Three Months']
            
            img = io.BytesIO()
            fig = plt.figure(figsize=(9.8,5), dpi=100)
            xaxis_loc = np.arange(12)
            fig.patch.set_facecolor('w')
            plt.plot(xaxis_loc, probs['Probability'])
            plt.ylim([0, 100])
            plt.xticks(xaxis_loc, probs['Month'])
            plt.xlabel('Month')
            plt.ylabel('% Chance of Acceptance')
            plt.title('Visa Chance of Acceptance by Month')
            plt.savefig(img, format='png')
            img.seek(0)        
            plot_url = base64.b64encode(img.getvalue()).decode
        except:
            errors.append("Unable to get URL. Please make sure it's valid and try again."
                         )
            print("error")
    return render_template('index.html', errors=errors, admit_class = admit_class, sector = sector, edu_level = edu_level, tables=htmltables, titles = titles, plot_url = plot_url)
    
def hello():
    return "Insight web app created by Lauren Kahre."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
