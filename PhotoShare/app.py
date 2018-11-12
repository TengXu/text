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
# from flaskext.mysql import MySQL
# import flask.ext.login as flask_login

# # for image uploading
# # from werkzeug import secure_filename
# import os, base64

# mysql = MySQL()
# app = Flask(__name__)
# app.secret_key = 'super secret string'  # Change this!

# # These will need to be changed according to your creditionals
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'sat2200'
# app.config['MYSQL_DATABASE_DB'] = 'photoshare'
# app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
# mysql.init_app(app)

# # begin code used for login
# login_manager = flask_login.LoginManager()
# login_manager.init_app(app)

# conn = mysql.connect()
# cursor = conn.cursor()
# cursor.execute("SELECT email FROM Users")
# users = cursor.fetchall()


# def getUserList():
    # cursor = conn.cursor()
    # cursor.execute("SELECT email FROM Users")
    # return cursor.fetchall()


# class User(flask_login.UserMixin):
    # pass


# @login_manager.user_loader
# def user_loader(email):
    # users = getUserList()
    # if not (email) or email not in str(users):
        # return
    # user = User()
    # user.id = email
    # return user


# @login_manager.request_loader
# def request_loader(request):
    # users = getUserList()
    # email = request.form.get('email')
    # if not (email) or email not in str(users):
        # return
    # user = User()
    # user.id = email
    # cursor = mysql.connect().cursor()
    # cursor.execute("SELECT password FROM Users WHERE email = '{0}'".format(email))
    # data = cursor.fetchall()
    # pwd = str(data[0][0])
    # user.is_authenticated = request.form['password'] == pwd
    # return user


# '''
# A new page looks like this:
# @app.route('new_page_name')
# def new_page_function():
	# return new_page_html
# '''


# @app.route('/login', methods=['GET', 'POST'])
# def login():
    # if flask.request.method == 'GET':
        # return '''
			   # <form action='login' method='POST'>
				# <input type='text' name='email' id='email' placeholder='email'></input>
				# <input type='password' name='password' id='password' placeholder='password'></input>
				# <input type='submit' name='submit'></input>
			   # </form></br>
		   # <a href='/'>Home</a>
			   # '''
    # # The request method is POST (page is recieving data)
    # email = flask.request.form['email']
    # cursor = conn.cursor()
    # # check if email is registered
    # if cursor.execute("SELECT password FROM Users WHERE email = '{0}'".format(email)):
        # data = cursor.fetchall()
        # pwd = str(data[0][0])
        # if flask.request.form['password'] == pwd:
            # user = User()
            # user.id = email
            # flask_login.login_user(user)  # okay login in user
            # return flask.redirect(flask.url_for('protected'))  # protected is a function defined in this file

    # # information did not match
    # return "<a href='/login'>Try again</a>\
			# </br><a href='/register'>or make an account</a>"


# @app.route('/logout')
# def logout():
    # flask_login.logout_user()
    # return render_template('hello.html', message='Logged out')


# @login_manager.unauthorized_handler
# def unauthorized_handler():
    # return render_template('unauth.html')


# # you can specify specific methods (GET/POST) in function header instead of inside the functions as seen earlier
# @app.route("/register", methods=['GET'])
# def register():
    # return render_template('register.html', supress='True')


# @app.route("/register", methods=['POST'])
# def register_user():
    # try:
        # firstname = request.form.get('firstname')
        # lastname = request.form.get('lastname')
        # birthday = request.form.get('birthday')
        # email = request.form.get('email')
        # password = request.form.get('password')
        # hometown = request.form.get('hometown')
        # gender = request.form.get('gender')
    # except:
        # print(
            # "couldn't find all tokens")  # this prints to shell, end users will not see this (all print statements go to shell)
        # return flask.redirect(flask.url_for('register'))
    # cursor = conn.cursor()
    # test = isEmailUnique(email)
    # if test:
        # print(cursor.execute("INSERT INTO Users (firstname, lastname, birthday, email, password, hometown, gender) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}')".format(firstname, lastname, birthday, email, password, hometown, gender)))
        # conn.commit()
        # # log user in
        # user = User()
        # user.id = email
        # flask_login.login_user(user)
        # uid = getUserIdFromEmail(email)
        # cursor.execute("INSERT INTO Activity (activity, user_id) VALUES ('{0}', '{1}')".format(0, uid))
        # conn.commit()
        # return render_template('hello.html', name=email, message='Account Created!')
    # else:
        # print("couldn't find all tokens")
        # return flask.redirect(flask.url_for('register'))


