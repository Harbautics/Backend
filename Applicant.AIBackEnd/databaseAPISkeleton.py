from flask_mysqldb import MySQL
from flask_restful import Resource, Api
import sys
import subprocess
import re
import os
import shutil

#Flask and MySQL setup
application = app = Flask(__name__)
api = Api(app)

mysql = MySQL()

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'sdocs'
app.config['MYSQL_DB'] = 'TempList'
app.config['MYSQL_HOST'] = 'localhost'
mysql.init_app(app)

#Saves the json sent through the request. Currently labeled
#temp, will be replaced soon with full json
@app.route('/saveTemp', methods=['POST'])
def save_temp():
	#Get the data from the HTTP request
	data = request.get_json(force=True)
	#Connect to MySQL and get the cursor for making SQL Calls
	cursor = mysql.connection.cursor()
	try:	
		#This is a prepared statement, utilizing parameters
		cursor.execute("SELECT * FROM temps WHERE temp = %s", [data["temp"]])
		#If it doesn't exist in the database, insert it
		if cursor.rowcount == 0:
			cursor.execute("INSERT INTO temps ( temp ) VALUES ( %s )", [data['temp']])
			mysql.connection.commit()
			return "Stored!\n"
		else:
			return "Already exists in DB!\n"
	except:
		#Any form of error, inform the user
		return "ERROR! Not Stored!\n"

#Get the Temp object if it exists
@app.route('/getTemp', methods=['POST'])
def get_temp():
	data = request.get_json(force=True)
	cursor = mysql.connection.cursor()
	cursor.execute("SELECT * FROM temps WHERE temp = %s", [data["temp"]])
	if cursor.rowcount == 0:
		return null
	else:
		return cursor.fetchall()

if __name__ == '__main__':
	app.run(debug=True)
