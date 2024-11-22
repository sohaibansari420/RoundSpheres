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
def users_registration():
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
# Fetching All Scientific Data
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

# --RETRIEVING ANALYTIC DATA--
# Fetching Predictive analytics Data
@app.get("/api/analytics/predictive")
def get_analytic_data():
 response = [{
  "status": "success",
  "predictions": [
    {
      "region": "Reservoir A",
      "evaporationRate": 2.5,
      "trend": "Decreasing"
    },
    {
      "region": "Reservoir B",
      "evaporationRate": 3.1,
      "trend": "Stable"
    }
  ]
}
]
 return jsonify (response)

# Upload New Scientific Data 
@app.post("/api/add-data")
def create_data():
 data = request.get_json() # access data from POST request
 print(json.dumps(data,indent=4))
 return jsonify(data)

# Update Specific Scientific Data elements like tempature only
@app.patch("/api/update-data")
def update_data_field():
 data = request.get_json() # access data from POST request
 print(json.dumps(data,indent=4))
 return jsonify(data)

# Update Scientific Data
@app.put("/api/update-data")
def update_data():
 data = request.get_json() # access data from POST request
 print(json.dumps(data,indent=4))
 return jsonify(data)

# Upload Bulk Scientific Data
@app.post("/api/add-data/bulk")
def create_data_bulk():
 data = request.get_json() # access data from POST request
 print(json.dumps(data,indent=4))
 return jsonify(data)


# --ADMINISTRATIVE ACTION--
# Add new Product
@app.post("/api/add-product")
def create_product():
 data = request.get_json() # access data from POST request
 print(json.dumps(data,indent=4))
 return jsonify(data)

# Update Product Data
@app.put("/api/update-product")
def update_product():
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


# --USER ACCOUNT MANAGEMENT--
# Retrieve Data of a specific User
@app.get("/api/get-user-profile")
def get_user_profile():
 response = [{
  "status": "success",
  "data": [
    {
      "dataId": 1,
      "date": "2024-01-01",
      "firstName": "Prime",
      "lastName": "Senpai",
      "email": "gojo@gmail.com",
      "profilePic": "",
      "Role": "Admin",
    }
  ]
}
]
 return jsonify (response)

# Allow User update profile information
@app.patch("/api/update-user-profile")
def update_user_profile():
 data = request.get_json() # access data from POST request
 print(json.dumps(data,indent=4))
 return jsonify(data)

# Delete user account---only admin has this permission
@app.delete('/api/delete-user-profile')
def delete_user_profile():
 json_data = request.delete_json() # req.delete_json() used to access json data
 print(json_data) # used for debugging purposes
 user_id = json_data['user_id']
 User.query.filter_by(user_id=user_id).delete()
 return {"User deleted with JSON" : f"user_id: {user_id}"}


# Port
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

# Add new order
@app.post("/api/add-orders")
def create_order():
 data = request.get_json() # access data from POST request
 print(json.dumps(data,indent=4))
 return jsonify(data)

# get order
@app.get("/api/orders")
def get_orders():
 response = [{
  "status": "success",
  "predictions": [
    {
      "id": "1",
      "quantity": 2.5
    }
  ]
}
]
 return jsonify (response)
