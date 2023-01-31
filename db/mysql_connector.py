import mysql.connector
# pip install mysql-connector-python

DB_ECHO: bool = True
DB_HOST: str = '59.68.29.90'
DB_PORT: int = 3306
DB_USER: str = 'root'
DB_PASSWORD: str = '4402115bac2c1c68'
DB_DATABASE: str = 'sabala'
DB_CHARSET: str = 'utf8mb4'
"Xirú Missioneiro"


mydb = mysql.connector.connect(
  host=DB_HOST,
  user=DB_USER,
  password=DB_PASSWORD,
  database=DB_DATABASE
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM m_song")

myresult = mycursor.fetchall()

for x in myresult:
  print(x[-3], type(x[-3]))
  print(list(x[-3]))
  break