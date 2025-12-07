# %%

import csv
import random
from flask import Flask, jsonify, render_template
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column 
from sqlalchemy import Integer, String

# Initialize Flask app and configurations
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

# Initialize Bootstrap
Bootstrap5(app)

# Create Table base class
class Base(DeclarativeBase):
    pass

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(model_class=Base)
db.init_app(app)

# CREATE TABLE
class Cafe(Base):
    __tablename__ = 'cafes'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    open: Mapped[str] = mapped_column(String(250), nullable=False)
    close: Mapped[str] = mapped_column(String(250), nullable=False)
    coffee_rating: Mapped[str] = mapped_column(String(250), nullable=False)
    wifi_rating: Mapped[str] = mapped_column(String(250), nullable=False)
    power_rating: Mapped[str] = mapped_column(String(250), nullable=False)

# Create WTForm
class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField("Cafe Location on Google Maps (URL)", validators=[DataRequired(), URL()])
    open = StringField("Opening Time e.g. 8AM", validators=[DataRequired()])
    close = StringField("Closing Time e.g. 5:30PM", validators=[DataRequired()])
    coffee_rating = SelectField("Coffee Rating", choices=["☕️", "☕☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕"], validators=[DataRequired()])
    wifi_rating = SelectField("Wifi Strength Rating", choices=["✘", "💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"], validators=[DataRequired()])
    power_rating = SelectField("Power Socket Availability", choices=["✘", "🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"], validators=[DataRequired()])
    submit = SubmitField('Submit')

# Initialize database and create tables
with app.app_context():
    db.create_all()
    
    # Check if database is empty before populating
    if db.session.execute(db.select(Cafe)).first() is None:
        # populate the database with cafes from CSV
        with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
            csv_data = csv.reader(csv_file, delimiter=',')
            next(csv_data)  # Skip header row
            for row in csv_data:
                new_cafe = Cafe(
                    name=row[0],
                    location=row[1],
                    open=row[2],
                    close=row[3],
                    coffee_rating=row[4],
                    wifi_rating=row[5],
                    power_rating=row[6]
                )
                db.session.add(new_cafe)
            db.session.commit()

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below

# %%

@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe(
            name=form.cafe.data,
            location=form.location.data,
            open=form.open.data,
            close=form.close.data,
            coffee_rating=form.coffee_rating.data,
            wifi_rating=form.wifi_rating.data,
            power_rating=form.power_rating.data
        )
        db.session.add(new_cafe)
        db.session.commit()
        return render_template('cafes.html')
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    all_cafes = db.session.execute(db.select(Cafe).order_by(Cafe.name)).scalars().all()
    return render_template('cafes.html', cafes=all_cafes)

@app.route('/random')
def random_cafe():
    all_cafes = db.session.execute(db.select(Cafe)).scalars().all()
    if all_cafes:
        cafe = random.choice(all_cafes)
        return jsonify(cafe={
            "name": cafe.name,
            "location": cafe.location,
            "open": cafe.open,
            "close": cafe.close,
            "coffee_rating": cafe.coffee_rating,
            "wifi_rating": cafe.wifi_rating,
            "power_rating": cafe.power_rating
        })
    return jsonify(error="No cafes found"), 404

if __name__ == '__main__':
    app.run(debug=True)
