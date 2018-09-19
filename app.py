from flask import Flask
app = Flask(__name__)
@app.route('/')
def hello():
    return "Insight web app created by Lauren Kahre."

if __name__ == '__main_':
    app.run()

app.run(port=5000)
