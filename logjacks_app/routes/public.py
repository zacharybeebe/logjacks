from logjacks_app import app, db, request, render_template, redirect, url_for, session, send_file
from logjacks_app.routes import private
from logjacks_app.database.authentication import check_login, get_user, check_create_account, initialize_user, disengage_user

@app.route('/')
@app.route('/home')
def index():
	return render_template('public/index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
	if request.method == 'POST':
		check, user_or_error = check_login(request.form['username'], request.form['password'])
		if not check:
			if user_or_error == 'Incorrect Username':
				return render_template('public/login.html', flash=user_or_error, username='')
			else:
				return render_template('public/login.html', flash=user_or_error, username=request.form['username'])
		else:
			initialize_user(user_or_error, session)
			app.logger.info(f'{user_or_error.username} logged in successfully')
			return redirect(url_for('dashboard', username=user_or_error.username))
	else:
		if 'user' in session:
			return redirect(url_for('dashboard', username=session['user']))
		else:
			return render_template('public/login.html', username='')


@app.route('/create_account', methods=['POST', 'GET'])
def create_account():
	data = {
		'f_name': '',
		'l_name': '',
		'email': '',
		'phone': '',
		'company': '',
		'username': ''
	}
	flash = None
	if request.method == 'POST':
		print(request.form)
		error, data, user_or_flash = check_create_account(request.form)
		print(f'{data=}')
		if not error:
			user = user_or_flash
			initialize_user(user, session)
			app.logger.info(f'{user.username} logged in successfully')
			return redirect(url_for('dashboard', username=user.username))
		else:
			flash = user_or_flash
	return render_template('public/create_account.html', data=data, flash=flash)


@app.route('/<username>/logout')
def logout(username):
	disengage_user(session)
	app.logger.info(f'{username} logged out successfully')
	return redirect(url_for('index'))

