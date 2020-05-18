from flask import Blueprint,render_template,request,redirect,url_for,session,flash
from config import *
import pymysql

con = pymysql.connect(HOST,USER,PASS,DB)
user = Blueprint('user',__name__)

@user.route("/loginpage")
def loginpage():
    if "username" not in session:
        return render_template("login/login.html")
    else:
        return redirect(url_for("member.Showdatamember"))

@user.route("/checklogin",methods=["POST"])
def checklogin():
    user = request.form["username"]
    passw = request.form["password"]
    with con:
        cur = con.cursor()
        sql = "select * from tb_user where user_username = %s and user_password = %s and user_status = 1"
        cur.execute(sql,(user,passw))
        rows = cur.fetchall()
        if len(rows) >0:
            session["username"] = user
            session["name"] = rows[0][1]
            session.permanent = True
            print(session)
            return redirect(url_for("member.Showdatamember"))
        else:
            flash("ไม่พบข้อมูลในระบบ")
            return render_template("login/login.html")

@user.route("/logoff")
def logoff():
    session.clear()
    return redirect(url_for("user.loginpage"))

@user.route("/regisuser")
def regisuser():
    return render_template("adduser.html")

@user.route("/adduser",methods=["POST"])
def adduser():
    if request.method == "POST":
        fname = request.form["FNAME"]
        lname = request.form["LNAME"]
        user = request.form["USER"]
        passw = request.form["PASS"]
        repass = request.form["REPASS"]
        if passw != repass:
            flash("Password และ RE-Password ไม่เหมือนกัน")
            return render_template("adduser.html")
        with con :
            cur = con.cursor()
            sql = "insert into tb_user  (user_fname , user_lname , user_username , user_password ) values(%s,%s,%s,%s)"
            cur.execute(sql,(fname,lname,user,passw))
            con.commit()
            flash("สมัครสมาชิกเรียบร้อย !!")
            return render_template("login.html",status = "wait")
