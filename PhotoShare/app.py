######################################
# author ben lawson <balawson@bu.edu> 
# Edited by: Baichuan Zhou (baichuan@bu.edu) and Craig Einstein <einstein@bu.edu>
######################################
# Some code adapted from 
# CodeHandBook at http://codehandbook.org/python-web-application-development-using-flask-and-mysql/
# and MaxCountryMan at https://github.com/maxcountryman/flask-login/
# and Flask Offical Tutorial at  http://flask.pocoo.org/docs/0.10/patterns/fileuploads/
# see links for further understanding
###################################################

import flask
from flask import Flask, Response, request, render_template, redirect, url_for
from flaskext.mysql import MySQL
import flask_login
import datetime

import os, base64

mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'super secret string'  # Change this!

# These will need to be changed according to your creditionals
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'sat2200'
app.config['MYSQL_DATABASE_DB'] = 'photoshare'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
mysql.init_app(app)

# begin code used for login
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()
cursor.execute("SELECT email FROM Users")
users = cursor.fetchall()


def getUserList():
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM Users")
    return cursor.fetchall()


class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    users = getUserList()
    if not (email) or email not in str(users):
        return
    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    users = getUserList()
    email = request.form.get('email')
    if not (email) or email not in str(users):
        return
    user = User()
    user.id = email
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT password FROM Users WHERE email = '{0}'".format(email))
    data = cursor.fetchall()
    pwd = str(data[0][0])
    user.is_authenticated = request.form['password'] == pwd
    return user


'''
A new page looks like this:
@app.route('new_page_name')
def new_page_function():
	return new_page_html
'''


@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return render_template('login.html')
    # The request method is POST (page is recieving data)
    email = flask.request.form['email']
    cursor = conn.cursor()
    # check if email is registered
    if cursor.execute("SELECT password FROM Users WHERE email = '{0}'".format(email)):
        data = cursor.fetchall()
        pwd = str(data[0][0])
        if flask.request.form['password'] == pwd:
            user = User()
            user.id = email
            flask_login.login_user(user)  # okay login in user
            return flask.redirect(flask.url_for('protected'))  # protected is a function defined in this file

    # information did not match
    return "<a href='/login'>Try again</a>\
			</br><a href='/register'>or make an account</a>"


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return render_template('login.html')


@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('login.html')


# you can specify specific methods (GET/POST) in function header instead of inside the functions as seen earlier
@app.route("/register", methods=['GET'])
def register():
    return render_template('register.html', supress='True')


@app.route("/register", methods=['POST'])
def register_user():
    try:
		username = request.form.get('username') 
		firstname = request.form.get('firstname') 
		lastname = request.form.get('lastname')
		email = request.form.get('email') 
		password = request.form.get('password')
    except:
        print(
            "couldn't find all tokens")  # this prints to shell, end users will not see this (all print statements go to shell)
        return flask.redirect(flask.url_for('register'))
    cursor = conn.cursor()
    test = isEmailUnique(email)
    if test:
        print(cursor.execute("INSERT INTO Users (username, firstname, lastname, email, password) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')".format(username, firstname, lastname, email, password)))
        conn.commit()
        # log user in
        user = User()
        user.id = email
        flask_login.login_user(user)
        uid = getUserIdFromEmail(email)
        cursor.execute("INSERT INTO Activity (activity, user_id) VALUES ('{0}', '{1}')".format(0, uid))
        conn.commit()
        return render_template('hello.html', name=getUserNameFromEmail(email), message='Account Created!')
    else:
        print("couldn't find all tokens")
        return flask.redirect(flask.url_for('register'))


def getUsersPhotos(uid):
    cursor = conn.cursor()
    cursor.execute("SELECT photopath, photo_id, caption FROM Photo WHERE user_id = '{0}'".format(uid))
    return cursor.fetchall()  # NOTE list of tuples, [(photopath, pid), ...]
	
