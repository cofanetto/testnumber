from flask import Flask , render_template
from Member import *
from User import *
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "number"
app.permanent_session_lifetime = timedelta(days=1)
app.register_blueprint(member)
app.register_blueprint(user)

@app.route("/")
def Index():
    if "username" not in session:
        return render_template("login/login.html")
    else:
        return redirect(url_for("member.Showdatamember"))


if __name__ == '__main__':
    app.run(debug = True)
