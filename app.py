from flask import Flask, request, render_template, url_for
from models import select_college_holder
import os
from search import search
from pymongo import MongoClient

client = MongoClient('mongodb://heroku_srq7rv94:3o6c97o1kth5ctf2g10mqpii11@ds033875.mongolab.com:33875/heroku_srq7rv94')
db = client.get_default_database()


app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def system_error(e):
	return render_template('500.html'), 500

@app.route("/", methods=["GET","POST"])
def index():
	colleges = db.colleges.find()
	if request.method == 'POST':
		colleges = db.colleges.find()
		search_input = request.form['search']
		college_found = search(search_input, colleges)

		if college_found == '<p class="title">This college does not yet exist in the database or there is a typo in the query</p>':
			return college_found
		else:
			return render_template("college.html", search_input=search_input, colleges=colleges, college_found=college_found)

	return render_template("index.html", colleges=colleges)



#@app.route("/signup", methods=["GET","POST"])
#def signup():
#	return render_template("signup.html")

"""@app.route("/signedup", methods=["GET","POST"])
def signedup():
	email = request.form['email']
	username = request.form['username']
	password = request.form['password']
	phone = request.form.get('phone')

	if not session.get("logged_in"):
		insert_account_holder(name,acceptance_rate,location,sat_score,act_score)
	return render_template("homepage.html",username=username) 

@app.route("/login")
def login():
	return render_template("login.html")

@app.route("/directory/<username>")
def directory(username):
	contacts = select_by_username_contact(username)
	return render_template("directory.html",username=username,contacts=contacts)"""

if __name__ == '__main__':
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port, debug=False)