def getUsersTexts(uid):
    cursor = conn.cursor()
    cursor.execute("SELECT caption, content, post_time, text_id FROM Text WHERE user_id = '{0}'".format(uid))
    return cursor.fetchall() 
	
def getUsersLikes(tid):
    cursor = conn.cursor()
    cursor.execute("SELECT u.username FROM Users u, Likes l WHERE l.text_id = '{0}' AND l.user_id = u.user_id".format(tid))
    return cursor.fetchall() 

def getUsersTextsByDate(uid):
    cursor = conn.cursor()
    cursor.execute("SELECT caption, content, post_time, text_id, user_id FROM Text WHERE user_id = '{0}' ORDER BY post_time DESC".format(uid))
    return cursor.fetchall() 

def getUserIdFromEmail(email):
    cursor = conn.cursor()
    cursor.execute("SELECT user_id  FROM Users WHERE email = '{0}'".format(email))
    return cursor.fetchone()[0]
	
def getUserNameFromEmail(email):
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM Users WHERE email = '{0}'".format(email))
    return cursor.fetchone()[0]
	
def getUserNameFromUid(uid):
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM Users WHERE user_id = '{0}'".format(uid))
    return cursor.fetchone()[0]


def isEmailUnique(email):
    # use this to check if a email has already been registered
    cursor = conn.cursor()
    if cursor.execute("SELECT email  FROM Users WHERE email = '{0}'".format(email)):
        # this means there are greater than zero entries with that email
        return False
    else:
        return True


# end login code

@app.route('/profile')
@flask_login.login_required
def protected():
    return render_template('hello.html', name=getUserNameFromEmail(flask_login.current_user.id), message="Here's your profile")


# begin photo uploading code
# photos uploaded using base64 encoding so they can be directly embeded in HTML 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


upload_folder = '/Users/Teng/PhotoShare/static'
app.config['upload_folder'] = upload_folder
@app.route('/upload', methods=['GET', 'POST'])
@flask_login.login_required
def upload_file():
    if request.method == 'POST':
        uid = getUserIdFromEmail(flask_login.current_user.id)
        imgfile = request.files['photo']
        filename = imgfile.filename
        caption = request.form.get('caption')
        imgfile.save(os.path.join(app.config['upload_folder'], filename))
        #photo_data = base64.standard_b64encode(imgfile.read())
        photopath = "static/"+filename
        cursor = conn.cursor()
        cursor.execute(
        "INSERT INTO Photo (photopath, user_id, caption) VALUES ('{0}', '{1}', '{2}' )".format(photopath, uid, caption))
        conn.commit()
        cursor.execute("UPDATE Activity SET activity = activity + 1 WHERE user_id = '{0}'".format(uid))
        conn.commit()
        return render_template('hello.html', name=getUserNameFromEmail(flask_login.current_user.id), message='Photo uploaded!',
                               photos=getUsersPhotos(uid), photopath= photopath)
    # The method is GET so we return a  HTML form to upload the a photo.
    else:
        return render_template('upload.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/upload_text', methods=['GET', 'POST'])
@flask_login.login_required
def upload_text():
    if request.method == 'POST':
		uid = getUserIdFromEmail(flask_login.current_user.id)
		content = request.form.get('content') 
		caption = request.form.get('caption') 
		post_time = datetime.datetime.now()
		cursor = conn.cursor() 
		cursor.execute( "INSERT INTO Text (content, user_id, caption, post_time) VALUES ('{0}', '{1}', '{2}', '{3}' )".format(content, uid, caption, post_time)) 
		conn.commit() 
		cursor.execute("UPDATE Activity SET activity = activity + 1 WHERE user_id = '{0}'".format(uid)) 
		conn.commit() 
		return render_template('hello.html', name=getUserNameFromEmail(flask_login.current_user.id), message='Text uploaded!')
    else:
        return render_template('upload_text.html')


# default page
@app.route("/", methods=['GET'])
def hello():
    return render_template('login.html')

