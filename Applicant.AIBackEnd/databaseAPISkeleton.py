from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin

#Flask and MySQL setup
application = app = Flask(__name__)
api = Api(app)
CORS(app)

mysql = MySQL()

#MySQL setup
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'sdocs123'
app.config['MYSQL_DB'] = 'ApplicantAIDB'
app.config['MYSQL_HOST'] = 'aa5mho3pd0cv71.czzaljfmuz2x.us-east-2.rds.amazonaws.com'
app.config['MYSQL_PORT'] = 3306
mysql.init_app(app)

@app.route('/saveOrganizationInfo', methods=['POST'])
@cross_origin(origin='*')
def save_hash():
	data = request.form
	return 'Stored! (jk, just for test purposes)\n'

@app.route('/getOrganizationInfo', methods=['POST'])
@cross_origin(origin='*')
def get_hash():
	data = request.form
	#cursor = mysql.connection.cursor()
	return None

@app.route('/getOrganizationInfo', methods=['GET'])
@cross_origin(origin='*')
def true_get_hash():
	return None

if __name__ == '__main__':
	app.run(debug=True)