# def getUsersPhotos(uid):
    # cursor = conn.cursor()
    # cursor.execute("SELECT photopath, photo_id, caption FROM Photo WHERE user_id = '{0}'".format(uid))
    # return cursor.fetchall()  # NOTE list of tuples, [(photopath, pid), ...]


# def getUserIdFromEmail(email):
    # cursor = conn.cursor()
    # cursor.execute("SELECT user_id  FROM Users WHERE email = '{0}'".format(email))
    # return cursor.fetchone()[0]


# def isEmailUnique(email):
    # # use this to check if a email has already been registered
    # cursor = conn.cursor()
    # if cursor.execute("SELECT email  FROM Users WHERE email = '{0}'".format(email)):
        # # this means there are greater than zero entries with that email
        # return False
    # else:
        # return True


# # end login code

# @app.route('/profile')
# @flask_login.login_required
# def protected():
    # return render_template('hello.html', name=flask_login.current_user.id, message="Here's your profile")


# # begin photo uploading code
# # photos uploaded using base64 encoding so they can be directly embeded in HTML 
# ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


# def allowed_file(filename):
    # return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# upload_folder = '/Users/shizhan/CS460/PhotoShare/static/'
# app.config['upload_folder'] = upload_folder
# @app.route('/upload', methods=['GET', 'POST'])
# @flask_login.login_required
# def upload_file():
    # if request.method == 'POST':
        # uid = getUserIdFromEmail(flask_login.current_user.id)
        # imgfile = request.files['photo']
        # filename = imgfile.filename
        # caption = request.form.get('caption')
        # imgfile.save(os.path.join(app.config['upload_folder'], filename))
        # #photo_data = base64.standard_b64encode(imgfile.read())
        # photopath = "static/"+filename
        # cursor = conn.cursor()
        # cursor.execute(
        # "INSERT INTO Photo (photopath, user_id, caption) VALUES ('{0}', '{1}', '{2}' )".format(photopath, uid, caption))
        # conn.commit()
        # cursor.execute("UPDATE Activity SET activity = activity + 1 WHERE user_id = '{0}'".format(uid))
        # conn.commit()
        # return render_template('hello.html', name=flask_login.current_user.id, message='Photo uploaded!',
                               # photos=getUsersPhotos(uid), photopath= photopath)
    # # The method is GET so we return a  HTML form to upload the a photo.
    # else:
        # return render_template('upload.html')


# # end photo uploading code


# # default page
# @app.route("/", methods=['GET'])
# def hello():
    # return render_template('hello.html', message='Welecome to Photoshare')

# #Friends
# @app.route('/searchUsers', methods= ['POST','GET'])
# @flask_login.login_required
# def searchUsers():
    # if request.method == 'POST':
        # cursor = conn.cursor()
        # email = request.form.get('email')
        # cursor.execute("SELECT u.email, u.firstname, u.lastname FROM Users u  WHERE u.email = '{0}'".format(email))
        # return render_template('searchUsers.html', rows=cursor.fetchall())
    # else:
        # return render_template('searchUsers.html')

# @app.route('/addFriends', methods= ['POST','GET'])
# @flask_login.login_required
# def addFriends():
        # if request.method == 'POST':
            # cursor = conn.cursor()
            # uid = getUserIdFromEmail(flask_login.current_user.id)
            # email = request.form.get('email')
            # fid = getUserIdFromEmail(email)
            # cursor.execute("INSERT INTO Friends (user_id, friend_id) VALUES ('{0}','{1}')".format(uid,fid))
            # conn.commit()
            # return render_template('addFriends.html', message = 'Success!')
        # else:
            # return render_template('addFriends.html')

# @app.route('/listFriends', methods = ['GET'])
# @flask_login.login_required
# def listFriends():
    # cursor = conn.cursor()
    # uid = getUserIdFromEmail(flask_login.current_user.id)
    # cursor.execute("SELECT u.firstname, u.lastname, u.email FROM Friends f, Users u WHERE f.user_id = '{0}' and f.friend_id = u.user_id".format(uid))
    # return render_template('listFriends.html',row=cursor.fetchall())

