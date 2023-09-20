from flask import Flask, render_template, json, request
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

mysql = MySQL()
# MySQL configurations 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Republic-C207*'
app.config['MYSQL_DB'] = 'BucketList'
app.config['MYSQL_HOST'] = 'localhost'

mysql.init_app(app)

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/api/signup',methods=['POST'])
def signUp():
    # read the posted values from the UI 
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']

    # validate the received values
    if _name and _email and _password:
        
        # connect to the database
        conn = mysql.connection
        cursor = conn.cursor()
        
        _hashed_password = generate_password_hash(_password)
        cursor.callproc('sp_createUser', (_name, _email, _hashed_password))
        data = cursor.fetchall()
        
        if len(data) == 0:
            conn.commit()
            return json.dumps({'message':'User created successfully !'})
        else:
            return json.dumps({'error':str(data[0])})
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})
        
if __name__ == "__main__":
    app.run()



