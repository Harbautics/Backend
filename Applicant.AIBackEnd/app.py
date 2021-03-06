from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
from random import random

import os
import subprocess

#Flask and MySQL setup
application = app = Flask(__name__)
api = Api(app)
CORS(app)

#MySQL setup
'''
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'sdocs'
app.config['MYSQL_DB'] = 'AAIDB'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'sdocs123'
app.config['MYSQL_DB'] = 'AAIDB'
app.config['MYSQL_HOST'] = 'aa5mho3pd0cv71.czzaljfmuz2x.us-east-2.rds.amazonaws.com'
app.config['MYSQL_PORT'] = 3306
'''

mysql = MySQL()
# testing locally
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'sdocs123'
app.config['MYSQL_DB'] = 'AAIDB'
app.config['MYSQL_HOST'] = 'aa5mho3pd0cv71.czzaljfmuz2x.us-east-2.rds.amazonaws.com'
app.config['MYSQL_PORT'] = 3306
mysql.init_app(app)


@app.route('/test/removal', methods=['POST'])
@cross_origin(origin='*')
def drop_all_rows():
	cursor = mysql.connection.cursor()
	cursor.execute("DELETE FROM Answers")
	cursor.execute("DELETE FROM Questions")
	cursor.execute("DELETE FROM Applicants")
	cursor.execute("DELETE FROM Postings")
	cursor.execute("DELETE FROM Members")
	cursor.execute("DELETE FROM Organizations")
	cursor.execute("DELETE FROM Users")
	mysql.connection.commit()

	retIdData = {}
	retIdData["message"] = "SUCCESS!"
	return jsonify(retIdData), 400

#curl --request POST -H "Content-Type: application/json" -d '{"org_name":"BobsClub","description":"This is Bobs club", "email":"bob@bob.com"}' http://127.0.0.1:5000/CreateOrg
@app.route('/CreateOrg', methods=['POST'])
@cross_origin(origin='*')
def post_create_org():
	data = request.get_json()
	cursor = mysql.connection.cursor()

	cursor.execute("SELECT * FROM Organizations WHERE name = %s", [data["org_name"]])
	if cursor.rowcount > 0:
		retIdData = {}
		retIdData["message"] = "ORG ALREADY EXISTS"
		return jsonify(retIdData), 400

	cursor.execute("INSERT INTO Organizations ( name, description, email ) VALUES ( %s, %s, %s )", [data['org_name'], data['description'], data['email']])
	cursor.execute("SELECT * FROM Organizations WHERE name = %s", [data["org_name"]])
	results = cursor.fetchall()
	retId = 0
	for row in results:
		retId = row[0]

	cursor.execute("SELECT user_id FROM Users WHERE email = %s", [data['email']])
	results = cursor.fetchall()
	if cursor.rowcount == 0:
		retIdData = {}
		retIdData["message"] = "email dne in records"
		return jsonify(retIdData), 400

	cursor.execute("INSERT INTO Members (user_id, org_id) VALUES ( %s, %s )", [results[0], retId])
	mysql.connection.commit()

	retIdData = {}
	retIdData["OrganizationId"] = retId
	return jsonify(retIdData), 200


#curl --request POST -H "Content-Type: application/json" -d '{"name":"bob bob","email":"bob@bob.com","password":"bob!"}' http://127.0.0.1:5000/CreateUser
@app.route('/CreateUser', methods=['POST'])
@cross_origin(origin='*')
def post_create_user():
	data = request.get_json()
	cursor = mysql.connection.cursor()
	
	cursor.execute("SELECT * FROM Users WHERE email = %s", [data["email"]])
	if cursor.rowcount > 0:
		retIdData = {}
		retIdData["message"] = "EMAIL ALREADY EXISTS"
		return jsonify(retIdData), 400

	cursor.execute("INSERT INTO Users ( name, email, password ) VALUES ( %s, %s, %s )", [data['name'], data['email'], data['password']])
	mysql.connection.commit()
	cursor.execute("SELECT * FROM Users WHERE email = %s", [data["email"]])
	results = cursor.fetchall()
	retId = 0	
	for row in results:
		retId = row[0]
	retIdData = {}
	retIdData["UserId"] = retId
	return jsonify(retIdData), 200

