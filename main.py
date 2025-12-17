# %%

import random
from flask import Flask, Response, jsonify, redirect, render_template, request, url_for
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
class Cafe(db.Model):
    __tablename__ = 'cafes'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    has_sockets: Mapped[bool] = mapped_column(nullable=False)
    has_toilet: Mapped[bool] = mapped_column(nullable=False)
    has_wifi: Mapped[bool] = mapped_column(nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=True)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def to_dict(self):
        #Method 1. 
        dictionary = {}
        # Loop through each column in the data record
        for column in self.__table__.columns:
            #Create a new dictionary entry;
            # where the key is the name of the column
            # and the value is the value of the column
            dictionary[column.name] = getattr(self, column.name)
        return dictionary

        #Method 2. Altenatively use Dictionary Comprehension to do the same thing.
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
    
# Create WTForm
class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField("Cafe Location", validators=[DataRequired()])
    map_url = StringField("Google Maps URL", validators=[DataRequired(), URL()])
    img_url = StringField("Image URL", validators=[DataRequired(), URL()])
    seats = StringField("Number of Seats", validators=[DataRequired()])
    coffee_price = StringField("Coffee Price e.g. $3.50", validators=[DataRequired()])
    has_sockets = SelectField("Has Power Sockets", choices=[("True", "Yes"), ("False", "No")], validators=[DataRequired()])
    has_toilet = SelectField("Has Toilet", choices=[("True", "Yes"), ("False", "No")], validators=[DataRequired()])
    has_wifi = SelectField("Has WiFi", choices=[("True", "Yes"), ("False", "No")], validators=[DataRequired()])
    can_take_calls = SelectField("Can Take Calls", choices=[("True", "Yes"), ("False", "No")], validators=[DataRequired()])
    submit = SubmitField('Submit')

# Initialize database and create tables
with app.app_context():
    if exists := db.inspect(db.engine).has_table('cafes'):
        print("Table 'cafes' already exists.")
    else:
        print("Creating table 'cafes'...")
        db.create_all()



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
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            seats=form.seats.data,
            coffee_price=form.coffee_price.data,
            has_sockets=form.has_sockets.data == "True",
            has_toilet=form.has_toilet.data == "True",
            has_wifi=form.has_wifi.data == "True",
            can_take_calls=form.can_take_calls.data == "True",
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("cafes"))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    all_cafes = db.session.execute(db.select(Cafe).order_by(Cafe.name)).scalars().all()
    return render_template('cafes.html', cafes=all_cafes)

@app.route('/random')
def random_cafe() -> Response | tuple[Response, int]:
    all_cafes = db.session.execute(db.select(Cafe)).scalars().all()
    
    if all_cafes:
        # method 1: using to_dict() method
        random_cafe = random.choice(all_cafes)
        #Simply convert the random_cafe data record to a dictionary of key-value pairs. 
        return jsonify(cafe=random_cafe.to_dict())
    else:
        return jsonify(error="No cafes found")

@app.route("/search")
def get_cafe_at_location():
    query_location = request.args.get("loc")
    result = db.session.execute(db.select(Cafe).where(Cafe.location == query_location))
    # Note, this may get more than one cafe per location
    all_cafes = result.scalars().all()
    if all_cafes:
        return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."}), 404

if __name__ == '__main__':
    app.run(debug=True)
