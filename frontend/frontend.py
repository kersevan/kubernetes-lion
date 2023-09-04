from flask import Flask, render_template, request
import os
import requests
import json

backendRandom = "http://backend:30002/randomJoke"
backendId = "http://backend:30002/jokeById"
backendDb = "http://backend:30002/getDb"
app = Flask(__name__)

def getRandomJoke():
    response = requests.get(backendRandom)
    joke = response.json()
    return joke

def getJokeById(id):
    response = requests.get(f"{backendId}/{id}")
    joke = response.json()
    return joke

def getDb():
    response = requests.get(backendDb)
    joke = response.json()
    return joke

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/randomJoke", methods=['GET'])
def get_random_joke():
    joke = getRandomJoke()
    setup, punchline = joke["setup"], joke["punchline"]
    return render_template('joke.html', setup=setup, punchline=punchline)

@app.route("/", methods=['POST'])
def get_joke_id():
    jokeId = int(request.form['jokeId'])
    joke = getJokeById(jokeId)
    setup, punchline = joke["setup"], joke["punchline"]
    return render_template('joke.html', setup=setup, punchline=punchline)

@app.route("/getDb", methods=['GET'])
def get_db():
    jokes = getDb()
    return render_template('db.html', jokes=json.dumps(jokes))

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 30001))
    app.run(debug=True, host='0.0.0.0', port=port)