#curl --request POST -H "Content-Type: application/json" -d '{"org_name":"BobsClub","email":"bob@bob.dcom","pos_name":"Best Friend","answers":["need a friend", "im 6 feet tall", "seems like we would be a good fit", "123"],"answers_ML":[[7,2],[-1,-1],[8,5],[-2, 123]]}' http://127.0.0.1:5000/CreateSubmission

# Answers_ML explanation:
# The answers_ML value is a list of lists (more like list of tuples). The first number in each inner list represents the size of the list of choices in a dropdown field.
# The second number represents the index of the choice that was chosen. If the field is a text field, set both numbers to -1. If the field is an integer field, set the 
# first number to -2 and the second number to the integer value.
@app.route('/CreateSubmission', methods=['POST'])
@cross_origin(origin='*')
def post_create_submission():
	data = request.get_json()
	cursor = mysql.connection.cursor()

	if not os.path.isdir("mldata/"):
		os.mkdir("mldata/")
	
	

	#get User id:
	cursor.execute("SELECT * FROM Users WHERE email = %s", [data["email"]])
	results = cursor.fetchall()
	userId = -1
	for row in results:
		userId = row[0]
	
	if userId == -1:
		retIdData = {}
		retIdData["message"] = "USER NOT FOUND"
		return jsonify(retIdData), 400
	
	#get org id
	cursor.execute("SELECT * FROM Organizations WHERE name = %s", [data["org_name"]])
	results = cursor.fetchall()
	orgId = -1
	for row in results:
		orgId = row[0]

	if orgId == -1:
		retIdData = {}
		retIdData["message"] = "ORG NOT FOUND"
		return jsonify(retIdData), 400

	#get post id
	cursor.execute("SELECT * FROM Postings WHERE org_id = %s AND name = %s", [orgId, data['pos_name']])
	results = cursor.fetchall()
	postId = -1	
	for row in results:
		postId = row[0]

	if postId == -1:
		retIdData = {}
		retIdData["message"] = "POST NOT FOUND"
		return jsonify(retIdData), 400

	cursor.execute("SELECT * FROM Applicants WHERE user_id = %s AND post_id = %s", [userId, postId])
	if cursor.rowcount > 0:
		retIdData = {}
		retIdData["message"] = "APPLICANT ALREADY EXISTS"
		return jsonify(retIdData), 400

	cursor.execute("INSERT INTO Applicants ( user_id, post_id, status) VALUES ( %s, %s, 'PENDING' )", [userId, postId])
	
	questionCount = 0
	for answer in data['answers']:
		cursor.execute("SELECT * FROM Questions WHERE post_id = %s AND question_id = %s", [postId, questionCount])
		if cursor.rowcount == 0:
			retIdData = {}
			s = "QUESTION DOES NOT EXIST FOR ANSWER # " + str(questionCount+1)
			retIdData["message"] = s
			return jsonify(retIdData), 400
		cursor.execute("INSERT INTO Answers ( user_id, post_id, question_id, answer ) VALUES ( %s, %s, %s, %s )", [userId, postId, questionCount, answer])
		questionCount = questionCount + 1
	
	count = 0
	string_to_add = ""
	with open('mldata/'+str(userId)+'.txt', 'w') as f:
		#f.write(str(data_len))
		for answer in data['answers_ML']:
			code = answer[0]
			val = answer[1]
			options = []
			if code != -1:
				count += 1
				if code > 0:
					options = [0] * code
					options[val] = 1
				elif code == -2:
					options = [val]
				for choice in options:
					string_to_add += ','+str(choice)
		
		f.write('1,'+str(count)+string_to_add)
	
	mysql.connection.commit()
	
	retData = {}
	retData["message"] = "Success!"
	return jsonify(retData), 200

