"""
Name: RoundSphere
Date: 20241119
Purpose: Basic Flask Server for RoundSphere Website
"""

from flask import Flask,request,render_template,jsonify
import json
"""SQLAlchemy is an Object Relational Mapper allowing decoupling of db operations"""
from flask_sqlalchemy import SQLAlchemy
"""Marshmallow is an object serialization/deserialization library"""
from flask_marshmallow import Marshmallow
from sqlalchemy.sql import func
from flask_swagger_ui import get_swaggerui_blueprint
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'django-insecure-9i8xk#_3t5v^(uem232=$-xo_v0#ymj=l#seg-#5ang)%98a*f'

jwt = JWTManager(app)

"""SQLAlchemy configuration"""
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///roundspheres.db' # path to db
app.config['SQLALCHEMY_ECHO'] = True # echoes SQL for debug
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

"""--------------------------------------------------------------------------------------------------"""
"""instantiate db obj using the SQLAlchemy class with the Flask app obj as arg"""
db = SQLAlchemy(app)

"""--------------------------------------------------------------------------------------------------"""
"""Marshmallow must be initialised after SQLAlchemy"""
ma = Marshmallow(app)

"""--------------------------------------------------------------------------------------------------"""
"""class def for SQLAlchemy ORM"""
class User(db.Model):
    """Definition of the User Model used by SQLAlchemy"""
    # user_id       = db.Column(db.String(80), primary_key=True)
    __tablename__ = 'User_data'
    profileId   = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(80), nullable=False)
    lastname  = db.Column(db.String(80), nullable=False)
    email    = db.Column(db.String(80), nullable=False)
    role     = db.Column(db.String(80), nullable=False)
    password = db.Column(db.Text())
    created_at    = db.Column(db.DateTime(timezone=True), server_default=func.now())
 
    def __repr__(self):
        return '<User %r>' % self.profileId
    
    def set_password(self,password):
        self.password = generate_password_hash(password)
        
    def check_password(self,password):
        return check_password_hash(self.password,password)
    
    def to_dict(self):
        return {
            "profileId": self.profileId,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at.isoformat()
        }
      
"""APIData"""
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

"""AnalyticData"""
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
      
"""Product"""
class Product(db.Model):
    """Definition of the Product Model used by SQLAlchemy"""
    __tablename__ = 'Product_data'
    productId       = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    description  = db.Column(db.String(200), nullable=False)
    price    = db.Column(db.Float, nullable=True)
    stock     = db.Column(db.Integer, nullable=True)
    created_at    = db.Column(db.DateTime(timezone=True), server_default=func.now())
 
    def __repr__(self):
        return '<Product %r>' % self.productId, self.name, self.price, self.stock
    
    # def __repr__(self):
    #     return f"<Product(id={self.productId}, name={self.name}, price={self.price}, stock={self.stock})>"

    def to_dict(self):
        return {
            "productId": self.productId,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "stock": self.stock,
            "created_at": self.created_at.isoformat()
        }

"""Order""" 
class Order(db.Model):
    """Definition of the Order Model used by SQLAlchemy"""
    __tablename__ = 'Order_data'
    orderId       = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userId       = db.Column(db.Integer, autoincrement=True)
    productId       = db.Column(db.Integer, autoincrement=True)
    orderItemId       = db.Column(db.Integer, autoincrement=True)
    status = db.Column(db.String(80), nullable=False)
    pricePerUnit    = db.Column(db.Float, nullable=True)
    totalAmout    = db.Column(db.Float, nullable=True)
    quantity     = db.Column(db.Integer, nullable=True)
    orderDate   = db.Column(db.DateTime(timezone=True), server_default=func.now())
 
    def __repr__(self):
        return '<Order %r>' % self.orderId

"""--------------------------------------------------------------------------------------------------"""
"""class def for Marshmallow serialization"""
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
 """Definition used by serialization library based on Product Model"""
 class Meta:
    fields = ("productId","name","description", "price", "stock")  
    
class OrderSchema(ma.SQLAlchemyAutoSchema):
 """Definition used by serialization library based on Order Model"""
 class Meta:
    fields = ("orderId","userId","productId","orderItemId","quantity","totalAmount", "status", "orderDate","pricePerUnit",)    
    
"""instantiate objs based on Marshmallow schemas"""
user_schema = UserSchema()
users_schema = UserSchema(many=True)
apidata_schema = ApiDataSchema()
apidatas_schema = ApiDataSchema(many=True)
analytic_schema = AnalyticDataSchema()
analytics_schema = AnalyticDataSchema(many=True)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

"""--------------------------------------------------------------------------------------------------"""
"""Configure Swagger UI"""
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

"""---------------------------------------------------------------------------------------------------"""

@app.route("/")
def home():
    return render_template("index.html")
  
@app.route("/shop")
def shop():
    return render_template("shop.html")

