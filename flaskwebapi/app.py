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
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from decouple import config
from flask_migrate import Migrate
from flask_jwt_extended.exceptions import NoAuthorizationError


app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = config("JWT_SECRET_KEY")
"""To confirm the Secret key is loaded"""
# print(f"JWT_SECRET_KEY: {app.config['JWT_SECRET_KEY']}")

jwt = JWTManager(app)

"""SQLAlchemy configuration"""
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///roundspheres.db' #path to db
app.config['SQLALCHEMY_ECHO'] = True # echoes SQL for debug
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

"""--------------------------------------------------------------------------------------------------"""
"""instantiate db obj using the SQLAlchemy class with the Flask app obj as arg"""
db = SQLAlchemy(app)

"""--------------------------------------------------------------------------------------------------"""
"""Marshmallow must be initialised after SQLAlchemy"""
ma = Marshmallow(app)

"""--------------------------------------------------------------------------------------------------"""

"""--------------------------------------------------------------------------------------------------"""
migrate = Migrate(app, db)

"""class def for SQLAlchemy ORM"""
class User(db.Model):
    """Definition of the User Model used by SQLAlchemy"""
    __tablename__ = 'User_data'
    profileId   = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(80), nullable=False)
    lastname  = db.Column(db.String(80), nullable=False)
    email    = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Hashed password
    role     = db.Column(db.String(80), nullable=False)  
    created_at    = db.Column(db.DateTime(timezone=True), server_default=func.now())
 
    def __repr__(self):
        return '<User %r>' % self.profileId
    
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
    
    def to_dict(self):
        return {
            "dataId": self.dataId,
            "temperatureWater": self.temperatureWater,
            "temperatureAir": self.temperatureAir,
            "humidity": self.humidity,
            "windSpeed": self.windSpeed,
            "precipitation": self.precipitation,
            "notes": self.notes,
            "created_at": self.created_at.isoformat()
        }

"""AnalyticData"""
class Analytic(db.Model):
    """Definition of the User Model used by SQLAlchemy"""
    __tablename__ = 'Analytic_data'
    analyticId       = db.Column(db.Integer, primary_key=True, autoincrement=True)
    region = db.Column(db.String(80), nullable=False)
    evaporationRate  = db.Column(db.Float, nullable=True)
    trend    = db.Column(db.String(80), nullable=False)
    created_at    = db.Column(db.DateTime(timezone=True), server_default=func.now())
 
    def __repr__(self):
        return '<Analyticdata %r>' % self.analyticId
    def to_dict(self):
        return {
            "analyticId": self.analyticId,
            "region": self.region,
            "evaporationRate": self.evaporationRate,
            "trend": self.trend,
            "created_at": self.created_at.isoformat()
        }
      
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
SWAGGER_URL = '/api/docs'   # URL for exposing Swagger UI (without trailing '/')
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

"""--ADMIN CHECK--"""
def admin_required():
 """Ensure the user has the admin role"""
 claims = get_jwt()
 if claims.get("role") != "admin":
    return jsonify({"msg": "Admin access required"}), 403

"""HTTP Methods and Endpoints"""

"""--USER MANAGEMENT--"""
"""--------------------------------------------------------------------------------------------------"""
"""--AUTHENTICATION--"""
"""User Registration"""
@app.post("/auth/register")
def register_user():
 """Register a new user"""
 json_data = request.get_json() # req.get_json() used to access json sent
 print(json_data) #used for debugging purposes

 """ Validate input """
 if not all(key in json_data for key in ("firstname", "lastname", "email", "password", "role")):
    return jsonify({"error": "Missing required fields"}), 400

 hashed_password = generate_password_hash(json_data["password"])  #Hash the password

 """Create a new user"""
 newUser = User (
 profileId = json_data['profileId'],
 firstname = json_data['firstname'],
 lastname = json_data['lastname'],
 email = json_data['email'],
 role = json_data['role'],
 password=hashed_password,
 )
 try:
    db.session.add(newUser)
    db.session.commit()
    print ("New  added:")
    print (json.dumps(json_data, indent=4)) # used for debugging purposes
    return user_schema.jsonify(newUser), 200
 except Exception as e:
    db.session.rollback()
    return jsonify({"error": "Failed to register user", "details": str(e)}), 500

