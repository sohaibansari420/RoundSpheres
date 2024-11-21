"""
Name: RoundSphere
Date: 20241119
Purpose: Basic Flask Server for RoundSphere Website
"""

from flask import Flask,request,render_template,jsonify
import json
# SQLAlchemy is an Object Relational Mapper allowing decoupling of db operations
from flask_sqlalchemy import SQLAlchemy
# Marshmallow is an object serialization/deserialization library
from flask_marshmallow import Marshmallow

app = Flask(__name__)

# SQLAlchemy configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db' # path to db
app.config['SQLALCHEMY_ECHO'] = True # echoes SQL for debug
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#------------------------------------------------------------------------------
# instantiate db obj using the SQLAlchemy class with the Flask app obj as arg
db = SQLAlchemy(app)
#------------------------------------------------------------------------------
# Marshmallow must be initialised after SQLAlchemy
ma = Marshmallow(app)
#------------------------------------------------------------------------------
# class def for SQLAlchemy ORM
class User(db.Model):
    """Definition of the User Model used by SQLAlchemy"""
    user_id       = db.Column(db.String(80), primary_key=True)
    user_forename = db.Column(db.String(80), nullable=False)
    user_surname  = db.Column(db.String(80), nullable=False)
    user_email    = db.Column(db.String(80), nullable=False)
 
    def __repr__(self):
        return '<User %r>' % self.user_id
#------------------------------------------------------------------------------
# class def for Marshmallow serialization
class UserSchema(ma.SQLAlchemyAutoSchema):
 """Definition used by serialization library based on User Model"""
 class Meta:
    fields = ("user_id","user_forename","user_surname", "user_email")
# instantiate objs based on Marshmallow schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)
#------------------------------------------------------------------------------

@app.route("/")
def home():
    return render_template("index.html")


# HTTP Methods and Endpoints

# --USER MANAGEMENT--
#------------------------------------------------------------------------------
# --AUTHENTICATION--
# User Registration
@app.post("/auth/register")
def users_regisgtration():
 data = request.get_json() # access data from POST request
 print(json.dumps(data,indent=4))
 return jsonify(data)

# User Login
@app.post("/auth/login")
def users_login():
 data = request.get_json() # access data from POST request
 print(json.dumps(data,indent=4))
 return jsonify(data)

# --RETRIEVING SCIENTIFIC DATA--
# Fetching Data
@app.get("/api/get-all-data")
def get_all_data():
 response = [{
  "status": "success",
  "data": [
    {
      "dataId": 1,
      "date": "2024-01-01",
      "temperatureWater": 15.2,
      "temperatureAir": 18.5,
      "humidity": 60,
      "windSpeed": 12.4,
      "precipitation": 0.0,
      "notes": "Clear day"
    },
    {
      "dataId": 2,
      "date": "2024-01-02",
      "temperatureWater": 15.8,
      "temperatureAir": 20.0,
      "humidity": 65,
      "windSpeed": 8.9,
      "precipitation": 0.2,
      "notes": "Light drizzle"
    }
  ]
}
]
 return jsonify (response)

# Upload Data
@app.post("/api/add-data")
def create_data():
 data = request.get_json() # access data from POST request
 print(json.dumps(data,indent=4))
 return jsonify(data)

# Upload Data
@app.put("/api/upload-data")
def update_data():
 data = request.get_json() # access data from POST request
 print(json.dumps(data,indent=4))
 return jsonify(data)

# Upload Bulk Data
@app.post("/api/add-data/bulk")
def create_data_bulk():
 data = request.get_json() # access data from POST request
 print(json.dumps(data,indent=4))
 return jsonify(data)


# --ADMINISTRATIVE ACTION--
# Add Product
@app.post("/api/add-product")
def create_product():
 data = request.get_json() # access data from POST request
 print(json.dumps(data,indent=4))
 return jsonify(data)


@app.delete('/api/delete-product')
def delete_product():
 json_data = request.delete_json() # req.delete_json() used to access json data
 print(json_data) # used for debugging purposes
 user_id = json_data['user_id']
 User.query.filter_by(user_id=user_id).delete()
 return {"User deleted with JSON" : f"user_id: {user_id}"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)