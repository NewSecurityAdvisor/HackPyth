from ticket import app, db
from flask import render_template, request, flash, url_for, redirect
from sqlalchemy import text

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login_pages():
    print("login was called")

    if request.method == 'POST':
        username = request.form.get('Username')
        password = request.form.get('Password')
        print("Here the Data!!!")
        print(username)
        print(password)

        if (username is None or
                isinstance(username, str) is False or
                len(username) < 3):
            print("not valid")
            flash(f"Username is not valid", category='warning')
            return render_template('login.html')

        if (password is None or
                isinstance(password, str) is False or
                len(password) < 3):
            print("something with password")
            flash(f"Password is not valid", category='warning')
            return render_template('login.html')

        query_stmt = f"select username from bugusers where username = '{username}' and password = '{password}'"
        print(query_stmt)
        result = db.session.execute(text(query_stmt))

        user = result.fetchall()
        #print("debug1")
        if not user:
            flash(f"Try again", category='warning')
            #print("debug2")
            return render_template('login.html')
        #print("debug3")
        flash(f"'{user}', you are logged in ", category='success')
        #print("debug4")
        return redirect(url_for('tickets_pages'))
        #return render_template('tickets.html')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        print('Post')

        username = request.form.get('Username')
        email = request.form.get('Email')
        password1 = request.form.get('Password1')
        password2 = request.form.get('Password2')

        print(username)
        print(email)
        print(password1)
        print(password2)

        if(username is None or
                isinstance(username, str) is False or
                len(username) < 3):
            print("username not valid")
            flash("Username not valid", category='danger')
            return render_template('register.html')

        if(email is None or
                isinstance(email, str) is False or
                len(email) < 3):
            print("email not valid")
            flash("Email not valid", category='danger')
            return render_template('register.html')

        if(password1 is None or
                isinstance(password1, str) is False or
                len(password1) < 3 or
                password1 != password2):
            print("password1 not valid")
            flash("Password1 not valid", category='danger')
            return render_template('register.html')

        query_stmt = f"select * from bugusers where username = '{username}'"
        print(query_stmt)
        result = db.session.execute(text(query_stmt))
        item = result.fetchone()
        print(item)

        if item is not None:
            flash("Username exists, try again")
            print("Username exists")
            return render_template('register.html')

        query_insert = f"insert into bugusers (username, email_address, password) values ('{username}', '{email}', '{password1}')"
        print(query_insert)
        db.session.execute(text(query_insert))
        db.session.commit()
        flash("You are registered", category='success')
        return redirect(url_for('tickets_pages'))

    return render_template('register.html')

@app.route('/tickets')
def tickets_pages():

#    items = [{"id": 1, "prio": 2, "user": "Mark", "title":"backend broken"},
#             {"id": 2, "prio": 1, "user": "Luke", "title":"GUI not working"},
#             {"id": 3, "prio": 2, "user": "Han", "title":"Nothing works"}]

    query_stmt = f"select * from bugitems"
    result = db.session.execute(text(query_stmt))
    itemsquery = result.fetchall()

    print(itemsquery)

    return render_template('tickets.html', items=itemsquery)


