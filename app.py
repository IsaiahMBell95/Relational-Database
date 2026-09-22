from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Table, Column, String, Integer, DateTime, Float, select
from marshmallow import fields, validate, ValidationError
from datetime import datetime


# Initialize Flask App
app = Flask(__name__)

# MySQL database config
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:Clemson21!@localhost/ecommerce_api"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Creating Base Model
class Base(DeclarativeBase):
    pass

# Initialize SQLAlchemy & Marshmallow
db = SQLAlchemy(model_class=Base)
db.init_app(app)
ma = Marshmallow(app)

# Association Table
order_product = Table(
    "order_product",
    Base.metadata,
    Column("order_id", Integer, ForeignKey("orders.id"), primary_key=True),
    Column("product_id", Integer, ForeignKey("products.id"), primary_key=True),
)


# Models
class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)

    orders: Mapped[list["Order"]] = relationship(back_populates="user")

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="orders")
    products: Mapped[list["Product"]] = relationship(
        secondary=order_product,
        back_populates="orders"
    )



class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)

    orders: Mapped[list["Order"]] = relationship(
        secondary=order_product,
        back_populates="products"
    )


# Marshmallow Schemas
class UserSchema(ma.SQLAlchemyAutoSchema):
    name = fields.String(required=True, validate=validate.Length(min=1, max=80))
    address = fields.String(required=True, allow_none=True, validate=validate.Length(max=255))
    email = fields.Email(required=True, validate=validate.Length(min=3, max=150))

    class Meta:
        model = User
        include_fk = True
    

class OrderSchema(ma.SQLAlchemyAutoSchema):
    order_date = fields.DateTime(required=True)
    user_id = fields.Integer(required=True, validate=validate.Range(min=1))

    class Meta:
        model = Order
        include_fk = True
        

class ProductSchema(ma.SQLAlchemyAutoSchema):
    product_name = fields.String(required=True, validate=validate.Length(min=1, max=100))
    price = fields.Float(required=True, validate=validate.Range(min=0))

    class Meta:
        model = Product
        include_fk = True

# Initialize Schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

       
with app.app_context():
    db.create_all()


# User Endpoints
@app.route('/users', methods=['GET'])
def get_users():
    query = select(User)
    users = db.session.execute(query).scalars().all()
    return users_schema.jsonify(users), 200

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = db.session.get(User, id)
    return user_schema.jsonify(user), 200

@app.route('/users', methods=['POST'])
def create_user():
    try:
        user_data = user_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 404

    new_user = User(name=user_data['name'], address=user_data['address'], email=user_data['email'])
    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user), 201

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = db.session.get(User, id)

    if not user:
        return jsonify({"message": "Invalid user id"}), 400

    try:
        user_data = user_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    user.name = user_data['name']
    user.email = user_data['email']

    db.session.commit()
    return user_schema.jsonify(user), 200

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = db.session.get(User, id)

    if not user:
        return jsonify({"message": "Invalid user id"}), 400

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"successfully delete user {id}"}), 200

# Product Endpoints
@app.route('/products', methods=['GET'])
def get_products():
    query = select(Product)
    products = db.session.execute(query).scalars().all()
    return products_schema.jsonify(products), 200

@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = db.session.get(Product, id)
    return product_schema.jsonify(product), 200

@app.route('/products', methods=['POST'])
def create_product():
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 404

    new_product = Product(product_name=product_data['product_name'], price=product_data['price'])
    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product), 201

@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = db.session.get(Product, id)

    if not product:
        return jsonify({"message": "Invalid user id"}), 400

    try:
        product_data = product_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    product.product_name = product_data['product_name']
    product.price = product_data['price']

    db.session.commit()
    return product_schema.jsonify(product), 200

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = db.session.get(Product, id)

    if not product:
        return jsonify({"message": "Invalid product id"}), 400

    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": f"successfully delete product {id}"}), 200

# Order Endpoints
@app.route('/orders/<int:order_id>/add_product/<int:product_id>', methods=['PUT'])
def add_product_to_order(order_id, product_id):
    order = Order.query.get(order_id)
    product = Product.query.get(product_id)

    order.products.append(product)
    db.session.commit()
    return jsonify({"message": f"{product.product_id} got added to{order_id} "})
  

@app.route("/orders/user/<int:user_id>", methods=["GET"])
def get_orders_by_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    orders = db.session.execute(
        db.select(Order).where(Order.user_id == user_id)
    ).scalars().all()

    return orders_schema.jsonify(orders), 200

@app.route('/orders', methods=['POST'])
def create_order():
    try:
        order_data = product_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_order = Order(order_date=order_data['order_date'], user_id=order_data['user_id'])
    db.session.add(new_order)
    db.session.commit()

    return order_schema.jsonify(new_order), 201

@app.route("/orders/<int:order_id>/products", methods=["GET"])
def get_products_for_order(order_id):
    order = db.session.get(Order, order_id)
    if not order:
        return jsonify({"message": "Order not found"}), 404

    products = db.session.execute(
        db.select(Product)
        .join(order_product, Product.id == order_product.c.product_id)
        .where(order_product.c.order_id == order_id)
    ).scalars().all()

    return products_schema.jsonify(products), 200

@app.route('/orders/<int:order_id>/remove_product/<int:product_id>', methods=['DELETE'])
def remove_product_from_order(order_id, product_id):
    product = db.session.get(Product, id)
    if not product:
        return jsonify({"message": "Product not found"}), 404
    
    order = db.session.get(Order, id)
    if not order:
        return jsonify({"message": "Order not found"}), 404

    item = db.delete(order_product).where(
        (order_product.c.order_id == order_id) &
        (order_product.c.product_id == product_id)
    )
    db.session.execute(item)
    db.session.commit()
    return jsonify({"message": f"Product {product_id} removed from order {order_id}"}), 200

if __name__ == "__main__":
    app.run(debug=True)
    
