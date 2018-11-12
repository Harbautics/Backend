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

#curl --request POST -H "Content-Type: application/json" -d '{"org_name":"BobsClub","description":"This is Bobs club"}' http://127.0.0.1:5000/CreateOrg
@app.route('/CreateOrg', methods=['POST'])
@cross_origin(origin='*')
def post_create_org():
	data = request.get_json()
	cursor = mysql.connection.cursor()
	cursor.execute("INSERT INTO Organizations ( name, description ) VALUES ( %s, %s )", [data['org_name'], data['description']])
	mysql.connection.commit()
	cursor.execute("SELECT * FROM Organizations WHERE name = %s", [data["org_name"]])
	results = cursor.fetchall()
	retId = 0
	for row in results:
		retId = row[0]
	return str(retId) + "\n"

#curl --request POST -H "Content-Type: application/json" -d '{"username":"bob","email":"bob@bob.com","password":"bob!"}' http://127.0.0.1:5000/CreateUser
@app.route('/CreateUser', methods=['POST'])
@cross_origin(origin='*')
def post_create_user():
	data = request.get_json()
	cursor = mysql.connection.cursor()
	cursor.execute("INSERT INTO Users ( name, email, password ) VALUES ( %s, %s, %s )", [data['username'], data['email'], data['password']])
	mysql.connection.commit()
	cursor.execute("SELECT * FROM Users WHERE email = %s", [data["email"]])
	results = cursor.fetchall()
	retId = 0	
	for row in results:
		retId = row[0]
	return str(retId) + "\n"

@app.route('/CreateSubmission', methods=['POST'])
@cross_origin(origin='*')
def post_create_submission():
	data = request.get_json()
	cursor = mysql.connection.cursor()

	#get User id:
	cursor.execute("SELECT * FROM Users WHERE email = %s", [data["email"]])
	results = cursor.fetchall()
	userId = -1
	for row in results:
		userId = row[0]
	
	if userId == -1:
		return "USER NOT FOUND"
	
	#get org id
	cursor.execute("SELECT * FROM Organizations WHERE name = %s", [data["org_name"]])
	results = cursor.fetchall()
	orgId = -1
	for row in results:
		orgId = row[0]

	if orgId == -1:
		return "ORG NOT FOUND"

	#get post id
	cursor.execute("SELECT * FROM Postings WHERE org_id = %s AND name = %s", [orgId, data['pos_name']])
	results = cursor.fetchall()
	postId = -1	
	for row in results:
		postId = row[0]

	if postId == -1:
		return "POST NOT FOUND"

	cursor.execute("INSERT INTO Applicants ( user_id, post_id ) VALUES ( %s, %s )", [userId, postId])
	mysql.connection.commit()
	
	questionCount = 0
	for answer in data['answers']:
		cursor.execute("INSERT INTO Answers ( user_id, post_id, question_id, answer ) VALUES ( %s, %s, %s, %s )", [userId, postId, questionCount, answer])
		mysql.connection.commit()
		questionCount = questionCount + 1


	return "Success!\n"

#ASSUMES ORG EXISTS
#curl --request POST -H "Content-Type: application/json" -d '{"org_name":"BobsClub","pos_name":"Third Best Friend","description":"need friend"}' http://127.0.0.1:5000/CreatePosting
@app.route('/CreatePosting', methods=['POST'])
@cross_origin(origin='*')
def post_create_posting():
	data = request.get_json()
	cursor = mysql.connection.cursor()

	cursor.execute("SELECT * FROM Organizations WHERE name = %s", [data["org_name"]])
	results = cursor.fetchall()
	orgId = 0
	for row in results:
		orgId = row[0]
	if orgId == 0:
		return "ORG NOT FOUND!"

	cursor.execute("INSERT INTO Postings ( org_id, name, status, description ) VALUES ( %s, %s, %s, %s )", [orgId, data['pos_name'], "OPEN", data['description']])
	mysql.connection.commit()
	cursor.execute("SELECT * FROM Postings WHERE org_id = %s AND name = %s", [orgId, data['pos_name']])
	results = cursor.fetchall()
	retId = 0	
	for row in results:
		retId = row[0]
	return str(retId) + "\n"

if __name__ == '__main__':
	app.run(debug=True)
