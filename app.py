from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game.db'
db = SQLAlchemy(app)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    money = db.Column(db.Float, default=1000)
    daily_income = db.Column(db.Float, default=100)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)
    assets = db.Column(db.Integer, default=0)
    companies = db.Column(db.Integer, default=0)

@app.route('/')
def index():
    player = Player.query.first()
    if not player:
        player = Player()
        db.session.add(player)
        db.session.commit()
    
    current_time = datetime.utcnow()
    time_diff = current_time - player.last_login
    days_passed = time_diff.days
    
    if days_passed > 0:
        player.money += player.daily_income * days_passed
        player.last_login = current_time
        db.session.commit()
    
    return render_template('index.html', player=player)

@app.route('/buy_asset')
def buy_asset():
    player = Player.query.first()
    if player.money >= 500:
        player.money -= 500
        player.assets += 1
        player.daily_income += 10
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/create_company')
def create_company():
    player = Player.query.first()
    if player.money >= 2000:
        player.money -= 2000
        player.companies += 1
        player.daily_income += 50
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)