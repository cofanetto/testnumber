from flask import Blueprint,render_template,request,redirect,url_for,session
from config import *
import pymysql
import os

con = pymysql.connect(HOST,USER,PASS,DB)
member = Blueprint('member',__name__)

@member.route("/showmember")
def Showdatamember():
    if "username" not in session:
        return render_template("login/login.html")
    with con :
        cur = con.cursor()
        sql = "select * from tb_member"
        cur.execute(sql)
        rows = cur.fetchall()
    return render_template("Showdatamember.html",headername = "แสดงข้อมูลสมาชิก",data = rows)

@member.route("/showwithsex",methods=["post"])
def showwithsex():
    if "username" not in session:
        return render_template("login/login.html")
    if request.method == "POST":
        dstart = request.form["dtstart"]
        dend = request.form["dtend"]
        with con :
            cur = con.cursor()
            sql = "select * from tb_member where mem_bddate between %s and %s"
            cur.execute(sql,(dstart,dend))
            rows = cur.fetchall()
        return render_template("Showdatamember.html",headername = "แสดงข้อมูลสมาชิก",data = rows)

@member.route("/editmember",methods=["post"])
def Editmember():
    if request.method == "POST":
        id = request.form["ID"]
        fname = request.form["FNAME"]
        lname = request.form["LNAME"]
        sex = request.form["SEX"]
        bdate = request.form["BDATE"]
        email = request.form["EMAIL"]
        file = request.files["imagemem"]

        if file.filename == "":
            with con:
                cur = con.cursor()
                sql = "update tb_member set mem_fname = %s , mem_lname = %s  where mem_id = %s"
                cur.execute(sql,(fname,lname,id))
                con.commit()
                return redirect(url_for('member.Showdatamember'))
        else:
            file = request.files['imagemem']
            upload_folder = 'static/images'
            app_folder = os.path.dirname(__file__)
            img_folder = os.path.join(app_folder,upload_folder)
            file.save(os.path.join(img_folder,file.filename))
            path = upload_folder + "/" + file.filename
            with con:
                cur = con.cursor()
                sql = "update tb_member set mem_fname = %s , mem_lname = %s , mem_pic = %s where mem_id = %s"
                cur.execute(sql,(fname,lname,path,id))
                con.commit()
                return redirect(url_for('member.Showdatamember'))


@member.route("/deletemember",methods=["post"])
def delmember():
    if request.method == "POST":
        id = request.form["id"]
        with con :
            cur = con.cursor()
            sql = "delete from tb_member where mem_id = %s"
            cur.execute(sql,id)
            con.commit()
            return redirect(url_for('member.Showdatamember'))

@member.route("/adddatamember")
def adddatamember():
    if "username" not in session:
        return render_template("login/login.html")
    else :
        return render_template("adddatamember.html")

@member.route("/addmember",methods=["POST"])
def adddata():
    if request.method == "POST":
        file = request.files['imagemem']
        upload_folder = 'static/images'
        app_folder = os.path.dirname(__file__)
        img_folder = os.path.join(app_folder,upload_folder)
        file.save(os.path.join(img_folder,file.filename))
        path = upload_folder + "/" + file.filename

        fname = request.form["FNAME"]
        lname = request.form["LNAME"]
        sex = request.form["SEX"]
        bdate = request.form["BDATE"]
        email = request.form["EMAIL"]
        with con :
            cur = con.cursor()
            sql = "insert into tb_member (mem_fname , mem_lname , mem_sex , mem_bddate , mem_email ,mem_pic) values(%s,%s,%s,%s,%s,%s)"
            cur.execute(sql,(fname,lname,sex,bdate,email,path))
            con.commit()
            return redirect(url_for('member.Showdatamember'))