"""User Login"""
@app.post("/auth/login")
def login_user():
 """Authenticate a user and return a JWT token"""
 json_data = request.get_json()

 """Validate input"""
 if not all(key in json_data for key in ("email", "password")):
    return jsonify({"error": "Missing required fields"}), 400

 """Find the user by email"""
 user = User.query.filter_by(email=json_data["email"]).first()
 if not user or not check_password_hash(user.password, json_data["password"]):
    return jsonify({"error": "Invalid email or password"}), 401

 """Generate a JWT token"""
 """access_token = create_access_token(identity={"id": user.profileId, "role": user.role})"""
 access_token = create_access_token(identity=str(user.profileId), additional_claims={"role": user.role})
 return jsonify(json_data, {
    "message": "Login successful",
    "access_token": access_token
 }), 200
 
"""Handle missing tokens"""
@app.errorhandler(NoAuthorizationError)
def handle_missing_token(e):
    return jsonify({"error": "Authorization token is missing"}), 401

"""Handle invalid tokens"""
@jwt.invalid_token_loader
def handle_invalid_token(reason):
    return jsonify({"error": "Invalid token", "details": reason}), 401

"""--------------------------------------------------------------------------------------------------"""
"""--RETRIEVING SCIENTIFIC DATA--"""
"""Fetching All Scientific Data"""
@app.get("/api/get-all-data")
@jwt_required()
def get_all_data():
 current_user = get_jwt_identity()
 apidata = Apidata.query.all()
 data=apidatas_schema.dump(apidata)
 return jsonify({"message": "Access granted", "user": current_user, "data": data}), 200

"""Fetching specific Scientific Data"""
@app.get("/api/get-data/<dataId>")
@jwt_required()
def get_data(dataId):
 apidata = Apidata.query.filter_by(dataId=dataId).first()
 return apidata_schema.jsonify(apidata), 200

"""Upload New Scientific Data"""
@app.post("/api/add-data")
@jwt_required()
def create_data():
 """Admin-only: Add new scientific data"""
 """Check admin role"""
 admin_check = admin_required()
 if admin_check:
    return admin_check

 json_data = request.get_json()
 new_data = Apidata(
    dataId=json_data['dataId'],
    temperatureWater=json_data['temperatureWater'],
    temperatureAir=json_data['temperatureAir'],
    humidity=json_data['humidity'],
    windSpeed=json_data['windSpeed'],
    precipitation=json_data['precipitation'],
    notes=json_data['notes']
 )
 try:
    db.session.add(new_data)
    db.session.commit()
    return apidata_schema.jsonify(new_data), 200
 except Exception as e:
    db.session.rollback()
    return jsonify({"msg": "Failed to add data", "error": str(e)}), 500

"""Update Specific Scientific Data elements like temperature only"""
@app.patch("/api/edit-data/<dataId>")
@jwt_required()
def update_data_field(dataId):
 """Admin-only: Update specific fields of scientific data"""
 """Check admin role"""
 admin_check = admin_required()
 if admin_check:
    return admin_check

 data = request.get_json()
 apidata = Apidata.query.get(dataId)
 if not apidata:
    return jsonify({"msg": "IoT data not found"}), 404

 """Update only the fields provided"""
 if "humidity" in data:
    apidata.humidity = data["humidity"]
 if "notes" in data:
    apidata.notes = data["notes"]
 if "precipitation" in data:
    apidata.precipitation = data["precipitation"]
 if "temperatureAir" in data:
    apidata.temperatureAir = data["temperatureAir"]
 if "temperatureWater" in data:
    apidata.temperatureWater = data["temperatureWater"]
 if "windSpeed" in data:
    apidata.windSpeed = data["windSpeed"]

 try:
    db.session.commit()
    return jsonify({"msg": "IoT data updated successfully", "IoTData": apidata.to_dict()}), 200
 except Exception as e:
    db.session.rollback()
    return jsonify({"msg": "Failed to update data", "error": str(e)}), 500

"""Update Scientific Data"""
@app.put("/api/update-data/<dataId>")
@jwt_required()
def update_data(dataId):
 """Admin-only: Replace all fields of scientific data"""
 """Check admin role"""
 admin_check = admin_required()
 if admin_check:
    return admin_check

 data = request.get_json()
 apidata = Apidata.query.get(dataId)
 if not apidata:
    return jsonify({"msg": "IoT data not found"}), 404

 apidata.humidity = data.get('humidity')
 apidata.notes = data.get('notes')
 apidata.precipitation = data.get('precipitation')
 apidata.temperatureAir = data.get('temperatureAir')
 apidata.temperatureWater = data.get('temperatureWater')
 apidata.windSpeed = data.get('windSpeed')

 try:
    db.session.commit()
    return jsonify({"msg": "IoT data replaced successfully", "IoT data": apidata.to_dict()}), 200
 except Exception as e:
    db.session.rollback()
    return jsonify({"msg": "Failed to replace data", "error": str(e)}), 500

