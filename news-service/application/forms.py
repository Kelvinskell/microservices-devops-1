from application import app
from application import mysql
from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from venv import create
import mysql.connector
import os
# Set Database Variables
USER = os.getenv('MYSQL_USER')
HOST = os.getenv('MYSQL_HOST')
DB = os.getenv('MYSQL_DB')
PASSWORD = os.getenv('DATABASE_PASSWORD')
SHOW_DB = "SHOW DATABASES"
SHOW_TB = "SHOW TABLES"


class RegisterForm(FlaskForm):
    def validate_username(self, value):
        # cursor = mysql.connection.cursor()
         with mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DB
        ) as connection:
          with connection.cursor() as cursor:
            cursor.execute(f"SELECT username FROM user WHERE username = '{value.data}'")
            result = cursor.fetchall()
         usernames = [row[0] for row in result]
         if value.data in usernames:
            raise ValidationError('Username already exists! Please use a different username.')

    def validate_email_address(self, value):
        #cursor = mysql.connection.cursor()
        with mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DB
        ) as connection:
          with connection.cursor() as cursor:
            cursor.execute(f"SELECT email_address FROM user WHERE email_address = '{value.data}'")
            result = cursor.fetchall()
        email_addresses = [row[0] for row in result]
        if value.data in email_addresses:
            raise ValidationError('Email Address already exists! Please use a different Email Address.')


    username = StringField(label='User Name', validators=[Length(min=5, max=20), DataRequired()])
    email_address = StringField(label='Email Address', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password', validators=[Length(min=8), DataRequired()])
    password2 = PasswordField(label='Confirm Password', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    username = StringField(label='User Name', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')
