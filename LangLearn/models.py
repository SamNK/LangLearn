from flask_login import LoginManager, UserMixin, login_user, current_user
from LangLearn import app, database, cursor, login_manager
from flask_login import login_user

logged_in_users = []
@login_manager.user_loader
def load_user(user_id):
    if len(logged_in_users) != 0: 
        user = logged_in_users[0]
        return user 
    else: 
        return None 

class Student(UserMixin): 
    def __init__(self, email, password, id=None):
        
        self.email = email 
        self.password = password 
        self.image_file = 'default.jpg'
        self.id = id
        
    def login(self):
        cursor.execute("select * from student where email = %s and password = %s",[self.email, self.password])
        user = cursor.fetchall()
        if len(user) == 1:  
            return True
        else: 
            return False

    def register(self, username): 
        cursor.execute("insert into student(username,email,password)"
                        "values(%s,%s,%s)",(username,self.email,self.password))
        database.commit()
    
    def set_id(self):
        cursor.execute('select * from student where email = %s',[self.email])
        self.id = cursor.fetchone()[0]
        return self.id
    
    def set_username(self):
        cursor.execute('select * from student where email = %s',[self.email])
        self.username = cursor.fetchone()[1]
        return self.username