# #Activity
# @app.route('/top10Activity', methods = ['GET'])
# def top10Activity():
    # cursor = conn.cursor()
    # cursor.execute("SELECT u.firstname, u.lastname, u.email FROM Users u, Activity a WHERE u.user_id = a.user_id ORDER BY a.activity DESC LIMIT 10")
    # p = cursor.fetchall()
    # return render_template('top10Activity.html', rows = p)

# #viewPhoto
# @app.route('/viewPhoto', methods = ['GET'])
# def viewPhoto():
    # cursor = conn.cursor()
    # cursor.execute("SELECT p.photopath, p.caption, p.photo_id, u.email, u.firstname, u.lastname FROM Photo p, Users u WHERE p.user_id = u.user_id")
    # return render_template('viewPhoto.html', photos=cursor.fetchall())

# #Album
# @app.route('/addAlbum', methods = ['POST','GET'])
# @flask_login.login_required
# def addAlbum():
    # if request.method == 'POST':
        # cursor = conn.cursor()
        # uid = getUserIdFromEmail(flask_login.current_user.id)
        # name = request.form.get('name')
        # cursor.execute("INSERT INTO Album (name, user_id) VALUES ('{0}','{1}')".format(name,uid))
        # conn.commit()
        # return render_template('addAlbum.html',message = 'Success!')
    # else:
        # return render_template('addAlbum.html')

# @app.route('/listAlbum', methods=['GET'])
# @flask_login.login_required
# def listAlbum():
    # cursor = conn.cursor()
    # uid = getUserIdFromEmail(flask_login.current_user.id)
    # cursor.execute("SELECT a.name, a.album_id FROM Album a, Users u WHERE u.user_id = '{0}' and a.user_id = u.user_id".format(uid))
    # return render_template('listAlbum.html', row = cursor.fetchall())

# @app.route('/deleteAlbum', methods = ['POST','GET'])
# @flask_login.login_required
# def deleteAlbum():
    # if request.method == 'POST':
        # cursor = conn.cursor()
        # aid = request.form.get('album_id')
        # uid = getUserIdFromEmail(flask_login.current_user.id)
        # name = request.form.get('name')
        # cursor.execute("DELETE FROM Album WHERE album_id = '{0}' and name = '{1}' and user_id = '{2}'".format(aid,name,uid))
        # conn.commit()
        # return render_template('deleteAlbum.html', message = 'SUCCESS!')
    # else:
        # return render_template('deleteAlbum.html')

# #Photo
# @app.route('/addPhoto', methods = ['POST','GET'])
# @flask_login.login_required
# def addPhoto():
    # if request.method == 'POST':
        # cursor = conn.cursor()
        # pid = request.form.get('photo_id')
        # aid = request.form.get('album_id')
        # cursor.execute("UPDATE Photo p SET p.album_id = '{0}' WHERE p.photo_id = '{1}'".format(aid,pid))
        # conn.commit()
        # return render_template('addPhoto.html',message = 'Success!')
    # else:
        # return render_template('addPhoto.html')

# @app.route('/listPhoto', methods=['GET'])
# @flask_login.login_required
# def listPhoto():
    # #print "in"
    # cursor = conn.cursor()
    # uid = getUserIdFromEmail(flask_login.current_user.id)
    # #print uid
    # p = getUsersPhotos(uid)
    # #print p
    # #cursor.execute("SELECT p.photopath, p.caption, p.photo_id, a.name FROM Photo p, Album a, Users u WHERE p.user_id = '{0}' and p.album_id = a.album_id and p.user_id = u.user_id".format(uid))
    # #print cursor.fetchall()
    # return render_template('listPhoto.html', photos = p)

# @app.route('/deletePhoto', methods = ['POST','GET'])
# @flask_login.login_required
# def deletePhoto():
    # if request.method == 'POST':
        # cursor = conn.cursor()
        # #uid = flask_login.current_user.id
        # #print(uid)
        # pid = request.form.get('photo_id')
        # cursor.execute("DELETE FROM Photo p WHERE p.photo_id = pid")
        # conn.commit()
        # return render_template('deletePhoto.html', message = 'Success!')
    # else:
        # return render_template('deletePhoto.html')

