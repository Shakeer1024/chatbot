import flask
from flask import Flask,session,request,render_template,redirect,url_for,flash
from flask_mysqldb import MySQL

app =Flask(__name__)

app.config['MYSQL_HOST'] = 'us-cdbr-east-06.cleardb.net' #Please use your host name
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'b81ff3091705f9' #Please use your user name
app.config['MYSQL_PASSWORD'] = 'd3f20e8c' #Please use your password
app.config['MYSQL_DB'] = 'heroku_8178ef1d9ae0bf2' #Please use your database name that is created.
app.config['MYSQL_CURSORCLASS']='DictCursor'
app.config['SECRET_KEY'] = "b'\x8e\x88}\xd9hC\\6z:,$'" #You can set your own secret key


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
		cur = mysql.connection.cursor()
		cur.execute("SELECT UserName FROM users WHERE UserName='"+ UserName +"'")
		userdata=cur.fetchone()

		if userdata is None:
			if Password == confirm:
				cur = mysql.connection.cursor()
				cur.execute("INSERT INTO users(Name,UserName,Password) VALUES(%s,%s,%s)",(Name,UserName,Password))
				mysql.connection.commit()

				session['name']=Name

				flash("Registered Successfully and you can login now",'success')
				return redirect(url_for('index'))
			else:
				flash("Password does not match",'error')
				return render_template('register.html')
		else:
			flash('username already exist! please user different user name','error')
			return render_template('register.html')

	return render_template('register.html')


@app.route('/login',methods=['GET','POST'])
def login():
	if request.method=='POST':
		session.pop('user',None)
		UserName=request.form.get("username")
		Password=request.form.get("password")

		cur = mysql.connection.cursor()
		cur.execute("SELECT UserName FROM users WHERE UserName='"+ UserName +"'")
		userdata=cur.fetchone()
		cur.execute("SELECT Password FROM users WHERE UserName='"+ UserName +"'")
		pwddata=cur.fetchone()
		session['user']=UserName

		if userdata is None:
			flash("No such user found, Please register",'error')
			return redirect(url_for('index'))
		else:
			if Password==pwddata['Password']:
				flash("Loggedin Successfully", 'success')
				return redirect(url_for('login'))
			else:
				flash("Incorrect username or password",'error')
				return redirect(url_for('index'))

	return render_template('loginhome.html')


@app.route('/chatbot')
def chatbot():
	return render_template('chatbot.html')


@app.route('/logout')
def logout():
	session.pop('user',None)
	flash("Your are now logged out",'success')
	return redirect(url_for('index'))


if __name__ == '__main__':
	app.run(debug=True)