"""Upload Bulk Scientific Data"""
@app.post("/api/add-data/bulk")
@jwt_required()
def create_data_bulk():
 """Admin-only: Add multiple scientific data records"""
 """ Check admin role"""
 admin_check = admin_required()
 if admin_check:
    return admin_check

 json_data = request.get_json()
 if not isinstance(json_data, list):
    return jsonify({"msg": "Invalid input. Expected a list of data"}), 400

 new_records = []
 for record in json_data:
    try:
        new_data = Apidata(
            dataId=record['dataId'],
            temperatureWater=record['temperatureWater'],
            temperatureAir=record['temperatureAir'],
            humidity=record['humidity'],
            windSpeed=record['windSpeed'],
            precipitation=record['precipitation'],
            notes=record['notes']
        )
        new_records.append(new_data)
    except KeyError as e:
        return jsonify({"msg": f"Missing required field: {str(e)}"}), 400

 try:
    db.session.add_all(new_records)
    db.session.commit()
    return jsonify({
        "msg": f"{len(new_records)} records added successfully",
        "data": [record.to_dict() for record in new_records]
    }), 200
 except Exception as e:
    db.session.rollback()
    return jsonify({"msg": "Failed to add bulk data", "error": str(e)}), 500

"""--------------------------------------------------------------------------------------------------"""
"""--RETRIEVING ANALYTIC DATA--"""
"""Fetching Predictive analytics Data"""
@app.get("/api/analytics/predictive")
@jwt_required()
def get_analytic_data():
 analytics = Analytic.query.all()
 return analytics_schema.jsonify(analytics)

@app.post("/api/analytics")
@jwt_required()
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
 if not products:
    return jsonify({"Error": "Products not found"}), 404
 return products_schema.jsonify(products), 200

"""Get Specific Products"""
@app.get("/api/get-products/<productId>")
def get_product_data(productId):
 product = Product.query.filter_by(productId=productId).first()
 if not product:
    return jsonify({"Error": "Product not found"}), 404
 return product_schema.jsonify(product), 200

"""Add new Product"""
@app.post("/api/add-product")
@jwt_required()
def create_product():
 """Admin-only: Add a new product"""
 admin_check = admin_required()
 if admin_check:
   return admin_check

 data = request.get_json()
 new_product = Product(
   productId=data["productId"],
   name=data["name"],
   description=data["description"],
   price=data["price"],
   stock=data["stock"]
 )
 try:
   db.session.add(new_product)
   db.session.commit()
   return product_schema.jsonify(new_product), 200
 except Exception as e:
   db.session.rollback()
   return jsonify({"msg": "Failed to add product", "error": str(e)}), 500

"""Add Bulk Products"""
@app.post("/api/add-products/bulk")
@jwt_required()
def add_bulk_products():
 """Admin-only: Add multiple products in bulk"""
 admin_check = admin_required()
 if admin_check:
   return admin_check

 data = request.get_json()
 if not isinstance(data, list):
   return jsonify({"error": "Invalid input. Expected a list of products."}), 400

 products = []
 errors = []

 for idx, product_data in enumerate(data):
   required_fields = ["name", "description", "price", "stock"]
   missing_fields = [field for field in required_fields if field not in product_data]
   if missing_fields:
      errors.append({"index": idx, "error": f"Missing fields: {', '.join(missing_fields)}"})
      continue

   try:
         new_product = Product(
            name=product_data["name"],
            description=product_data["description"],
            price=float(product_data["price"]),
            stock=int(product_data["stock"]),
         )
         products.append(new_product)
   except Exception as e:
         errors.append({"index": idx, "error": str(e)})

 if products:
   try:
      db.session.add_all(products)
      db.session.commit()
   except Exception as e:
      db.session.rollback()
      return jsonify({"error": "Failed to save products", "details": str(e)}), 500

 return jsonify({
   "message": f"{len(products)} products added successfully.",
   "products": [product.to_dict() for product in products],
   "errors": errors
 }), 200 if products else 400

'''Update Product Data'''
@app.put("/api/update-product/<productId>")
def update_product(productId):
 """Admin-only: Replace all fields of a product"""
 admin_check = admin_required()
 if admin_check:
   return admin_check

 data = request.get_json()
 product = Product.query.get(productId)
 if not product:
   return jsonify({"msg": "Product not found"}), 404

 product.name = data.get("name")
 product.description = data.get("description")
 product.price = data.get("price")
 product.stock = data.get("stock")

 try:
   db.session.commit()
   return jsonify({"msg": "Product replaced successfully", "product": product.to_dict()}), 200
 except Exception as e:
   db.session.rollback()
   return jsonify({"msg": "Failed to replace product", "error": str(e)}), 500