# #Tag
# @app.route('/addTag', methods = ['POST','GET'])
# @flask_login.login_required
# def addTag():
    # if request.method == 'POST':
        # cursor = conn.cursor()
        # photo_id = request.form.get('photo_id')
        # print (photo_id)
        # tag = request.form.get('tag')
        # q = "INSERT INTO Tag (tag, photo_id) VALUES ('{0}','{1}')".format(tag, photo_id)
        # cursor.execute(q)
        # #cursor.execute("INSERT INTO Album (name, user_id) VALUES ('{0}','{1}')".format(name, uid))
        # conn.commit()
        # print ('done')
        # return render_template('addTag.html', message = 'SUCCESS!')
    # else:
        # return render_template('addTag.html')

# @app.route('/listTag', methods = ['GET'])
# @flask_login.login_required
# def listTag():
    # cursor = conn.cursor()
    # print("here")
    # uid = getUserIdFromEmail(flask_login.current_user.id)
    # cursor.execute("SELECT p.photopath, p.caption, p.photo_id, a.name, a.album_id, t.tag FROM Photo p, Album a, Users u, Tag t WHERE p.user_id='{0}' and p.album_id = a.album_id and p.photo_id=t.photo_id and p.user_id = u.user_id".format(uid))
    # return render_template('listTag.html', photos = cursor.fetchall())

# @app.route('/viewallTag', methods = ['GET'])
# @flask_login.login_required
# def viewallTag():
    # cursor = conn.cursor()
    # cursor.execute("SELECT p.photopath, p.caption, p.photo_id, a.name, a.album_id, u.email, u.firstname, u.lastname, t.tag FROM Photo p, Album a, Users u, Tag t WHERE p.photo_id = t.photo_id and p.album_id = a.album_id and p.user_id = u.user_id")
    # return render_template('viewallTag.html', photos=cursor.fetchall())

# @app.route('/viewpopTag', methods = ['GET'])
# @flask_login.login_required
# def viewpopTag():
    # cursor = conn.cursor()
    # cursor.execute("SELECT t.tag, COUNT(*) FROM Tag t GROUP BY tag ORDER BY COUNT(*) DESC")
    # return render_template('viewpopTag.html', photos=cursor.fetchall())

# @app.route('/searchTag', methods = ['POST','GET'])
# def searchTag():
    # if request.method == 'POST':
        # cursor = conn.cursor()
        # tag = request.form.get('tag')
        # cursor.execute("SELECT p.photopath, p.caption, p.photo_id, a.name, u.firstname, u.lastname, u.email, t.tag, a.album_id FROM Photo p, Album a, Users u, Tag t WHERE t.tag = '{0}' and t.photo_id = p.photo_id and p.album_id = a.album_id and p.user_id = u.user_id".format(tag))
        # return render_template('searchTag.html', photos = cursor.fetchall())
    # else:
        # return render_template('searchTag.html')

# #Comment
# @app.route('/addComment', methods = ['POST','GET'])
# @flask_login.login_required
# def addComment():
    # if request.method == 'POST':
        # cursor = conn.cursor()
        # email = flask_login.current_user.id
        # uid = getUserIdFromEmail(email)
        # pid = request.form.get('photo_id')
        # ctext = request.form.get('text')
        # cursor.execute("UPDATE Activity SET activity = activity + 1")
        # conn.commit()
        # cursor.execute("INSERT INTO Comment (user_id, photo_id, text) VALUES ('{0}','{1}','{2}')".format(uid, pid, ctext))
        # conn.commit()
        # return render_template('addComment.html', message = 'Success!')
    # else:
        # return  render_template('addComment.html')

# @app.route('/viewComment', methods = ['POST','GET'])
# def viewComment():
    # if request.method == 'POST':
        # cursor = conn.cursor()
        # pid = request.form.get('photo_id')
        # cursor.execute("SELECT c.text, u.firstname, u.lastname, u.email FROM Photo p, Comment c, Users u WHERE c.photo_id = '{0}' and c.user_id = u.user_id and c.photo_id = p.photo_id".format(pid))
        # return render_template('viewComment.html', photos = cursor.fetchall())
    # else:
        # return render_template('viewComment.html')

# @app.route('/searchComment', methods = ['POST','GET'])
# def searchComment():
    # if request.method == 'POST':
        # cursor = conn.cursor()
        # comment = request.form.get('comment')
        # cursor.execute("SELECT p.photopath, p.caption, p.photo_id, a.name, u.firstname, u.lastname, u.email, a.album_id FROM Photo p, Album a, Users u, Comment c WHERE c.text = '{0}' and c.photo_id = p.photo_id and p.album_id = a.album_id and p.user_id = u.user_id".format(comment))
        # return render_template('searchComment.html', photos = cursor.fetchall())
    # else:
        # return render_template('searchComment.html')

