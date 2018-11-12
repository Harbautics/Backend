from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
import functions

#Flask and MySQL setup
application = app = Flask(__name__)
api = Api(app)
CORS(app)

#MySQL setup
'''
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'sdocs123'
app.config['MYSQL_DB'] = 'AAIDB'
app.config['MYSQL_HOST'] = 'aa5mho3pd0cv71.czzaljfmuz2x.us-east-2.rds.amazonaws.com'
app.config['MYSQL_PORT'] = 3306
'''

mysql = MySQL()

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'sdocs'
app.config['MYSQL_DB'] = 'AAIDB'
app.config['MYSQL_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/CreateOrg', methods=['POST'])
@cross_origin(origin='*')
def post_create_org():
	data = request.get_json()
	cursor = mysql.connection.cursor()
	cursor.execute("INSERT INTO Organizations ( name, description ) VALUES ( %s, %s )", [data['org_name'], data['description']])
	mysql.connection.commit()
	cursor.execute("SELECT * FROM Organizations WHERE name = %s", [data["org_name"]])
	results = cursor.fetchall()
	for row in results:
		retId = row[0]
	return retId

@app.route('/CreateUser', methods=['POST'])
@cross_origin(origin='*')
def post_create_user():
	data = request.form
	cursor = mysql.connection.cursor()
	cursor.execute("INSERT INTO Users ( name, email, password ) VALUES ( %s, %s, %s )", [data['username'], data['email'], data['password']])
	mysql.connection.commit()
	cursor.execute("SELECT * FROM Users WHERE name = %s", [data["email"]])
	results = cursor.fetchall()
	for row in results:
		retId = row[0]
	return retId
	return None

@app.route('/CreateSubmission', methods=['POST'])
@cross_origin(origin='*')
def post_create_submission():
	data = request.form
	#cursor = mysql.connection.cursor()
	return None

@app.route('/CreatePosting', methods=['POST'])
@cross_origin(origin='*')
def post_create_posting():
	data = request.form
	#cursor = mysql.connection.cursor()
	return None

if __name__ == '__main__':
	app.run(debug=True)