#Friends
@app.route('/searchUsers', methods= ['POST','GET'])
@flask_login.login_required
def searchUsers():
    if request.method == 'POST':
        cursor = conn.cursor()
        email = request.form.get('email')
        cursor.execute("SELECT u.email, u.firstname, u.lastname FROM Users u  WHERE u.email = '{0}'".format(email))
        return render_template('searchUsers.html', rows=cursor.fetchall())
    else:
        return render_template('searchUsers.html')

@app.route('/addFriends', methods= ['POST','GET'])
@flask_login.login_required
def addFriends():
        if request.method == 'POST':
            cursor = conn.cursor()
            uid = getUserIdFromEmail(flask_login.current_user.id)
            email = request.form.get('email')
            fid = getUserIdFromEmail(email)
            cursor.execute("INSERT INTO Friends (user_id, friend_id) VALUES ('{0}','{1}')".format(uid,fid))
            conn.commit()
            return render_template('addFriends.html', message = 'Success!')
        else:
            return render_template('addFriends.html')

@app.route('/listFriends', methods = ['GET'])
@flask_login.login_required
def listFriends():
    cursor = conn.cursor()
    uid = getUserIdFromEmail(flask_login.current_user.id)
    cursor.execute("SELECT u.username, u.user_id FROM Friends f, Users u WHERE f.user_id = '{0}' and f.friend_id = u.user_id".format(uid))
    return render_template('listFriends.html',row=cursor.fetchall())
	
@app.route('/listFriendsText', methods = ['POST','GET'])
@flask_login.login_required	
def listFriendsText():
	if request.method == 'POST': 
		cursor = conn.cursor() 
		uid = request.form.get('user_id') 
		conn.commit() 
		t = getUsersTextsByDate(uid) 
		return render_template('listFriendsText.html', name=getUserNameFromUid(uid), texts=t) 
	else: 
		return render_template('listFriendsText.html')
	

#Activity
@app.route('/top10Activity', methods = ['GET'])
def top10Activity():
    cursor = conn.cursor()
    cursor.execute("SELECT u.firstname, u.lastname, u.email FROM Users u, Activity a WHERE u.user_id = a.user_id ORDER BY a.activity DESC LIMIT 10")
    p = cursor.fetchall()
    return render_template('top10Activity.html', rows = p)

#viewPhoto
@app.route('/viewPhoto', methods = ['GET'])
def viewPhoto():
    cursor = conn.cursor()
    cursor.execute("SELECT p.photopath, p.caption, p.photo_id, u.email, u.firstname, u.lastname FROM Photo p, Users u WHERE p.user_id = u.user_id")
    return render_template('viewPhoto.html', photos=cursor.fetchall())

@app.route('/listText', methods=['GET'])
@flask_login.login_required
def listText():
    cursor = conn.cursor()
    uid = getUserIdFromEmail(flask_login.current_user.id)
    t = getUsersTextsByDate(uid)
    # cursor.execute("SELECT t.caption, t.content, t.post_time, t.text_id FROM Text t, Users u WHERE t.user_id = '{0}' and t.user_id = u.user_id".format(uid))
    return render_template('listText.html', texts = t)
	
@app.route('/listPhoto', methods=['GET'])
@flask_login.login_required
def listPhoto():
    #print "in"
    cursor = conn.cursor()
    uid = getUserIdFromEmail(flask_login.current_user.id)
    #print uid
    p = getUsersPhotos(uid)
    #print p
    #cursor.execute("SELECT p.photopath, p.caption, p.photo_id, a.name FROM Photo p, Album a, Users u WHERE p.user_id = '{0}' and p.album_id = a.album_id and p.user_id = u.user_id".format(uid))
    #print cursor.fetchall()
    return render_template('listPhoto.html', photos = p)

