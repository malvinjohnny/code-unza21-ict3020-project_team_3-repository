# code goes here
from flask import render_template, url_for, flash, redirect,request,send_file, send_from_directory, safe_join, abort
from app import app,db,bcrypt,mail
from app.Forms import FileUploadForm, RegistrationForm, LoginForm,SearchForm
from app.models import User, Post,FileUpload
from app.customModules import DataBaseFunctions as dbFunc
from flask_login import login_user,current_user,logout_user,login_required
from flask_mail import  Message
import werkzeug

# ? the home/landing route
@app.route('/')
@app.route("/home")
def index():
    return render_template("index.html", title="Home")

# ? this is where users sign up
@app.route("/signup", methods=['Get', 'POST'])
def register():
    # redirect the user to the home page if they are already logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    # this is the form for user Registration
    form = RegistrationForm()
    #This is called when  the form is submitted
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Your account has been created", category="success")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)

# ? This is the route for the login page
@app.route("/login", methods=['Get', 'POST'])
def login():
    # a redirect to the home page
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    #login form
    form = LoginForm()
    # this part checks for successful login by checking the data base
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash(f"Log in unsuccessfull, please check details", category="danger")

    return render_template("login.html", title="Login", form=form)

# ? route to logout
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

# ? route to show all documents stored in database
@app.route("/documents",methods=['Get', 'POST'])
def documents():
    form = SearchForm()
    if form.validate_on_submit():
        posts = FileUpload.query.filter(FileUpload.name.contains(form.parameter.data))
        return render_template("AcceptedDocuments.html",title = "Documents",posts=posts, form=form)
    
    posts = FileUpload.query.all()
    return render_template("AcceptedDocuments.html",title = "Documents",posts=posts, form=form)

# todo Make sure to refactor the part where the file is added to the data base cause it looks really messy, out it in a single function
# ? this is the user account page that is used to upload files
@app.route("/account",methods=['GET','POST'])
@login_required
def account():
    form = FileUploadForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=current_user.email).first()
        if form.ignore_spellCheck.data == True:
            upload = FileUpload(
                name=form.name.data,
                file_Path=dbFunc.SaveFile(form.file.data,app.config['UPLOAD_FOLDER']),
                author_email=form.email.data,
                staff_email=user.email)
            db.session.add(upload)
            db.session.commit()
            flash(f"File uploaded Successfully", category="success")
        else:
            hasNoSpellingErrors = dbFunc.openFileForCheck(form.file.data)
            if hasNoSpellingErrors == False:
                flash(f"File Upload Unsuccessful Because of Spelling Errors", category="danger")
                flash(f"Email sent to file owner", category="success")
                
                sendEmailAndAttachment(form.email.data,user,form.file.data)
            else:
                upload = FileUpload(
                    name=form.name.data,
                    file_Path=dbFunc.SaveFile(form.file.data,app.config['UPLOAD_FOLDER']),
                    author_email=form.email.data,
                staff_email=user.email)
                db.session.add(upload)
                db.session.commit()
                flash(f"File uploaded Successfully", category="success")
    image_file = url_for('static',filename=f'profilePics/{current_user.image_url}')
    return render_template("account.html", title="Account", image_post = image_file,form = form)

# ? file download route
@app.route("/download/<file>",methods=['GET'])
def download(file):
    fileData = FileUpload.query.filter_by(name=file).first()
    print(fileData.file_Path)
    try:
        
        return send_file(fileData.file_Path,as_attachment=True)
    except:
        abort(404)

# ? this function send email if spellig mistakes are found
def sendEmailAndAttachment(recipientUser,user,file):
    msg = Message(
        'Submitted file containing spelling errors',
        sender="noreply@thisProject.com",
        recipients=[recipientUser])

    msg.attach(file.filename + ".pdf",'application/pdf',file.read())
    msg.body=f""" A File You submitted to the File Repository Was found to have some Spelling Errors
    and Mistake, Pleas review your document to ensure the information is well written. 
    
    If your file contains no Mistakes please inform {user.username} at {user.email} as they handled your file
    """
    mail.send(msg)

