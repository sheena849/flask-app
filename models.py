from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

# Consistent metadata usage
metadata = MetaData(naming_convention={'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s'})
db = SQLAlchemy(metadata=metadata)

# Association table for many-to-many relationship
user_lifts = db.Table(
    'user_lifts',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('lift_id', db.Integer, db.ForeignKey('lifts.id'), primary_key=True)
)

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    serialize_rules = ('-product.user', '-lift.users')
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    product = db.relationship('Product', back_populates='user')
    lift = db.relationship('Lift', secondary=user_lifts, back_populates='users')

class Product(db.Model, SerializerMixin):
    __tablename__ = 'products'
    serialize_rules = ('-user.product',)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='product')

class Lift(db.Model, SerializerMixin):
    __tablename__ = 'lifts'
    serialize_rules = ('-users.lift',)
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    users = db.relationship('User', secondary=user_lifts, back_populates='lift')