#ASSUMES ORG EXISTS
#curl --request POST -H "Content-Type: application/json" -d '{"org_name":"BobsClub","pos_name":"Best Friend","description":"need friend","questions":["Why are you a good fit for this friendship?", "Tell me anything", "Anything else?"]}' http://127.0.0.1:5000/CreatePosting
@app.route('/CreatePosting', methods=['POST'])
@cross_origin(origin='*')
def post_create_posting():
	data = request.get_json()
	cursor = mysql.connection.cursor()

	cursor.execute("SELECT * FROM Organizations WHERE name = %s", [data["org_name"]])
	results = cursor.fetchall()
	orgId = -1
	for row in results:
		orgId = row[0]
	if orgId == -1:
		retIdData = {}
		retIdData["message"] = "ORG NOT FOUND"
		return jsonify(retIdData), 400
	
	cursor.execute("SELECT * FROM Postings WHERE org_id = %s AND name = %s", [orgId, data['pos_name']])
	if cursor.rowcount > 0:
		retIdData = {}
		retIdData["message"] = "POSTING ALREADY EXISTS"
		return jsonify(retIdData), 400
	
	cursor.execute("INSERT INTO Postings ( org_id, name, status, description ) VALUES ( %s, %s, %s, %s )", [orgId, data['pos_name'], "OPEN", data['description']])
	cursor.execute("SELECT * FROM Postings WHERE org_id = %s AND name = %s", [orgId, data['pos_name']])
	results = cursor.fetchall()
	postId = 0	
	for row in results:
		postId = row[0]

	questionCount = 0
	for question in data['questions']:
		cursor.execute("INSERT INTO Questions ( question_id, post_id, question ) VALUES ( %s, %s, %s )", [ questionCount, postId, question ])
		questionCount = questionCount + 1	
		
	mysql.connection.commit()

	retIdData = {}
	retIdData["PostingId"] = postId
	return jsonify(retIdData), 200

@app.route('/getAllSubmissions', methods=['POST'])
@cross_origin(origin='*')
def get_submissions():
	

	data = request.get_json()
	cursor = mysql.connection.cursor()

	cursor.execute("SELECT user_id from Users where email = %s", [data['email']])
	if cursor.rowcount == 0:
		retIdData = {}
		retIdData["message"] = "INVALID EMAIL"
		return jsonify(retIdData), 400

	user_id = cursor.fetchone()

	return_data = {}
	return_data['user_id'] = user_id
	return_data['submissions'] = []
	cursor.execute("SELECT a.post_id, a.status, p.org_id, p.name FROM Applicants a, Postings p WHERE a.user_id = %s \
					AND p.post_id = a.post_id", [user_id])
	results = cursor.fetchall()

	i = 0

	# for every submission to a posting this user has made,
	# provide the list of all questions/responses 
	for row in results:
		return_data['submissions'].append({})
		return_data['submissions'][i]['post_id'] = row[0]
		return_data['submissions'][i]['status'] = row[1]
		return_data['submissions'][i]['org_id'] = row[2]
		return_data['submissions'][i]['post_name'] = row[3]

		cursor.execute("SELECT q.question_id, q.question, a.answer FROM Questions q, Answers a \
							WHERE q.question_id = a.question_id \
							AND a.post_id = q.post_id \
							AND a.post_id = %s \
							AND a.user_id = %s", [row[0], user_id])
		responses = cursor.fetchall()

		return_data['submissions'][i]['responses'] = []

		for res in responses:
			qa = {}
			qa['question_id'] = res[0]
			qa['question'] = res[1]
			qa['answer'] = res[2]
			return_data['submissions'][i]['responses'].append(qa)
		i += 1


	return jsonify(return_data) 

