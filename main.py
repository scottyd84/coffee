# %%

import random
from typing import Literal
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
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            has_sockets=form.has_sockets.data == "True",
            has_toilet=form.has_toilet.data == "True",
            has_wifi=form.has_wifi.data == "True",
            can_take_calls=form.can_take_calls.data == "True",
            seats=form.seats.data,
            coffee_price=form.coffee_price.data,
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("cafes"))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes() -> str:
    all_cafes = db.session.execute(db.select(Cafe).order_by(Cafe.name)).scalars().all()
    return render_template('cafes.html', cafes=all_cafes)

@app.route("/all")
def get_all_cafes() -> Response:
    result = db.session.execute(db.select(Cafe).order_by(Cafe.name))
    all_cafes = result.scalars().all()
    #This uses a List Comprehension but you could also split it into 3 lines.
    return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])

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
    all_cafes: random.Sequence[random.Any] = result.scalars().all()
    if all_cafes:
        return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."}), 404

@app.route("/api/v1/cafes/add" , methods=["POST"])
def post_new_cafe() -> tuple[Response, Literal[400]] | tuple[Response, Literal[201]] | tuple[Response, Literal[500]]:
    # Handle both JSON and form data
    if request.is_json:
        # Handle JSON request
        data = request.get_json()
        new_cafe = Cafe(
            name=data.get('name'),
            map_url=data.get('map_url'),
            img_url=data.get('img_url'),
            location=data.get('location'),
            has_sockets=data.get('has_sockets'),
            has_toilet=data.get('has_toilet'),
            has_wifi=data.get('has_wifi'),
            can_take_calls=data.get('can_take_calls'),
            seats=data.get('seats'),
            coffee_price=data.get('coffee_price'),
        )
    else:
        # Handle form data request
        new_cafe = Cafe(
            name=request.form.get('name'),
            map_url=request.form.get('map_url'),
            img_url=request.form.get('img_url'),
            location=request.form.get('location'),
            has_sockets=request.form.get('has_sockets'),
            has_toilet=request.form.get('has_toilet'),
            has_wifi=request.form.get('has_wifi'),
            can_take_calls=request.form.get('can_take_calls'),
            seats=request.form.get('seats'),
            coffee_price=request.form.get('coffee_price'),
        )
    
    # Validate required fields
    if not new_cafe.name or not new_cafe.location:
        return jsonify(error="Missing required fields: name and location are required"), 400
    
    try:
        db.session.add(new_cafe)
        db.session.commit()
        return jsonify(response={"success": "Successfully added the new cafe."}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify(error=f"Failed to add cafe: {str(e)}"), 500


@app.route("/api/v1/cafes/<int:cafe_id>", methods=["GET"])
def get_cafe_by_id(cafe_id) -> Response | tuple[Response, Literal[404]]:
    """Get a specific cafe by ID"""
    cafe: Cafe | None = db.session.get(Cafe, cafe_id)
    if cafe:
        return jsonify(cafe=cafe.to_dict())
    else:
        return jsonify(error={"Not Found": "Sorry, a cafe with that id was not found in the database."}), 404



# Updating the price of a cafe based on a particular id:
# http://127.0.0.1:5000/api/v1/cafes/update-price/CAFE_ID?new_price=£5.67
@app.route("/api/v1/cafes/update-price/<int:cafe_id>", methods=["PATCH"])
def patch_new_price(cafe_id) -> tuple[Response, Literal[200]] | tuple[Response, Literal[404]]:
    new_price: str | None = request.args.get("new_price")
    cafe: Cafe | None = db.session.get(entity=Cafe, ident=cafe_id)  # Returns None if cafe_id is not found
    if cafe:
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the price."}), 200
    else:
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404

@app.route("/api/v1/cafes/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id) -> tuple[Response, Literal[403]] | tuple[Response, Literal[404]] | Response | tuple[Response, Literal[500]]:
    """Delete a cafe"""
    api_key: str | None = request.args.get("api-key")
    if api_key != "TopSecretAPIKey":
        return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403
    
    cafe: Cafe | None = db.session.get(Cafe, cafe_id)
    if not cafe:
        return jsonify(error={"Not Found": "Sorry, a cafe with that id was not found in the database."}), 404
    
    try:
        db.session.delete(cafe)
        db.session.commit()
        return jsonify(response={"success": "Successfully deleted the cafe from the database."})
    except Exception as e:
        db.session.rollback()
        return jsonify(error=f"Failed to delete cafe: {str(e)}"), 500


if __name__ == '__main__':
    app.run(debug=True)
