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
from sqlalchemy.sql import func
from flask_swagger_ui import get_swaggerui_blueprint


app = Flask(__name__)

# SQLAlchemy configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///roundspheres.db' # path to db
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
    # user_id       = db.Column(db.String(80), primary_key=True)
    __tablename__ = 'User_data'
    profileId   = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(80), nullable=False)
    lastname  = db.Column(db.String(80), nullable=False)
    email    = db.Column(db.String(80), nullable=False)
    role     = db.Column(db.String(80), nullable=False)
    created_at    = db.Column(db.DateTime(timezone=True), server_default=func.now())
 
    def __repr__(self):
        return '<User %r>' % self.profileId
      
# APIData
class Apidata(db.Model):
    """Definition of the User Model used by SQLAlchemy"""
    __tablename__ = 'IoT_data'
    dataId       = db.Column(db.Integer, primary_key=True, autoincrement=True)
    temperatureWater = db.Column(db.String(80), nullable=False)
    temperatureAir  = db.Column(db.String(80), nullable=False)
    humidity    = db.Column(db.String(80), nullable=False)
    windSpeed     = db.Column(db.String(80), nullable=False)
    precipitation     = db.Column(db.String(80), nullable=False)
    notes     = db.Column(db.String(200), nullable=False)
    created_at    = db.Column(db.DateTime(timezone=True), server_default=func.now())
 
    def __repr__(self):
        return '<Apidata %r>' % self.dataId

# AnalyticData
class Analytic(db.Model):
    """Definition of the User Model used by SQLAlchemy"""
    __tablename__ = 'Analytic_data'
    # user_id       = db.Column(db.String(80), primary_key=True)
    analyticId       = db.Column(db.Integer, primary_key=True, autoincrement=True)
    region = db.Column(db.String(80), nullable=False)
    evaporationRate  = db.Column(db.Float, nullable=True)
    trend    = db.Column(db.String(80), nullable=False)
    created_at    = db.Column(db.DateTime(timezone=True), server_default=func.now())
 
    def __repr__(self):
        return '<Analyticdata %r>' % self.analyticId
      
# Product 
class Product(db.Model):
    """Definition of the User Model used by SQLAlchemy"""
    __tablename__ = 'Product_data'
    productId       = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    description  = db.Column(db.String(200), nullable=False)
    price    = db.Column(db.Float, nullable=True)
    stock     = db.Column(db.Integer, nullable=True)
    created_at    = db.Column(db.DateTime(timezone=True), server_default=func.now())
 
    def __repr__(self):
        return '<Product %r>' % self.productId
#------------------------------------------------------------------------------
# class def for Marshmallow serialization
class UserSchema(ma.SQLAlchemyAutoSchema):
 """Definition used by serialization library based on User Model"""
 class Meta:
    fields = ("profileId","firstname","lastname", "email", "role")

class ApiDataSchema(ma.SQLAlchemyAutoSchema):
 """Definition used by serialization library based on API Data Model"""
 class Meta:
    fields = ("dataId","temperatureWater","temperatureAir", "humidity", "windSpeed", "precipitation", "notes")    
    
class AnalyticDataSchema(ma.SQLAlchemyAutoSchema):
 """Definition used by serialization library based on Analytic Data Model"""
 class Meta:
    fields = ("analyticId","region","evaporationRate", "trend")     
    
class ProductSchema(ma.SQLAlchemyAutoSchema):
 """Definition used by serialization library based on User Model"""
 class Meta:
    fields = ("productId","name","description", "price", "stock")    
    
# instantiate objs based on Marshmallow schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)
apidata_schema = ApiDataSchema()
apidatas_schema = ApiDataSchema(many=True)
analytic_schema = AnalyticDataSchema()
analytics_schema = AnalyticDataSchema(many=True)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
#------------------------------------------------------------------------------
# Configure Swagger UI
# SWAGGER_URL = '/swagger1'
# API_URL = '/swagger1.json'
SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Sample API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
#------------------------------------------------------------------------------

@app.route("/")
def home():
    return render_template("index.html")
  
@app.route("/shop")
def shop():
    return render_template("shop.html")

# HTTP Methods and Endpoints

# --USER MANAGEMENT--
#------------------------------------------------------------------------------
# --AUTHENTICATION--
# User Registration
@app.post("/auth/register")
def users_registration():
 """endpoint uses json to register user details to db"""
 json_data = request.get_json() # req.get_json() used to access json sent
 print(json_data) # used for debugging purposes
 newUser = User (
 profileId = json_data['profileId'],
 firstname = json_data['firstname'],
 lastname = json_data['lastname'],
 email = json_data['email'],
 role = json_data['role']
 )
 db.session.add(newUser)
 db.session.commit()
 print ("New  added:")
 print (json.dumps(json_data, indent=4)) # used for debugging purposes
 return user_schema.jsonify(newUser)

# User Login
@app.post("/auth/login")
def users_login():
 data = request.get_json() # access data from POST request
 print(json.dumps(data,indent=4))
 return jsonify(data)

#------------------------------------------------------------------------------
# --RETRIEVING SCIENTIFIC DATA--
# Fetching All Scientific Data
@app.get("/api/get-all-data")
def get_all_data():
 apidata = Apidata.query.all()
 return apidatas_schema.jsonify(apidata)

# Fetching specific Scientific Data
@app.get("/api/get-products/<dataId>")
def get_data(dataId):
 apidata = Product.query.filter_by(dataId=dataId).first()
 return apidata_schema.jsonify(apidata)

