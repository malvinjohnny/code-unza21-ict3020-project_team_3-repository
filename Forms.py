from flask_wtf import FlaskForm
from flask_wtf.file import  FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo,ValidationError
from app.models import  User,FileUpload
# ? this script stores all the need

#the registration form used buy the registration page
class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[
                                     DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")
    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('User name is already taken')
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('email is already taken')

# the login form
class LoginForm(FlaskForm):

    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Log In")
# the file uploading form
class FileUploadForm(FlaskForm):
    name = StringField("File Name", validators=[DataRequired(),Length(min=3,max=20)])
    email = StringField("File Authors Email", validators=[DataRequired(), Email()])
    file = FileField('Upload File', validators=[FileAllowed(['pdf'])])
    ignore_spellCheck = BooleanField("Ignore Spell Check")
    submit = SubmitField("Upload")
    def validate_name(self,name):
        filename = FileUpload.query.filter_by(name=name.data).first()
        if filename:
            raise ValidationError('File by That name already exists')
# the searching form
class SearchForm(FlaskForm):
    parameter = StringField("Search",validators=[DataRequired()])
    submit = SubmitField("search")
