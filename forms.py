
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from flask_login import current_user
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from cs350_proj.models import Student
from cs350_proj import app, database, cursor

class RegisterationForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    # def validate_username(self, username):
    #     cursor.execute("select * from student where username = %s ",[username])
    #     user = cursor.fetchone()[0]
    #     if user:
    #         raise ValidationError('That username is taken. Please choose a different one.')

    # def validate_email(self, email):
    #     cursor.execute("select * from student where email = %s ",[email])
    #     user = cursor.fetchone()[0]
    #     if user:
    #         raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update') 

    # def validate_username(self, username):
    #     if username.data != current_user.username: 
    #         cursor.execute("UPDATE student SET username = %s where username = %s ",[username.data, current_user.username])
    #         user = cursor.fetchone()[0]
    #         if user:
    #             raise ValidationError('That username is taken. Please choose a different one.')

    # def validate_email(self, email):
    #     if email.data != current_user.email: 
    #         cursor.execute("select * from student where email = %s ",[email])
    #         user = cursor.fetchone()[0]
    #         if user:
    #             raise ValidationError('That email is taken. Please choose a different one.')

class SelectLanguageForm(FlaskForm):
    cursor.execute('select distinct language from class')
    langs = cursor.fetchall()
    choices = []
    for lang in langs: 
        choices.append((lang[0], lang[0]))
    language = SelectField('language', choices=choices)
    level = SelectField('level', choices=[('A1','A1'),
                                          ('A2','A2'),
                                          ('B1','B1'),
                                          ('B2','B2'),
                                          ('C1','C1'),
                                          ('C2','C2')])
    submit = SubmitField('choose')


class DeleteLanguageForm(FlaskForm):
    cursor.execute('select distinct language from class')
    langs = cursor.fetchall()
    choices = []
    for lang in langs: 
        choices.append((lang[0], lang[0]))
    language = SelectField('language', choices=choices)
    level = SelectField('level', choices=[('A1','A1'),
                                          ('A2','A2'),
                                          ('B1','B1'),
                                          ('B2','B2'),
                                          ('C1','C1'),
                                          ('C2','C2')])
    submit = SubmitField('delete')