from flask import Flask, render_template, request
from get_letters import get_letters
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])

def index():
    errors = []
    letters = []
    trends = ''
    if request.method == "POST":
        #get url that the user has entered
        try:
            word = request.form['word']
            letters = get_letters(word)
            #print statements just print to terminal
            print("word was:")
            print(word)
        except:
            errors.append("Unable to get URL. Please make sure it's valid and try again."
                         )
            print("error")
    return render_template('index.html', letters=letters, errors=errors)
    
def hello():
    return "Insight web app created by Lauren Kahre."

if __name__ == '__main_':
    app.run()

app.run()