@app.patch("/api/edit-product/<productId>")
def edit_product(productId):
 """Admin-only: Update specific fields of a product"""
 admin_check = admin_required()
 if admin_check:
   return admin_check

 data = request.get_json()
 product = Product.query.get(productId)
 if not product:
   return jsonify({"msg": "Product not found"}), 404

 if "name" in data:
   product.name = data["name"]
 if "description" in data:
   product.description = data["description"]
 if "price" in data:
   product.price = data["price"]
 if "stock" in data:
   product.stock = data["stock"]

 try:
   db.session.commit()
   return jsonify({"msg": "Product updated successfully", "product": product.to_dict()}), 200
 except Exception as e:
   db.session.rollback()
   return jsonify({"msg": "Failed to update product", "error": str(e)}), 500
 
'''Delete a product'''
@app.delete('/api/delete-product/<productId>')
def delete_product(productId):
 """Admin-only: Delete a product"""
 admin_check = admin_required()
 if admin_check:
   return admin_check

 product = Product.query.get(productId)
 if not product:
   return jsonify({"msg": "Product not found"}), 404

 try:
   db.session.delete(product)
   db.session.commit()
   return jsonify({"msg": f"Product with ID {productId} deleted successfully"}), 200
 except Exception as e:
   db.session.rollback()
   return jsonify({"msg": "Failed to delete product", "error": str(e)}), 500

"""------------------------------------------------------------------------------"""
"""--USER ACCOUNT MANAGEMENT--"""

"""Retrieve Data of all User"""
@app.get("/api/get-user-profile")
@jwt_required()
def get_all_user_profile():
 """Admin-only: Retrieve all user profiles"""
 admin_check = admin_required()
 if admin_check:
    return admin_check

 users = User.query.all()
 if not users:
    return jsonify({"Error": "Users not found"}), 404
 return users_schema.jsonify(users), 200


'''Retrieve Data of a specific User'''
@app.get("/api/get-user-profile/<profileId>")
@jwt_required()
def get_user_profile(profileId):
 """Admin-only: Retrieve a specific user's profile"""
 admin_check = admin_required()
 if admin_check:
    return admin_check

 user = User.query.filter_by(profileId=profileId).first()
 if not user:
    return jsonify({"Error": "User not found"}), 404
 return user_schema.jsonify(user), 200

'''Allow User update profile information'''
@app.patch("/api/update-user-profile/<profileId>")
@jwt_required()
def update_user_profile(profileId):
 """Allow users to update their profile; role updates are admin-only"""
 current_user = get_jwt_identity()

 """Restrict updates to their own profile unless the user is an admin"""
 if current_user != str(profileId) and admin_required():
    return admin_required()

 data = request.get_json()
 user = User.query.get(profileId)
 if not user:
    return jsonify({"msg": "User not found"}), 404

 """Allow updating personal details"""
 if "firstname" in data:
    user.firstname = data["firstname"]
 if "lastname" in data:
    user.lastname = data["lastname"]
 if "email" in data:
    user.email = data["email"]

 """Role updates restricted to admins"""
 if "role" in data:
    if admin_required():
        return admin_required()
    user.role = data["role"]

 try:
    db.session.commit()
    return jsonify({"msg": "User updated successfully", "user": user.to_dict()}), 200
 except Exception as e:
    db.session.rollback()
    return jsonify({"msg": "Failed to update user", "error": str(e)}), 500

"""Delete user account---only admin has this permission"""
@app.delete('/api/delete-user-profile/<profileId>')
@jwt_required()
def delete_user_profile(profileId):
 """Admin-only: Delete a user account"""
 admin_check = admin_required()
 if admin_check:
    return admin_check

 user = User.query.get(profileId)
 if not user:
    return jsonify({"msg": "User not found"}), 404

 try:
    db.session.delete(user)
    db.session.commit()
    return jsonify({"msg": f"User with profileId {profileId} deleted successfully"}), 200
 except Exception as e:
    db.session.rollback()
    return jsonify({"msg": "Failed to delete user", "error": str(e)}), 500

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
@jwt_required()
def update_order(profileId):
 data = request.get_json() # access data from POST request
 print(json.dumps(data,indent=4))
 return jsonify(data)

'''--------------------------------------------------------------------------------------------------'''
'''Port'''
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)  