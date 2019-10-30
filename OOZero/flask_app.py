from OOZero import create_app
from flask import Flask, render_template, request, redirect, url_for, session, flash
from OOZero.user_model import authenticateUser, addUser, hashPassword, check_username
from OOZero.user_session import login_required, user_login, user_logout

app = create_app()

@app.route('/')
#@login_required
def home():
    try:
        if session['username']:
            return render_template('home.html', username=session['username'])
        return render_template('home.html')
    except:
        session['username'] = None
        return render_template('home.html')


@app.route('/login/', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        # Authenticate the given user with this username and password
        username = request.form['username']
        password = request.form['password']
        user = authenticateUser(username, password)
        if user:
            user_login(user)
            session['username'] = username
            return redirect(url_for('home'))
        else:
            error = 'Incorrect username or password entered.'

    return render_template('login.html', error=error)

@app.route('/signup/', methods=['POST', 'GET'])
def signup():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        name = request.form['name']

        # Need to check if username is already taken here
        check = check_username(username)
        if check:
            error = 'Username already taken.'
        else:
            addUser(username=username, password=password, name=name, email=email)
            session['username'] = username
            return redirect('/')
    return render_template('signup.html', error=error)

@app.route('/logout/', methods=['POST', 'GET'])
def logout():
    session['username'] = None
    user_logout()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run()