@app.route('/deletePhoto', methods = ['POST','GET'])
@flask_login.login_required
def deletePhoto():
    if request.method == 'POST':
        cursor = conn.cursor()
        #uid = flask_login.current_user.id
        #print(uid)
        pid = request.form.get('photo_id')
        cursor.execute("DELETE FROM Photo p WHERE p.photo_id = pid")
        conn.commit()
        return render_template('deletePhoto.html', message = 'Success!')
    else:
        return render_template('deletePhoto.html')
		
@app.route('/deleteText', methods = ['POST','GET'])
@flask_login.login_required
def deleteText():
	if request.method == 'POST': 
		cursor = conn.cursor() 
		tid = request.form.get('text_id')
		cursor.execute("DELETE FROM Text WHERE text_id = '{0}'".format(tid)) 
		conn.commit() 
		uid = getUserIdFromEmail(flask_login.current_user.id) 
		t = getUsersTexts(uid) 
		return render_template('listText.html', texts = t) 
	else: 
		return render_template('listText.html')

@app.route('/viewLikes', methods = ['POST','GET'])
@flask_login.login_required
def viewLikes():
	if request.method == 'POST': 
		cursor = conn.cursor() 
		tid = request.form.get('text_id')
		names = getUsersLikes(tid) 
		return render_template('listText.html', texts = t, likes = names) 
	else: 
		return render_template('listText.html')


#Comment
@app.route('/addComment', methods = ['POST','GET'])
@flask_login.login_required
def addComment():
    if request.method == 'POST':
        cursor = conn.cursor()
        email = flask_login.current_user.id
        uid = getUserIdFromEmail(email)
        pid = request.form.get('photo_id')
        ctext = request.form.get('text')
        cursor.execute("UPDATE Activity SET activity = activity + 1")
        conn.commit()
        cursor.execute("INSERT INTO Comment (user_id, photo_id, text) VALUES ('{0}','{1}','{2}')".format(uid, pid, ctext))
        conn.commit()
        return render_template('addComment.html', message = 'Success!')
    else:
        return  render_template('addComment.html')

@app.route('/viewComment', methods = ['POST','GET'])
def viewComment():
    if request.method == 'POST':
        cursor = conn.cursor()
        pid = request.form.get('photo_id')
        cursor.execute("SELECT c.text, u.firstname, u.lastname, u.email FROM Photo p, Comment c, Users u WHERE c.photo_id = '{0}' and c.user_id = u.user_id and c.photo_id = p.photo_id".format(pid))
        return render_template('viewComment.html', photos = cursor.fetchall())
    else:
        return render_template('viewComment.html')

@app.route('/searchComment', methods = ['POST','GET'])
def searchComment():
    if request.method == 'POST':
        cursor = conn.cursor()
        comment = request.form.get('comment')
        cursor.execute("SELECT p.photopath, p.caption, p.photo_id, a.name, u.firstname, u.lastname, u.email, a.album_id FROM Photo p, Album a, Users u, Comment c WHERE c.text = '{0}' and c.photo_id = p.photo_id and p.album_id = a.album_id and p.user_id = u.user_id".format(comment))
        return render_template('searchComment.html', photos = cursor.fetchall())
    else:
        return render_template('searchComment.html')

#Likes
@app.route('/addLikes', methods = ['POST','GET'])
@flask_login.login_required
def addLikes():
	if request.method == 'POST': 
		cursor = conn.cursor() 
		email = flask_login.current_user.id 
		uid = getUserIdFromEmail(email) 
		fid = request.form.get('friend_id')
		tid = request.form.get('text_id') 
		t = getUsersTextsByDate(fid) 
		cursor.execute("INSERT INTO Likes (user_id, text_id) VALUES ('{0}','{1}')".format(uid, tid)) 
		conn.commit() 
		return render_template('listFriendsText.html', name=getUserNameFromUid(fid), texts=t) 
	else: 
		return render_template('listFriendsText.html')


if __name__ == "__main__":
    # this is invoked when in the shell  you run
    # $ python app.py
    app.run(port=5000, debug=True)
