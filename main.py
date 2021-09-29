import random

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


@app.route("/")
def home():
    return render_template("index.html")


## HTTP GET - Read Record

@app.route("/random")
def get_random_cafe():
    cafes = db.session.query(Cafe).all()
    random_cafe = random.choice(cafes)
    return jsonify(cafe=random_cafe.to_dict())


@app.route("/all")
def all():
    all_cafes = db.session.query(Cafe).all()
    return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])


@app.route("/search")
def search():
    query_location = request.args.get('loc')
    all_cafe = db.session.query(Cafe).filter_by(location=query_location).all()
    if all_cafe:
        return jsonify(cafe=[cafe.to_dict() for cafe in all_cafe])
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."})


@app.route("/add", methods=["GET", "POST"])
def add_new_cafe():
    if request.method == "POST":
        new_cafe = Cafe(name=request.form["name"],
                        map_url=request.form['map_url'],
                        img_url=request.form['img_url'],
                        location=request.form['location'],
                        seats=request.form['seats'],
                        has_toilet=bool(request.form['has_toilet']),
                        has_wifi=bool(request.form['has_wifi']),
                        has_sockets=bool(request.form['has_sockets']),
                        can_take_calls=bool(request.form['can_take_calls']),
                        coffee_price=request.form['coffee_price'],
                        )
        db.session.add(new_cafe)
        db.session.commit()
        return jsonify(response={"success": "Successfully added the new cafe."})



@app.route("/update_price/<int:id>", methods=["PATCH"])
def update_price(id):
    cafe_to_update = Cafe.query.get(id)
    cafe_to_update.coffee_price = request.args.get("price")
    db.session.commit()
    return jsonify(response={"success": "Success update the price"})



@app.route("/report-closed/<int:id>", methods=["DELETE"])
def delete_cafe(id):
    api_key = "api_key"
    if api_key == request.args.get("api_key"):
        cafe_to_delete = Cafe.query.get(id)
        db.session.delete(cafe_to_delete)
        db.session.commit()
        return jsonify(response={"success": "Successful delete the cafe"})
    else:
        return jsonify(response={"403": "Invalid api key"})
if __name__ == '__main__':
    app.run(debug=True)
