from flask import Flask,render_template,redirect,request,session,flash
from cs50 import SQL
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from pytz import timezone
from datetime import datetime


app = Flask(__name__)


# for using database and session
db = SQL("sqlite:///database.db")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# for login
@app.route('/',methods=["GET","POST"])
def login():
    session.clear()
    if request.method=="GET":
        return render_template('login.html')
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")
        # mandatory fields error
        if not username:
            error = "username cannot be empty"
            return render_template("login.html",error=error)
        if not password:
            error="password cannot be empty"
            return render_template("login.html",error=error)
        rows = db.execute("SELECT * FROM users WHERE username = ?",request.form.get("username"))
        # verifies the and login the user
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            error="invalid username or password"
            return render_template("login.html",error=error)
        session["user_id"] = rows[0]["id"]
        return redirect("/index")



# for register
@app.route('/register',methods=["GET","POST"])
def register():
    if request.method=="GET":
        return render_template("register.html")
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")
        confirmation=request.form.get("confirmation")
        hash_password = generate_password_hash(password)
        # mandatory fields error
        if not username:
            error = "username cannot be empty"
            return render_template("register.html",error=error)
        if not password:
            error="password cannot be empty"
            return render_template("register.html",error=error)
        if not confirmation:
            error=" confirm password cannot be empty"
            return render_template("register.html",error=error)
        if password!=confirmation:
            error="passwords do not match"
            return render_template("register.html",error=error)

        rows = db.execute("SELECT * FROM users WHERE username = ?",request.form.get("username"))
        # for unique user id
        if len(rows)>0:
            error="User already exist! Try different username Or login"
            return render_template("register.html",error=error)
        else:
            # insering into database
            db.execute("INSERT into users (username,password) VALUES(?,?)", username, hash_password)
        return redirect("/")

# login required function
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            flash('You need to login first!')
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function


# for bid
@app.route('/index',methods=["GET","POST"])
@login_required
def index():
    if request.method=="GET":
        return render_template("index.html")
    if request.method=="POST":
        username=request.form.get("username")
        product=request.form.get("product")
        bid=request.form.get("bid")
        checkbox=request.form.get('checkbox')
        list=db.execute("select max(bid) as bid from history")
        winner=list[0]['bid']
        user_id = session["user_id"]
        user=db.execute("select username from users where id=?",user_id)
        # check username
        if user[0]['username']!=username:
            error = "Enter your username only"
            return render_template("index.html",error=error,winner=winner)

        # for base price
        if winner==None:
            winner=0
        try:
            if int(bid) < int(winner):
                error = "Your Bid is invalid"
                return render_template("index.html",error=error,winner=winner)
        except TypeError:
                winner=0
                error="fetchin data"
                return render_template("index.html",error=error,winner=winner)

        if not checkbox:
            error = "Accept Terms and Condition"
            return render_template("index.html",error=error)
        if not username:
            error = "username cannot be empty"
            return render_template("index.html",error=error)
        if not bid:
            error = "Bid price cannot be empty"
            return render_template("index.html",error=error)
        if not product:
            error = "Product name cannot be empty"
            return render_template("index.html",error=error)
        # indian time
        ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d(%H:%M:%S)')
        user_id = session["user_id"]
        # inserting into database
        db.execute("INSERT into history (username,user_id,product,bid,date) VALUES(?,?,?,?,?)",username,user_id,product,bid,ind_time)
        return redirect('/history')


# for history
@app.route('/history',methods=["GET","POST"])
@login_required
def history():
    if request.method=="GET":
        history=db.execute("SELECT * FROM history")
        return render_template("history.html",history=history)

# for winner
@app.route('/winner',methods=["GET","POST"])
@login_required
def winner():
    if request.method=="GET":
        list=db.execute("select max(bid) as bid from history")
        winner=list[0]['bid']
        user_id = session["user_id"]
        name=db.execute("select username from history where user_id=?",user_id)
        history=db.execute("select * from history where bid=?",winner)
        # if same user who won the bid
        if name[0]['username']==history[0]['username']:
            return render_template("payment.html",winner=winner,history=history)
        # if user who did't win the bid
        return render_template("winner.html",winner=winner,history=history)
    if request.method=="POST":
        address=request.form.get("address")
        if not address:
            error = "username cannot be empty"
            return render_template("payment.html",error=error)
        return

# for logout
@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect('/')

# for payment and address page
@app.route('/payment',methods=["GET","POST"])
@login_required
def payment():
    if request.method=="POST":
        name=request.form.get("name")
        email=request.form.get("email")
        address=request.form.get("address")
        user_id = session["user_id"]
        list=db.execute("select max(bid) as bid from history")
        winner=list[0]['bid']
        history=db.execute("select * from history where bid=?",winner)
        if not name:
            error = "name cannot be empty"
            return render_template("payment.html",error1=error,winner=winner,history=history)
        if not email:
            error = "email cannot be empty"
            return render_template("payment.html",error2=error,winner=winner,history=history)
        if not address:
            error = "name cannot be empty"
            return render_template("payment.html",error3=error,winner=winner,history=history)
        address=db.execute("insert into address (user_id,name,email,address) values(?,?,?,?)",user_id,name,email,address)
        return redirect('/sold')

#  sold page
@app.route('/sold',methods=["GET","POST"])
@login_required
def sold():
    return render_template("sold.html")

if __name__ == '__main__':
    app.run(debug=True,port=8000)