"""HTTP Methods and Endpoints"""

"""--USER MANAGEMENT--"""

"""--------------------------------------------------------------------------------------------------"""
"""--AUTHENTICATION--"""
"""User Registration"""
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

"""--------------------------------------------------------------------------------------------------"""
"""--RETRIEVING SCIENTIFIC DATA--"""
"""Fetching All Scientific Data"""
@app.get("/api/get-all-data")
@jwt_required()
def get_all_data():
 current_data = get_jwt_identity()
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

"""Update Specific Scientific Data elements like temperature only"""
@app.patch("/api/update-data")
def update_data_field():
 data = request.get_json() # access data from POST request
 print(json.dumps(data,indent=4))
 return jsonify(data)

"""Update Scientific Data"""
@app.put("/api/update-data/<dataId>")
def update_data():
 data = request.get_json() # access data from POST request
 print(json.dumps(data,indent=4))
 return jsonify(data)

"""Upload Bulk Scientific Data"""
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

"""--------------------------------------------------------------------------------------------------"""
"""--RETRIEVING ANALYTIC DATA--"""
"""Fetching Predictive analytics Data"""
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

"""--------------------------------------------------------------------------------------------------"""
"""--ADMINISTRATIVE ACTION--"""
"""Get Products"""
@app.get("/api/get-all-products")
def get_all_product_data():
 products = Product.query.all()
 return products_schema.jsonify(products), 200

"""Get Specific Products"""
@app.get("/api/get-products/<productId>")
def get_product_data(productId):
 product = Product.query.filter_by(productId=productId).first()
 return product_schema.jsonify(product), 200

"""Add new Product"""
@app.post("/api/add-product")
def create_product():
 data = request.get_json() # req.get_json() used to access json sent
 print(data) # used for debugging purposes
 newProduct = Product (
 productId = data['productId'],
 name = data['name'],
 description = data['description'],
 price = data['price'],
 stock = data['stock']
 )
 db.session.add(newProduct)
 db.session.commit()
 print ("New Product added:")
 print (json.dumps(data, indent=4)) # used for debugging purposes
 return product_schema.jsonify(newProduct), 200

# """Add Bulk Products"""
# @app.post("/api/ass-product/bulk")
# def add_bulk_product():
#  data = request.get_json()
#  print(data)
#  '''Validate the request body'''
#  if not isinstance(data, list):
#     return jsonify({"msg": "Invalid input. Expected a list of products."}), 400

#  products = []
#  for product_data in data:
#     '''Validate each product'''
#     if not all(key in product_data for key in ["productId", "name", "price", "stock"]):
#         return jsonify({"msg": "Missing required fields in one or more products."}), 400

#     '''Create a new product instance'''
#     new_product = Product(
#     productId = product_data['productId'],
#     name=product_data["name"],
#     description=product_data.get("description"),  # Optional field
#     price=product_data["price"],
#     stock=product_data["stock"]
#     )
#     products.append(new_product)
    
#  '''Add all products to the session and commit'''
#  try:
#     db.session.add_all(products)
#     db.session.commit()
#     return jsonify({
#             "msg": f"{len(products)} products created successfully.",
#             "products": [product.to_dict() for product in products]
#         }), 201
#  except Exception as e:
#     db.session.rollback()
#     return jsonify({"msg": "Failed to create products", "error": str(e)}), 500

 products = []
 errors = []
 for idx, product_data in enumerate(data):
        # Validate required fields
    if not all(key in product_data for key in ["name", "price", "stock"]):
     errors.append({"index": idx, "msg": "Missing required fields"})
     continue

    try:
     # Create a new product instance
     new_product = Product(
        name=product_data["name"],
        description=product_data.get("description"),
        price=product_data["price"],
        stock=product_data["stock"]
        )
     products.append(new_product)
    except Exception as e:
        errors.append({"index": idx, "msg": str(e)})

    # Add valid products to the session
    try:
        if products:
            db.session.add_all(products)
            db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Failed to create products", "error": str(e)}), 500

    return jsonify({
        "msg": f"{len(products)} products created successfully.",
        "products": [product.to_dict() for product in products],
        "errors": errors
    }), 200 if products else 400

'''Update Product Data'''
@app.put("/api/update-product/<productId>")
def update_product(productId):
 data = request.get_json() # access data from POST request

 """Replace a product with new details"""
 data = request.get_json()

 '''Fetch the product by ID'''
 product = Product.query.get(productId)
 if not product:
    return jsonify({"msg": "Product not found"}), 404

 """Replace all fields with new values""" 
 product.name = data.get('name')
 product.description = data.get('description')
 product.price = data.get('price')
 product.stock = data.get('stock')

 """Commit the changes"""
 try:
    db.session.commit()
    return jsonify({
            "msg": "Product replaced successfully",
            "product": product.to_dict()
    }), 200
 except Exception as e:
    db.session.rollback()
    return jsonify({"msg": "Failed to replace product", "error": str(e)}), 500

