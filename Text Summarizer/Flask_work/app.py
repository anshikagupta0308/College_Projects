from flask import Flask, render_template,request,redirect
import mysql.connector
from main import text_summarizer
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Datopic123#",
  database="test"
)
mycursor = mydb.cursor()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login_validation', methods=['POST'])
def login_validation():
    email = request.form.get('email')
    password = request.form.get('password')
    mycursor.execute("""SELECT * FROM `logindata` where `email` LIKE '{}' AND `password` LIKE '{}' """ .format(email,password))
    myresult = mycursor.fetchall()

    if len(myresult) > 0:
        return redirect("/home")
    else:
        return redirect("/")


@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form.get('uname')
    email = request.form.get('uemail')
    password = request.form.get('upassword')
    mycursor.execute(
        """INSERT INTO `logindata` (`Name`,`Email`,`Password`) VALUES ('{}','{}','{}')""".format(name,email, password))
    mydb.commit()
    return redirect("/home")

@app.route('/summ', methods=['POST'])
def summ():
    text = request.form.get('text')
    len_text= len(text.split())
    ntext = text_summarizer(text)
    len_ntext = len(ntext.split())
    return render_template('home.html', final_summary=ntext, len_ntext = len_ntext, len_text=len_text)




if __name__ == "__main__":
    app.run(debug = True)