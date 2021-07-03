from os import name
from flask import Flask, request, render_template, session, url_for, redirect
from flask.helpers import url_for
from werkzeug.utils import redirect
from werkzeug.wrappers import response
from flask_restful import Resource, Api
from flask_cors import CORS

#inisiasi object

app = Flask(__name__)
app.config["SECRET_KEY"] = "kovidituS14L"

@app.route("/", methods=["POST", "GET"])
def index():
    if "email" in session:
        return redirect(url_for('success_request'))
    


        ##kalau ada post untuk request
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        
        print("email : ", email)
        print("pass ; ", password)


        #kalau email dan password betul
        if email == 'sayacomel@gmail.com' and password == 'pass':
            session['email'] = email
            session['password'] = password

            return redirect(url_for('success_request'))

        #kalau salah
        else:
            return redirect(url_for('index'))

        # return render_template("index.html")
    return render_template("index.html")

@app.route("/success")
def success_request():
    nilai =  "Yeah dah boleh login!"
    return render_template("success.html", nilai=nilai)


@app.route("/logout")
def logout_acc():
    if "email" in session:
        session.pop("email")
        session.pop("password")
        return redirect(url_for('index'))
    
    else:

        return redirect(url_for('index'))


@app.route("/about")
def about():
    if "email" in session:
        return render_template("about.html")

    else:
        return redirect(url_for('index'))

@app.route("/contact")
def contact():
    if "email" in session:
        return render_template("contact.html")

    else:
        return redirect(url_for('index'))
    
    # return render_template("contact.html")



##ini boleh langsung bawak ke about melalui tekan button about 
@app.route("/redirect-about")
def kite_redirect_about():
    return redirect(url_for('about'))

@app.route("/redirect-contact")
def kite_redirect_contact():
    return redirect(url_for('contact'))

# @app.route("/halaman/<int:nilai>")
# def session_1(nilai): 
#     session["nilaiku"] = nilai
#     return "Sudah dapat mengesan nilainya"

# @app.route("/halaman/lihat")
# def view_session_1():
#     try:
#         data = session["nilaiku"]
#         return "Nilai yang diset adalah = {}".format(data)
#     except:
#         return "Anda tiada nilai session"

# #logout session
# @app.route("/halaman/logout")
# def logout_session_1():
#     session.pop("nilaiku")
#     return "Berjaya logout"

if __name__ == "__main__":
    app.run (debug=True, port=5005)
