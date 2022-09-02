from ImageToText import app
from flask_mysqldb import MySQL

app.config['MYSQL_HOST'] = 'sql6.freesqldatabase.com'
app.config['MYSQL_USER'] = 'sql6508670'
app.config['MYSQL_PASSWORD'] = 'KrTCeavdD3'
app.config['MYSQL_DB'] = 'sql6508670'

mysql = MySQL(app)