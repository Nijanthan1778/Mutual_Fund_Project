from flask import Flask,render_template,request,redirect,url_for
import requests,sqlite3

app=Flask(__name__)
url="https://api.mfapi.in/mf/"
@app.route("/",methods=["GET","POST"])
def home():
    
    conn=sqlite3.connect("mutualFund.db")
    conn.row_factory=sqlite3.Row
    cur=conn.cursor()
    cur.execute("Select * from users")
    data=cur.fetchall()   
    return render_template("home.html",d=data)
   
@app.route("/add",methods=["GET","POST"])
def add():
    if request.method=="POST":
        name=request.form.get("name")
        fundCode=request.form.get("fund_code")
        unitHeld=request.form.get("unit_held")
        investedAmount=request.form.get("invested_amount")
        req=requests.get(url+fundCode)
        data2=req.json()
        fundHouse=data2["meta"]["fund_house"]
        nav=data2["data"][0]["nav"]
        currentValue=float(nav)*int(investedAmount)
        growth=float(currentValue)-int(unitHeld)
        conn=sqlite3.connect("mutualFund.db")
        cur=conn.cursor()
        cur.execute("Insert into users(NAME,FUNDCODE,INVESTEDAMOUNT,UNITHELD,FUNDNAME,NAV,CURRENTVALUE,GROWTH) values(?,?,?,?,?,?,?,?)",
                (name,fundCode,investedAmount,unitHeld,fundHouse,nav,currentValue,growth)) 
        conn.commit() 
        return redirect(url_for("home"))
    return render_template("add.html")

@app.route("/edit/<string:id>",methods=["GET","POST"])
def edit(id):
    if request.method=="POST":
        name=request.form.get("name")
        fundCode=request.form.get("fund_code")
        unitHeld=request.form.get("unit_held")
        investedAmount=request.form.get("invested_amount")
        req=requests.get(url+fundCode)
        data3=req.json()
        fundHouse=data3["meta"]["fund_house"]
        nav=data3["data"][0]["nav"]
        currentValue=float(nav)*int(investedAmount)
        growth=float(currentValue)-int(unitHeld)
        conn=sqlite3.connect("mutualFund.db")
        cur=conn.cursor()
        cur.execute("Update users set Name=?, FundCode=?, UnitHeld=?, InvestedAmount=?, FundName=?, Nav=?, CurrentValue=?, Growth=? where ID=?",
                (name,fundCode,investedAmount,unitHeld,fundHouse,nav,currentValue,growth,id)) 
        conn.commit() 
        return redirect(url_for("home"))

    conn=sqlite3.connect("mutualFund.db")
    conn.row_factory=sqlite3.Row
    cur=conn.cursor()
    cur.execute("Select * from users where ID=?",(id,))
    data=cur.fetchone()   
    return render_template("edit.html",d=data)  

@app.route("/delete/<string:id>") 
def delete(id):
    conn=sqlite3.connect("mutualFund.db")
    cur=conn.cursor()
    cur.execute("Delete from users where ID=?",(id,))
    conn.commit()
    return redirect(url_for("home"))


if "__main__"==__name__:
    app.run(debug=True)