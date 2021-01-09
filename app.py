import os
import json
import pandas as pd
from flask import Flask, render_template, redirect, url_for, flash, request, \
					send_from_directory
from sqlalchemy import create_engine
from quickstart import get_data
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key_4_Aviate_project'
UPLOAD_FOLDER = os.path.abspath(os.path.dirname(__file__)) + '/Data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'csv'}

@app.route('/')
def index():
	return render_template('home.html')

@app.route('/view', methods = ['GET', 'POST'])
def view_data():
	data = get_data()
	engine = create_engine('sqlite:///personal_info.db', echo=True)
	sqlite_connection = engine.connect()
	sqlite_table = "PersonalInfo"
	data.to_sql(sqlite_table, sqlite_connection, index=False, if_exists='append')
	data = pd.read_sql_table('PersonalInfo', engine)
	data = data.drop_duplicates()
	data.to_sql(sqlite_table, sqlite_connection, index=False, if_exists='replace')
	sqlite_connection.close()
	data = data.to_dict('records')
	return render_template('view.html', data = json.dumps(data))

@app.route('/add', methods=['GET', 'POST'])
def add_data():
	return render_template('add_data.html')

@app.route('/add_form', methods=['GET', 'POST'])
def add_data_form():
	return render_template('add_data_form.html', columns=get_data().columns.values)

@app.route('/add_file', methods=['GET', 'POST'])
def add_data_file():
	return render_template('add_data_file.html')

@app.route('/success_form', methods=['GET', 'POST'])
def success_form():
	if request.method == 'POST':
		data = request.form
		engine = create_engine('sqlite:///personal_info.db', echo=True)
		sqlite_connection = engine.connect()
		sqlite_table = "PersonalInfo"
		data = pd.DataFrame(dict(data), index=[0])
		data.to_sql(sqlite_table, sqlite_connection, index=False, if_exists='append')
		data = pd.read_sql_table('PersonalInfo', engine)
		data = data.drop_duplicates()
		data.to_sql(sqlite_table, sqlite_connection, index=False, if_exists='replace')
		sqlite_connection.close()

		return redirect(url_for('view_data'))
	return render_template('add_data_form.html')

def allowed_file(filename):
	return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/success_file', methods=['GET', 'POST'])
def success_file():
	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)

		file = request.files['file']
		# if user does not select file, browser also
		# submit an empty part without filename

		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)

		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

			data = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			
			if all(data.columns.values == get_data().columns.values):
				engine = create_engine('sqlite:///personal_info.db', echo=True)
				sqlite_connection = engine.connect()
				sqlite_table = "PersonalInfo"
				data.to_sql(sqlite_table, sqlite_connection, index=False, if_exists='append')
				data = pd.read_sql_table('PersonalInfo', engine)
				data = data.drop_duplicates()
				data.to_sql(sqlite_table, sqlite_connection, index=False, if_exists='replace')
				sqlite_connection.close()

				return redirect(url_for('view_data'))

			else:
				flash('Column names do not match')
				return render_template('add_data_file.html')

	return render_template('add_data_file.html')

@app.route('/download', methods=['GET', 'POST'])
def download():
	file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'test')
	return send_from_directory(directory=file_path, filename='test.csv', as_attachment=True)

if __name__ == '__main__':
	app.run()