# #Likes
# @app.route('/addLikes', methods = ['POST','GET'])
# @flask_login.login_required
# def addLikes():
    # if request.method == 'POST':
        # cursor = conn.cursor()
        # email = flask_login.current_user.id
        # uid = getUserIdFromEmail(email)
        # pid = request.form.get('photo_id')
        # cursor.execute("INSERT INTO Likes (user_id, photo_id) VALUES ('{0}','{1}')".format(uid, pid))
        # conn.commit()
        # return render_template('addLikes.html', message = 'Success!')
    # else:
        # return  render_template('addLikes.html')

# @app.route('/viewLikes', methods = ['POST','GET'])
# def viewLikes():
    # if request.method == 'POST':
        # cursor = conn.cursor()
        # pid = request.form.get('photo_id')
        # cursor.execute("SELECT u.firstname, u.lastname, u.email FROM Likes l, Users u WHERE l.photo_id = '{0}' and l.user_id = u.user_id".format(pid))
        # return render_template('viewLikes.html', rows = cursor.fetchall())
    # else:
        # return render_template('viewLikes.html')

# #Recommend
# @app.route('/recommendFriends', methods = ['GET'])
# @flask_login.login_required
# def recommendFriends():
    # cursor = conn.cursor()
    # email = flask_login.current_user.id
    # uid = getUserIdFromEmail(email)
    # q = "SELECT f.user_id FROM Friends f WHERE f.friend_id = (SELECT f1.friend_id FROM Friends f1 WHERE f1.user_id = '{0}') GROUP BY f.user_id HAVING COUNT(f.friend_id)>1".format(uid)
    # cursor.execute(q)
    # friendlist = cursor.fetchall()
    # return render_template('recommendFriend.html', rows = friendlist)


# def popTag():
    # cursor = conn.cursor()
    # uid = getUserIdFromEmail(flask_login.current_user.id)
    # #cursor.execute("SELECT t.tag FROM Tag t, Photo p WHERE t.photo_id = p.photo_id and p.user_id = '{0}' GROUP BY (t.tag) HAVING COUNT (*)>0 ORDER BY COUNT(*) DESC LIMIT 5".format(uid))
    # q = "SELECT t.tag FROM Tag t, Photo p WHERE t.photo_id = p.photo_id and p.user_id = '{0}' Group BY (t.tag) ORDER BY COUNT(p.user_id) DESC LIMIT 5".format(
        # uid)
    # cursor.execute(q)
    # poptag = cursor.fetchall()
    # poptag = [str(item[0]) for item in poptag]
    # return poptag

# @app.route('/recommendPhoto', methods = ['GET'])
# @flask_login.login_required
# def recommendPhoto():
    # cursor = conn.cursor()
    # poptag = popTag()
    # uid = getUserIdFromEmail(flask_login.current_user.id)
    # cursor.execute("SELECT photo_id FROM Photo")
    # photos = cursor.fetchall()
    # pid = [int(item[0]) for item in photos]
    # rate = [0] * len(pid)
    # recommend = []
    # for i in range(len(pid)):
        # for t in poptag:
            # cursor.execute("SELECT COUNT(*) FROM Tag Where photo_id = '{0}' and tag = '{1}'.format(pid[i], t)")
            # count = cursor.fetchone()
            # count = int(count[0])
            # if count > 0:
                # rate[i] = rate[i] + 1
    # photorate = [(pid[j], rate[j]) for j in range(len(pid))]
    # photorate = sorted(photorate, key=lambda x: (-x[1], x[0]))
    # photorate = photorate[:5]
    # for i in range(len(photorate)):
        # cursor.execute("SELECT photopath FROM Photo WHERE photo_id = '{0}'".format(photorate[i][0]))
        # Rate = cursor.fetchall()
        # count = [item[0] for item in Rate]
        # recommend.append(count)
    # return render_template('recommendPhoto.html', photos = recommend)





if __name__ == "__main__":
    # this is invoked when in the shell  you run
    # $ python app.py
    app.run(port=5000, debug=True)