@app.route('/updateApplicant', methods=['POST'])
@cross_origin(origin='*')
def update_applicant():
	data = request.get_json()

	cursor = mysql.connection.cursor()

	if (data['status'] not in ['INTERVIEW', 'ACCEPT', 'REJECT', 'PENDING']):
		retIdData = {}
		retIdData["message"] = "INVALID STATUS UPDATE"
		return jsonify(retIdData), 400

	cursor.execute("SELECT user_id FROM Users where email = %s", [data['email']])
	results = cursor.fetchall()

	if (cursor.rowcount == 0):
		retIdData = {}
		retIdData["message"] = "USER NOT FOUND"
		return jsonify(retIdData), 400
	user_id = results[0]
	#get user_id based off of the email and posting
	cursor.execute("UPDATE Applicants SET status = %s \
					WHERE user_id = %s AND post_id = %s", [data['status'], user_id, data['post_id']])
	results = cursor.fetchall()

	# if the applicant has been accepted we add them to the members list
	if (data['status'] == 'ACCEPT'):
		cursor.execute("SELECT org_id FROM Postings WHERE post_id = %s ", [data['post_id']])
		if (cursor.rowcount != 1):
			retIdData = {}
			retIdData["message"] = "ERROR: INVALID ORG"
			return jsonify(retIdData), 400
		orgs = cursor.fetchone()
		cursor.execute("SELECT * FROM Members where user_id = %s AND org_id = %s", [user_id, orgs])
		if (cursor.rowcount == 0):
			cursor.execute("INSERT INTO Members ( user_id, org_id) VALUES (%s, %s)", [user_id, orgs])



	mysql.connection.commit()

	retIdData = {}
	retIdData["message"] = "APPLICATION UPDATED!"
	return jsonify(retIdData), 400

@app.route('/getOrganizationInfo', methods=['GET'])
@cross_origin(origin='*')
def get_all_org_info():
	cursor = mysql.connection.cursor()
	data = { 
		"user" : {
			"name" : "bob",
			"id:" : 10,
			"password" : "hhhh",
			"email" : "i@bob.com"
		},
		"organizations": [

		]
	}
	
	cursor.execute("SELECT * FROM Organizations", [])
	results = cursor.fetchall()
	for row in results:
		print(row)
		orgData = {}
		orgData["name"] = row[1]
		orgData["id"] = row[0]
		orgData["members"] = []
		cursor.execute("SELECT m.user_id, u.name, u.email FROM Members m, Users u WHERE m.org_id = %s AND m.user_id = u.user_id", [row[0]])
		memberResults = cursor.fetchall()
		for mr in memberResults:
			memberData = {}
			memberData["id"] = mr[0]
			memberData["name"] = mr[1]
			memberData["email"] = mr[2]
			orgData["members"].append(memberData)
		orgData["postings"] = []
		cursor.execute("SELECT * FROM Postings WHERE org_id = %s", [row[0]])
		innerResults = cursor.fetchall()
		for innerRow in innerResults:
			postData = {}
			postData["id"] = innerRow[0]
			postData["name"] = innerRow[2]
			postData["status"] = innerRow[3]
			postData["description"] = innerRow[4]
			postData["questions"] = []
			cursor.execute("SELECT * FROM Questions WHERE post_id = %s", [innerRow[0]])
			questionResults = cursor.fetchall()
			for questionRow in questionResults:
				postData["questions"].append(questionRow[2])
			orgData["postings"].append(postData)
		data["organizations"].append(orgData)
	
	return jsonify(data)


