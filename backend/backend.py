import psycopg2
from flask import Flask, request
import os
import requests
import json

randomJokeApi = "https://official-joke-api.appspot.com/random_joke"
jokeIdApi = "https://official-joke-api.appspot.com/jokes/"
app = Flask(__name__)


# Define the connection parameters
db_params = {
    'dbname': 'dbname',
    'user': 'dbuser',
    'password': 'dbpassword',
    'host': 'database',  # Use 'localhost' for a local database
    'port': '5432',       # Default PostgreSQL port
}

try:
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()
    create_table_query = '''
    CREATE TABLE jokes (
        id SERIAL PRIMARY KEY,
        joke_id INT,
        setup VARCHAR(255),
        punchline VARCHAR(255)
    )
    '''
    cursor.execute(create_table_query)
    connection.commit()
    cursor.close()
    connection.close()

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL:", error)

def addJokeToDb(id, setup, punchline):
    try:
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()
        insert_query = "INSERT INTO jokes (joke_id, setup, punchline) VALUES (%s, %s, %s)"
        data_to_insert = (id, setup, punchline)
        cursor.execute(insert_query, data_to_insert)
        connection.commit()
        cursor.close()
        connection.close()

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL:", error)

def getAllJokes():
    try:
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()
        query = "SELECT * FROM jokes"
        cursor.execute(query)
        results = cursor.fetchall()

        columns = [desc[0] for desc in cursor.description]

        data = []
        for row in results:
            data.append(dict(zip(columns, row)))

        json_data = json.dumps(data, indent=4)


        cursor.close()
        connection.close()
        return json_data

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL:", error)

def getRandomJoke():
    response = requests.get(randomJokeApi)
    joke = response.json()
    return joke

def getJokeById(id):
    response = requests.get(jokeIdApi + str(id))
    joke = response.json()
    return joke

@app.route("/randomJoke/", methods=['GET'])
def get_randome_joke():
    return json.dumps(getRandomJoke())

@app.route("/jokeById/<jokeId>", methods=['GET'])
def get_joke_id(jokeId):
    joke = getJokeById(jokeId)
    addJokeToDb(joke['id'], joke['setup'], joke['punchline'])
    return joke

@app.route("/getDb", methods=['GET'])
def getDb():
    jokes = getAllJokes()
    return jokes

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 30002))
    app.run(debug=True, host='0.0.0.0', port=port)