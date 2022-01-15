from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from flask import jsonify, make_response
import MySQLdb.cursors
import bcrypt

from datetime import timedelta
from features import login_func, check_trans, exec_trans, cek_saldo, history

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'sN16sdBjk77'
app.permanent_session_lifetime = timedelta(seconds=6000)

# Enter your database connection details below
conn = MySQLdb.connect("localhost","root","18agustus98","atm")

# Initialize MySQL
mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']

        salt = b'$2b$12$O4GGyQXRald97MZwuhurL.'
        hashed = bcrypt.hashpw(password.encode(), salt)

        # Check if account exists using MySQL
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM `server` WHERE `username` = %s AND `password` = %s', (username, hashed,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['username'] = account['username']
            session['password'] = account['password']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    return render_template('login.html', msg=msg)

def index ():
    response = {
        "status": 1,  # Success
        "message": "Welcome"
    }
    res = make_response(jsonify(response), 200)
    return res


@app.route('/home/')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('in_home.html', username=session['username'])
    # User is not loggedin redirect to login page
    else :
        return redirect(url_for('login'))

@app.route('/logout/')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('username', None)
   session.pop('password', None)
   # Redirect to login page
   return redirect(url_for('login'))

@app.route('/register/', methods=["GET","POST"])
def register():
# Check if user is loggedin
    if 'loggedin' in session:
        msg = ''
        # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'POST' and 'nama' in request.form and 'PIN' in request.form and 'rekening' in request.form and 'telepon' in request.form :
            # Create variables for easy access
            nama = request.form['nama']
            rekening = request.form['rekening']
            PIN = request.form['PIN']
            telepon = request.form['telepon']

            salt = b'$2b$12$O4GGyQXRald97MZwuhurL.'
            PIN_hashed = bcrypt.hashpw(PIN.encode(), salt)

            cursor = conn.cursor()
            cursor.execute('SELECT * FROM nasabah WHERE no_rek=%s',(rekening,))
            account = cursor.fetchone()
            # If account exists show error and validation checks
            if account:
                msg = 'Akun telah ada! Silakan ubah nomor rekening Anda.'
            elif not nama or not PIN or not telepon:
                msg = 'Silakan isi yang masih kosong!'
            else:
                # Account doesnt exists and the form data is valid, now insert new account into accounts table
                cursor.execute('INSERT INTO `nasabah` (no_rek, nama, no_telpon) VALUES (%s, %s, %s)', (rekening,nama,telepon, ))
                cursor.execute('INSERT INTO `auth` (magic_code) VALUES (%s)', (PIN_hashed,))
                conn.commit()
                msg = 'Registrasi berhasil!'
        return render_template('register.html', msg=msg)
    else :
        return redirect(url_for('login'))

@app.route('/histori/')
def histori():
    if 'loggedin' in session:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM histori_transaksi")
        data = cursor.fetchall()  # data from database
        # User is loggedin show them the home page
        return render_template('histori.html', value=data)
    # User is not loggedin redirect to login page
    else :
        return redirect(url_for('login'))

@app.route('/data/')
def data():
    if 'loggedin' in session:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM nasabah")
        data = cursor.fetchall()  # data from database
        # User is loggedin show them the home page
        return render_template('data.html', value=data)
    # User is not loggedin redirect to login page
    else :
        return redirect(url_for('login'))

@app.route('/update', methods=["POST"])
def update():
    id = request.form['id']
    nama = request.form['nama']
    telepon = request.form['telepon']

    cur = conn.cursor()
    cur.execute("UPDATE nasabah SET nama=%s, no_telpon=%s WHERE id_nasabah=%s", (nama,telepon,id,))
    conn.commit()
    return redirect(url_for('data'))

@app.route('/hapus/<string:id>', methods=["GET"])
def hapus(id):
    cur = conn.cursor()
    cur.execute("DELETE FROM auth WHERE id_nasabah=%s", (id,))
    cur.execute("DELETE FROM nasabah WHERE id_nasabah=%s", (id,))
    conn.commit()
    return redirect(url_for('data'))

@app.route('/isisaldo/', methods=["GET","POST"])
def isisaldo():
    # Check if user is loggedin
    if 'loggedin' in session:
        msg = ''
        # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'POST' and 'rekening' in request.form and 'saldo' in request.form :
            # Create variables for easy access
            rekening = request.form['rekening']
            saldo = request.form['saldo']

            cursor = conn.cursor()
            cursor.execute('SELECT * FROM nasabah WHERE no_rek=%s', (rekening,))
            account = cursor.fetchone()
            # If account exists show error and validation checks
            if not account:
                msg = 'No rekening tidak tersedia.'
            elif not rekening or not saldo:
                msg = 'Silakan isi yang masih kosong!'
            else:
                # Account doesnt exists and the form data is valid, now insert new account into accounts table
                select_stmt = "SELECT id_nasabah " \
                              "FROM nasabah " \
                              "WHERE no_rek =  %(no_rek)s"
                cursor.execute(select_stmt, {'no_rek': rekening})
                user = cursor.fetchall()
                id = user[0][0]

                kode = '1' #Isi Saldo
                cursor.execute('INSERT INTO `saldo` (id_nasabah, saldo) VALUES (%s,%s)',(id, saldo,))
                cursor.execute('INSERT INTO `histori_transaksi` (id_nasabah, kode_transaksi, rek_asal_atau_tujuan, jumlah_transaksi) VALUES (%s,%s,%s,%s)',(id, kode, rekening, saldo,))
                conn.commit()
                msg = 'Transaksi berhasil!'
        return render_template('isisaldo.html', msg=msg)
    else :
        return redirect(url_for('login'))


# Check Login Password
@app.route('/login', methods=['POST'])
def awal():
    res, id_nasabah, no_rek = login_func(mysql)
    return res

# Eksekusi Transfer
@app.route('/exec_transfer', methods=['POST'])
def exec_transfer():
    req = request.get_json()
    no_rek = req.get("no_rek")
    return exec_trans(mysql, no_rek)

# Cek Saldo
@app.route('/cek_saldo', methods=['GET'])
def cek():
    req = request.get_json()
    no_rek = req.get("no_rek")
    return cek_saldo(mysql, no_rek)

# Cek Histori Transaksi
@app.route('/history', methods=['GET'])
def history_transaksi():
    req = request.get_json()
    no_rek = req.get("no_rek")
    return history(mysql, no_rek)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