@app.route('/getOrganizationInfoFromEmail', methods=['POST'])
@cross_origin(origin='*')
def get_all_org_info_by_email():
	cursor = mysql.connection.cursor()
	inData = request.get_json()
	data = {
		"organizations": [

		]
	}
	
	cursor.execute("SELECT * FROM Organizations WHERE email = %s", [inData['email']])
	results = cursor.fetchall()
	for row in results:
		print(row)
		orgData = {}
		orgData["name"] = row[1]
		orgData["id"] = row[0]
		orgData["members"] = []
		cursor.execute("SELECT m.user_id, u.name, u.email FROM Members m, Users u WHERE m.org_id = %s AND m.user_id = u.user_id", [row[0]])
		memberResults = cursor.fetchall()
		for mr in memberResults:
			memberData = {}
			memberData["id"] = mr[0]
			memberData["name"] = mr[1]
			memberData["email"] = mr[2]
			orgData["members"].append(memberData)
		orgData["postings"] = []
		cursor.execute("SELECT * FROM Postings WHERE org_id = %s", [row[0]])
		innerResults = cursor.fetchall()
		for innerRow in innerResults:
			postData = {}
			postData["id"] = innerRow[0]
			postData["name"] = innerRow[2]
			postData["status"] = innerRow[3]
			postData["description"] = innerRow[4]
			postData["questions"] = []
			cursor.execute("SELECT * FROM Questions WHERE post_id = %s", [innerRow[0]])
			questionResults = cursor.fetchall()
			for questionRow in questionResults:
				postData["questions"].append(questionRow[2])
			orgData["postings"].append(postData)
		data["organizations"].append(orgData)
	
	return jsonify(data)




@app.route('/getApplicantsFromPosting', methods=['POST'])
@cross_origin(origin='*')
def get_applicant_from_posting():
	data = request.get_json()
	cursor = mysql.connection.cursor()
	
	#get org id
	cursor.execute("SELECT * FROM Organizations WHERE name = %s", [data["org_name"]])
	results = cursor.fetchall()
	orgId = -1
	for row in results:
		orgId = row[0]

	if orgId == -1:
		retIdData = {}
		retIdData["message"] = "ORG NOT FOUND"
		return jsonify(retIdData), 400

	#get post id
	cursor.execute("SELECT * FROM Postings WHERE org_id = %s AND name = %s", [orgId, data['pos_name']])
	results = cursor.fetchall()
	postId = -1	
	for row in results:
		postId = row[0]

	if postId == -1:
		retIdData = {}
		retIdData["message"] = "POST NOT FOUND"
		return jsonify(retIdData), 400
	
	
	cursor.execute("SELECT * FROM Applicants WHERE post_id = %s", [postId])
	results = cursor.fetchall()
	retData = { "applicants": [] }
	for applicant in results:
		userId = applicant[0]
		status = applicant[2]
		applicantData = { "status":status }
		
		cursor.execute("SELECT * FROM Users WHERE user_id = %s", [userId])
		userResults = cursor.fetchall()
		userData = {}
		for ur in userResults:
			userData["id"] = userId
			userData["name"] = ur[1]
			userData["email"] = ur[2]
		applicantData["userInfo"] = userData
		
		args = ("./run", "out", 'mldata/'+str(userId)+".txt")
		
		popen = subprocess.Popen(args, stdout=subprocess.PIPE)
		popen.wait()
		percentage = popen.stdout.read()
		
		applicantData["perc_match"] = float(percentage) * 100
		
		#applicantData["perc_match"] = round(random()*10000)/100.0
		
		cursor.execute("SELECT * FROM Answers WHERE user_id = %s AND post_id = %s", [userId, postId])
		answerResults = cursor.fetchall()
		applicantData["questions"] = []
		for ar in answerResults:
			questionId = ar[2]
			answer = ar[3]
			question = ""
			cursor.execute("SELECT * FROM Questions WHERE question_id = %s", [questionId])
			questionResults = cursor.fetchall()
			for qr in questionResults:
				question = qr[2]
			applicantData["questions"].append({"question":question, "answer":answer})
		retData["applicants"].append(applicantData)
	return jsonify(retData)
		

if __name__ == '__main__':
	app.run(debug=True)
