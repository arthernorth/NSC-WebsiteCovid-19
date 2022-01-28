from flask import Flask 
from flask_mysqldb import MySQL 

app = Flask(__name__)

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'web-health_project'

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()

    cur.execute('''SELECT * FROM users''')
    results = cur.fetchall()
    print(results)
    return str(results[1])

if __name__ == '__main__':
   app.run(debug="on")
