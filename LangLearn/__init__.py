from flask import Flask
import mysql.connector
from flask_login import LoginManager
from LangLearn import routes 

app = Flask(__name__)
database = mysql.connector.connect(host="localhost",
                                   user="root",
                                   password="SamWorks4SQL!",
                                   database ="cs350")

cursor = database.cursor(buffered=True)
app.config['SECRET_KEY'] = 'bba84d04f76682deddf3cfacb7e2fe10'
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

