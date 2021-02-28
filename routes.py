from cs350_proj.models import Student, logged_in_users
from cs350_proj import app, database, cursor
from flask import render_template, url_for, flash, redirect, request, Markup
from cs350_proj.forms import RegisterationForm, LoginForm, UpdateAccountForm, SelectLanguageForm, DeleteLanguageForm
from flask_login import login_user, current_user, logout_user, login_required

posts = [
    {
        'author': 'Langlearn', 
        'title': 'New languages added!',
        'content': 'Register now to start learning..',
        'Date_Posted': 'April 9, 2020' 
    },
    {
        'author': 'Langlearn', 
        'title': 'our newsletter',
        'content': "what's new!",
        'Date_Posted': 'April 10, 2020'
    }
]

questions = [
    {
        'author': 'std 1', 
        'title': 'question 1',
        'content': 'First post Contet',
        'Date_Posted': 'April 9, 2020' 
    },
    {
        'author': 'std 2', 
        'title': 'question 2',
        'content': 'Second post Contet',
        'Date_Posted': 'April 10, 2020'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about") 
def about():
    return render_template("about.html", title="About")


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated: 
        return redirect("/home")
    form = RegisterationForm()
    if form.validate_on_submit():
        password = form.password.data
        username = form.username.data 
        email = form.email.data
        registering_std = Student(email, password)
        cursor.execute("select * from student")
        all_users = cursor.fetchall()
        check = True
        for user in all_users:
            if user[2] == email:    
                check = False
            elif user[1] == username: 
                check = False
        if check == True:
            registering_std.register(username)
            registering_std.set_id()
            registering_std.set_username()
            flash(f'Account created for {form.username.data}!', 'Success')
            return redirect("/login")
        else:
            return redirect("/register")
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: 
        return redirect("/home")
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        std = Student(email, password)
        cursor.execute("select username from student where email = %s",[email])
        username = cursor.fetchone()[0]
        std.username = username 
        cursor.execute("select SID from student where email = %s",[email])
        sid = cursor.fetchone()[0]
        std.id = sid 
        if std.login(): 
            logged_in_users.append(std)
            login_user(std, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('you have been loggd in!', 'success') 
            return redirect(next_page) if next_page else redirect("/home")
        else: 
            flash('log in unsuccessful, invalid input', 'danger')   
            return redirect("/login")
    return render_template('login.html', title='login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    if len(logged_in_users) != 0:
        logged_in_users.pop(0)
    return render_template('home.html', posts=posts)


@app.route("/Forum")
def forum():
    if not current_user.is_authenticated: 
        flash('log in to access this page', 'danger')
        return redirect("/login")
    return render_template("Forum.html", title="Forum", posts=questions)


@app.route("/classes")
@login_required
def classes():
    form = DeleteLanguageForm()
    if request.method == 'POST':
        # I was working on this ( not finished )
        cursor.execute('select distinct language from class,takes where std_id = %s',[current_user.id])
        langs = cursor.fetchall()
        choices = []
        for lang in langs: 
            choices.append((lang[0], lang[0]))
            cursor.execute('select level from class,takes where language = %s and std_id=%s',[lang[0], current_user.id ])
            lvls = cursor.fetchall()
            print(lvls)
            choices_lvl = []
            for lvl in lvls: 
                choices_lvl.append((lvl[0], lvl[0]))

        form.language.choices = choices
        form.level.choices = choices_lvl

        # level
        cursor.execute('select distinct level from class,takes where std_id = %s',[current_user.id])
        lvls = cursor.fetchall()
        choices = []
        for lvl in lvls: 
            choices.append((lvl[0], lvl[0]))

    # loading classes 
    sid = current_user.id
    cursor.execute('select language,level,CID from class,takes where CID = cls_id and std_id = %s;',[sid])
    taken_classes = cursor.fetchall()
    
    return render_template("classes.html", title="Classes", posts=taken_classes, form=form)

@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.username.data != current_user.username:
            current_user.username = form.username.data
            print(current_user.id)
            cursor.execute("UPDATE student SET username = %s WHERE SID = %s;",[form.username.data,current_user.id])
            database.commit()
        if form.email.data != current_user.email:
            current_user.email = form.email.data
            cursor.execute("UPDATE student SET email = %s WHERE SID = %s;",[form.email.data,current_user.id])
            database.commit()
        flash('your account has been updated', 'success')
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template("profile.html", title='Account', image_file=image_file, form = form)


@app.route("/languages", methods=['GET', 'POST'])
@login_required
def languages():
    form = SelectLanguageForm()
    if request.method == 'POST':
        lan = form.language.data
        lvl = form.level.data
        cursor.execute("select CID from class where language = %s and level = %s",[lan,lvl])
        cid = cursor.fetchone()[0]
        print(current_user.username)
        cursor.execute("insert into takes ( std_id , cls_id ) values ( %s, %s)",[current_user.id, cid])
        database.commit()
        flash('Class Added, click here to access it', 'success')
    return render_template("languages.html", form=form)


@app.route('/delete')
def delete():
    if current_user.is_authenticated: 
        username = current_user.username
        cursor.execute("select SID from student where username = %s ",[username])
        sid = cursor.fetchone()[0]
        cursor.execute("DELETE from student where SID = %s ",[sid])
        database.commit()
        flash('your account has been deleted', 'success')
        logout_user()
        if len(logged_in_users) != 0:
            logged_in_users.pop(0)
    return render_template('home.html', posts=posts)

@app.route("/classes/<class_id>")
@login_required
def language_class(class_id):
    cursor.execute('select file_path from class,takes where CID = %s',[class_id])
    file_path = cursor.fetchone()[0]
    cursor.execute('select language, level from class where CID=%s',[class_id])
    lang_lvl = cursor.fetchone()
    value = [file_path, lang_lvl[0], lang_lvl[1]]
    return render_template("language_class.html", title="Classes", value=value)


@app.route("/teacher_login", methods=['GET', 'POST'])
def teacher_login():
    return render_template('login_teacher.html', title='login')