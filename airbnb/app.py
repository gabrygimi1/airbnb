import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

def create_table():
    conn = sqlite3.connect('guests.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS guests
                 (id INTEGER PRIMARY KEY, fullname TEXT, birthdate TEXT, gender TEXT, nationality TEXT, 
                 document_type TEXT, document_number TEXT, issue_date TEXT, expiration_date TEXT, 
                 residence_country TEXT, street_address TEXT, city TEXT, province TEXT, zip_code TEXT,
                 document_front BLOB, document_back BLOB)''')
    conn.commit()
    conn.close()

def insert_guest_data(fullname, birthdate, gender, nationality, document_type, document_number, issue_date, expiration_date, 
                      residence_country, street_address, city, province, zip_code, document_front, document_back):
    conn = sqlite3.connect('guests.db')
    c = conn.cursor()
    c.execute('''INSERT INTO guests (fullname, birthdate, gender, nationality, document_type, document_number, issue_date, expiration_date, 
                                     residence_country, street_address, city, province, zip_code, document_front, document_back)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                 (fullname, birthdate, gender, nationality, document_type, document_number, issue_date, expiration_date, 
                  residence_country, street_address, city, province, zip_code, document_front, document_back))
    conn.commit()
    conn.close()

@app.route('/view_guests')
def view_guests():
    conn = sqlite3.connect('guests.db')
    c = conn.cursor()
    c.execute("SELECT * FROM guests")
    guests = c.fetchall()
    conn.close()
    return render_template('view_guests.html', guests=guests)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/guest_information', methods=['POST'])
def guest_information():
    if request.method == 'POST':
        num_guests = int(request.form['num_guests'])
        language = request.form['language']
        return render_template('guest_information.html', num_guests=num_guests, language=language)
    else:
        return redirect('/')

@app.route('/thank_you', methods=['POST'])
def thank_you():
    if request.method == 'POST':
        num_guests = int(request.form['num_guests'])
        language = request.form['language']
        for guest in range(num_guests):
            fullname = request.form[f'fullname{guest}']
            birthdate = request.form[f'birthdate{guest}']
            gender = request.form[f'gender{guest}']
            nationality = request.form[f'nationality{guest}']
            document_type = request.form[f'document_type{guest}']
            document_number = request.form[f'document_number{guest}']
            issue_date = request.form[f'issue_date{guest}']
            expiration_date = request.form[f'expiration_date{guest}']
            residence_country = request.form[f'residence_country{guest}']
            street_address = request.form[f'street_address{guest}']
            city = request.form[f'city{guest}']
            province = request.form[f'province{guest}']
            zip_code = request.form[f'zip_code{guest}']
            document_front = request.files[f'document_front{guest}'].read()
            document_back = request.files[f'document_back{guest}'].read()

            insert_guest_data(fullname, birthdate, gender, nationality, document_type, document_number, issue_date, expiration_date, 
                              residence_country, street_address, city, province, zip_code, document_front, document_back)

        return redirect('/view_guests')
    else:
        return redirect('/')

if __name__ == '__main__':
    create_table()
    app.run(debug=True)


