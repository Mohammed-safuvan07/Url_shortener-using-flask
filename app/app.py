import os
from flask import Flask,render_template,request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from pyshorteners import Shortener

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))   ###abspath means whole directory from c:...
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')  ##were creating a database for this app
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Shrotner(db.Model):
    __tablename__= 'url_short_data'
    id = db.Column(db.Integer,primary_key = True)
    long_url = db.Column(db.Text)
    short_url = db.Column(db.Text)
    
    def __init__(self,long_url,short_url):
        self.long_url=long_url
        self.short_url=short_url
    


def ShortenUrl(long_url):
    url=long_url
    st = Shortener()
    return st.tinyurl.short(url)


@app.route("/",methods = ["POST","GET"])
def index():
    if request.method == 'POST':
        long_url = request.form['in_1']
        short_url = ShortenUrl(long_url)
        obj = Shrotner(long_url, short_url)
        db.session.add(obj)
        db.session.commit()
        return render_template("result.html",Srl=short_url)
    return render_template("index.html")

@app.route('/result')
def result():
    return render_template("result.html")
@app.route("/display")
def display():
    values = Shrotner.query.all()
    return render_template('display.html', values = values)


if __name__ =="__main__":
    app.run(debug=True)