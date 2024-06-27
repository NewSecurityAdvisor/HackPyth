from flask import Flask, render_template, request, url_for, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.file import FileField
from sqlalchemy import text
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.datetime import DateField
from wtforms.fields.numeric import DecimalField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from werkzeug.utils import secure_filename
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
from ticket import app, db



# Set up rate limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=3)])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password1 = PasswordField('Password', validators=[DataRequired(), Length(min=3)])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password1')])
    submit = SubmitField('Register')
class TicketEntryForm(FlaskForm):
    Artist = StringField('Artist', validators=[DataRequired()])
    EventDate = DateField('Event Date', format='%Y-%m-%d', validators=[DataRequired()])
    Price = DecimalField('Price ($)', places=2, validators=[DataRequired()])
    SellerName = StringField('Seller Name', validators=[DataRequired()])
    Description = TextAreaField('Description')
    Image = FileField('Upload Image')
    submit = SubmitField('Enter')


@app.route('/')
def home_page():
    cookie = session.get('name')
    return render_template('home.html', cookie=cookie)


@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login_pages():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        query_stmt = text("SELECT username FROM bugusers WHERE username = :username AND password = :password")
        result = db.session.execute(query_stmt, {'username': username, 'password': password})
        user = result.fetchall()

        if not user:
            flash("Username or Password wrong", category='warning')
            return render_template('login.html', form=form, cookie=None)

        session['name'] = username
        return redirect('/tickets')

    return render_template('login.html', form=form, cookie=None)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password1 = form.password1.data

        query_stmt = text("SELECT * FROM bugusers WHERE username = :username")
        result = db.session.execute(query_stmt, {'username': username})
        item = result.fetchone()

        if item is not None:
            flash("Username exists, try again")
            return render_template('register.html', form=form, cookie=None)

        query_insert = text(
            "INSERT INTO bugusers (username, email_address, password) VALUES (:username, :email, :password)")
        db.session.execute(query_insert, {'username': username, 'email': email, 'password': password1})
        db.session.commit()
        flash("You are registered", category='success')
        session['name'] = username
        return redirect('/tickets')

    return render_template('register.html', form=form)


@app.route('/tickets')
def tickets():
    cookie = session.get('name')
    if not cookie:
        return redirect(url_for('login_pages'))

    query_stmt = text("SELECT * FROM tickets")
    result = db.session.execute(query_stmt)
    itemsquery = result.fetchall()

    return render_template('tickets.html', items=itemsquery, cookie=cookie)


@app.route('/logout')
def logout():
    session.pop('name', None)
    return redirect('/')


@app.route('/ticket_entry', methods=['GET', 'POST'])
def ticket_entry():
    cookie = session.get('name')
    if not cookie:
        return redirect(url_for('login'))

    form = TicketEntryForm()
    if form.validate_on_submit():
        artist = form.artist.data
        date = form.date.data
        sellername = form.sellername.data
        price = form.price.data
        description = form.description.data
        image = form.image.data

        # Handle image upload
        if image and image.filename != '':
            filename = secure_filename(image.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(filepath)
        else:
            filename = None

        query_insert = text("""
        INSERT INTO tickets (Artist, Description, EventDate, Price, SellerName, ImagePath)
        VALUES (:artist, :description, :date, :price, :sellername, :filename)
        """)
        db.session.execute(query_insert, {
            'artist': artist, 'description': description, 'date': date,
            'price': price, 'sellername': sellername, 'filename': filename
        })
        db.session.commit()

        return redirect('/tickets')

    return render_template('ticket_entry.html', cookie=cookie, form=form)


@app.route('/ticket_item/<item_id>', methods=['GET'])
def ticket_item(item_id):
    query_stmt = text("SELECT * FROM tickets WHERE TicketID = :item_id")
    result = db.session.execute(query_stmt, {'item_id': item_id})
    item = result.fetchone()
    if not item:
        print("item not existing")

    cookie = session.get('name')
    return render_template('ticket_item.html', items=item, cookie=cookie)


if __name__ == '__main__':
    app.run(debug=True)
