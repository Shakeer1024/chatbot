import flask
from flask import Flask,session,request,render_template,redirect,url_for,flash
from flask_mysqldb import MySQL
#from sqlalchemy import create_engine
#from sqlalchemy.orm import scoped_session,sessionmaker

#from flaskext.mysql import MySQL
#import yaml

app =Flask(__name__)

# Configure db
#db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'loginapp'

mysql = MySQL(app)



@app.route('/')
def index():
	return render_template('login.html')

@app.route('/register',methods=['GET','POST'])
def register():
	if request.method == "POST":
		Name=request.form.get("name")
		UserName=request.form.get("username")
		Password=request.form.get("password")
		confirm=request.form.get("confirm password")

		if Password == confirm:
			cur = mysql.connection.cursor()
			cur.execute("INSERT INTO users(Name,UserName,Password) VALUES(%s,%s,%s)",
			                                  (Name,UserName,Password))
			mysql.connection.commit()
			flash("Registered Successfully and you can login now",'success')
			return redirect(url_for('index'))
		else:
			flash("Password is incorrect",'error')
			return render_template('register.html')

	return render_template('register.html')

@app.route('/login',methods=['GET','POST'])
def login():
	if request.method=='POST':
		UserName=request.form.get("username")
		Password=request.form.get("password")
		cur = mysql.connection.cursor()
		cur.execute("SELECT UserName FROM users WHERE UserName='"+ UserName +"'")
		userdata=cur.fetchone()
		cur.execute("SELECT Password FROM users WHERE UserName='"+ UserName +"'")
		pwddata=cur.fetchone()

		if userdata is None:
			flash("No such user found, Please register",'error')
			return redirect(url_for('index'))
		else:
			for pwd in pwddata:
				if Password==pwd:
					flash("Loggedin Successfully", 'success')
					return redirect(url_for('login'))
				else:
					flash("Incorrect username or password",'error')
					return redirect(url_for('index'))

	return render_template('loginhome.html')
if __name__ == '__main__':
	app.secret_key="1234567projectwebcoding"
	app.run(debug=True)