# Upload New Scientific Data 
@app.post("/api/add-data")
def create_data():
 json_data = request.get_json() # req.get_json() used to access json sent
 print(json_data) # used for debugging purposes
 newApiData = Apidata (
 dataId = json_data['dataId'],
 temperatureWater = json_data['temperatureWater'],
 temperatureAir = json_data['temperatureAir'],
 humidity = json_data['humidity'],
 windSpeed = json_data['windSpeed'],
 precipitation = json_data['precipitation'],
 notes = json_data['notes'],
 )
 db.session.add(newApiData)
 db.session.commit()
 print ("New API Data added:")
 print (json.dumps(json_data, indent=4)) # used for debugging purposes
 return apidata_schema.jsonify(newApiData)

# Update Specific Scientific Data elements like tempature only
@app.patch("/api/update-data")
def update_data_field():
 data = request.get_json() # access data from POST request
 print(json.dumps(data,indent=4))
 return jsonify(data)

# Update Scientific Data
@app.put("/api/update-data/<dataId>")
def update_data():
 data = request.get_json() # access data from POST request
 print(json.dumps(data,indent=4))
 return jsonify(data)

# Upload Bulk Scientific Data
# @app.post("/api/add-data/bulk")
# def create_data_bulk():
#  json_data = request.get_json() # req.get_json() used to access json sent
#  print(json_data) # used for debugging purposes
#  newBulkApiData = Apidatabulk (
#  dataId = json_data['dataId'],
#  temperatureWater = json_data['temperatureWater'],
#  temperatureAir = json_data['temperatureAir'],
#  humidity = json_data['humidity'],
#  windSpeed = json_data['windSpeed'],
#  precipitation = json_data['precipitation'],
#  notes = json_data['notes'],
#  )
#  db.session.add(newBulkApiData)
#  db.session.commit()
#  print ("New API Data added:")
#  print (json.dumps(json_data, indent=4)) # used for debugging purposes
#  return apidata_schema.jsonify(newBulkApiData)

#------------------------------------------------------------------------------
# --RETRIEVING ANALYTIC DATA--
# Fetching Predictive analytics Data
@app.get("/api/analytics/predictive")
def get_analytic_data():
 analytics = Analytic.query.all()
 return analytics_schema.jsonify(analytics)

@app.post("/api/analytics")
def add_analytic_data():
 json_data = request.get_json() # req.get_json() used to access json sent
 print(json_data) # used for debugging purposes
 newAnalytic = Analytic (
 analyticId = json_data['analyticId'],
 region = json_data['region'],
 evaporationRate = json_data['evaporationRate'],
 trend = json_data['trend']
 )
 db.session.add(newAnalytic)
 db.session.commit()
 print ("New Product added:")
 print (json.dumps(json_data, indent=4)) # used for debugging purposes
 return analytic_schema.jsonify(newAnalytic)

#------------------------------------------------------------------------------
# --ADMINISTRATIVE ACTION--
# Get Products
@app.get("/api/get-all-products")
def get_all_product_data():
 products = Product.query.all()
 return products_schema.jsonify(products)

# Get Specific Products
@app.get("/api/get-products/<productId>")
def get_product_data(productId):
 product = Product.query.filter_by(productId=productId).first()
 return product_schema.jsonify(product)

# Add new Product
@app.post("/api/add-product")
def create_product():
 json_data = request.get_json() # req.get_json() used to access json sent
 print(json_data) # used for debugging purposes
 newProduct = Product (
 productId = json_data['productId'],
 name = json_data['name'],
 description = json_data['description'],
 price = json_data['price'],
 stock = json_data['stock']
 )
 db.session.add(newProduct)
 db.session.commit()
 print ("New Product added:")
 print (json.dumps(json_data, indent=4)) # used for debugging purposes
 return product_schema.jsonify(newProduct)

# Update Product Data
@app.put("/api/update-product/<productId>")
def update_product():
 data = request.get_json() # access data from POST request
 print(json.dumps(data,indent=4))
 return jsonify(data)

@app.delete('/api/delete-product/<productId>')
def delete_product(productId):
 User.query.filter_by(productId=productId).delete()
 db.session.commit()
 return {"Product deleted with route params" : f"productId: {productId}"}

#------------------------------------------------------------------------------
# --USER ACCOUNT MANAGEMENT--

# Retrieve Data of all User
@app.get("/api/get-user-profile")
def get_all_user_profile():
 """endpoint uses route parameters to determine user to be queried from db"""
 users = User.query.all()
 return users_schema.jsonify(users)

# Retrieve Data of a specific User
@app.get("/api/get-user-profile/<profileId>")
def get_user_profile(profileId):
 """endpoint uses route parameters to determine user to be queried from db"""
 user = User.query.filter_by(profileId=profileId).first()
 return user_schema.jsonify(user)

# Allow User update profile information
@app.patch("/api/update-user-profile/<profileId>")
def update_user_profile(profileId):
 data = request.get_json() # access data from POST request
 print(json.dumps(data,indent=4))
 return jsonify(data)

# Delete user account---only admin has this permission
@app.delete('/api/delete-user-profile/<profileId>')
def delete_user_profile(profileId):
 User.query.filter_by(profileId=profileId).delete()
 db.session.commit()
 return {"User deleted with route params" : f"profiled: {profileId}"}


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