@app.patch("/api/update-product/<productId>")
def edit_product(productId):
 """Endpoint to update specific fields of a product"""
 data = request.get_json()

 '''Find the product by ID'''
 product = Product.query.get(productId)
 if not product:
    return jsonify({"msg": "Product not found"}), 404

 '''Update only the fields provided in the request'''
 if "name" in data:
    product.name = data["name"]
 if "description" in data:
    product.description = data["description"]
 if "price" in data:
    product.price = data["price"]
 if "stock" in data:
    product.stock = data["stock"]

 '''Commit changes to the database'''
 try:
        db.session.commit()
        return jsonify({
            "msg": "Product updated successfully",
            "product": product.to_dict()
        }), 200
 except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Failed to update product", "error": str(e)}), 500
 
'''Delete a product'''
@app.delete('/api/delete-product/<productId>')
def delete_product(productId):
 User.query.filter_by(productId=productId).delete()
 db.session.commit()
 return {"Product deleted with route params" : f"productId: {productId}"}

"""------------------------------------------------------------------------------"""
"""--USER ACCOUNT MANAGEMENT--"""

"""Retrieve Data of all User"""
@app.get("/api/get-user-profile")
def get_all_user_profile():
 """endpoint uses route parameters to determine user to be queried from db"""
 users = User.query.all()
 return users_schema.jsonify(users)

'''Retrieve Data of a specific User'''
@app.get("/api/get-user-profile/<profileId>")
def get_user_profile(profileId):
 """endpoint uses route parameters to determine user to be queried from db"""
 user = User.query.filter_by(profileId=profileId).first()
 return user_schema.jsonify(user)

'''Allow User update profile information'''
@app.patch("/api/update-user-profile/<profileId>")
def update_user_profile(profileId):
 data = request.get_json() # access data from POST request
 user = User.query.get(profileId)
 if not user:
        return jsonify({"msg": "User not found"}), 404

 if "firstname" in data:
    user.firstname = data["firstname"]
 if "lastname" in data:
    user.lastname = data["lastname"]
 if "email" in data:
    user.email = data["email"]
 if "role" in data:
    user.role = data["role"]

 try:
    db.session.commit()
    return jsonify({"msg": "User updated successfully", "user": user.to_dict()}), 200
 except Exception as e:
    db.session.rollback()
    return jsonify({"msg": "Failed to update user", "error": str(e)}), 500

'''Delete user account---only admin has this permission'''
@app.delete('/api/delete-user-profile/<profileId>')
def delete_user_profile(profileId):
 User.query.filter_by(profileId=profileId).delete()
 db.session.commit()
 return {"User deleted with route params" : f"profiled: {profileId}"}

'''--------------------------------------------------------------------------------------------------'''
'''--ORDER MANAGEMENT--'''
'''Add new order'''
@app.post("/api/add-orders")
def create_order():
 json_data = request.get_json() # req.get_json() used to access json sent
 print(json_data) # used for debugging purposes
 newOrder = Order (
 orderId = json_data['orderId'],
 userId = json_data['userId'],
 orderDate = json_data['orderDate'],
 totalAmount = json_data['totalAmount'],
 status = json_data['status']
 )
 db.session.add(newOrder)
 db.session.commit()
 print ("New Order added:")
 print (json.dumps(json_data, indent=4)) # used for debugging purposes
 return order_schema.jsonify(newOrder)

'''Add new order item'''
@app.post("/api/add-order-item")
def create_order_item():
 json_data = request.get_json() # req.get_json() used to access json sent
 print(json_data) # used for debugging purposes
 newOrderItem = Order (
 orderId = json_data['orderId'],
 userId = json_data['userId'],
 orderDate = json_data['orderDate'],
 totalAmount = json_data['totalAmount'],
 status = json_data['status']
 )
 db.session.add(newOrderItem)
 db.session.commit()
 print ("New Order added:")
 print (json.dumps(json_data, indent=4)) # used for debugging purposes
 return order_schema.jsonify(newOrderItem)

'''get order'''
@app.get("/api/orders")
def get_orders():
 orders = Order.query.all()
 return orders_schema.jsonify(orders)

'''Retrieve Data of a specific Order'''
@app.get("/api/orders/<orderId>")
def get_single_order(orderId):
 """endpoint uses route parameters to determine user to be queried from db"""
 order = Order.query.filter_by(orderId=orderId).first()
 return orders_schema.jsonify(order)

'''Allow Admin update profile information'''
@app.patch("/api/orders/<orderId>")
def update_order(profileId):
 data = request.get_json() # access data from POST request
 print(json.dumps(data,indent=4))
 return jsonify(data)

'''--------------------------------------------------------------------------------------------------'''
'''Port'''
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)  