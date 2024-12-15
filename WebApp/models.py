from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declared_attr

db = SQLAlchemy()


class TransactionBase(db.Model):
    __abstract__ = True  # Mark this class as abstract, so no table is created for it

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    account = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    is_categorized = db.Column(db.Boolean, default=False)

    @declared_attr
    def category_level_1(cls):
        return db.Column(db.Integer, db.ForeignKey('categories.id'))

    @declared_attr
    def category_level_2(cls):
        return db.Column(db.Integer, db.ForeignKey('categories.id'))

    @declared_attr
    def category_level_3(cls):
        return db.Column(db.Integer, db.ForeignKey('categories.id'))

    @declared_attr
    def __tablename__(cls):
        # Dynamically set the table name to match the subclass name
        return cls.__name__.lower()

# Transactions Table
class Transaction(TransactionBase):
    sub_transactions = db.relationship(
            'SubTransaction',
            back_populates='parent_transaction',
            cascade='all, delete-orphan'
            )

class SubTransaction(TransactionBase):
    parent_transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'), nullable=False)
    parent_transaction = db.relationship('Transaction', back_populates='sub_transactions')


# Categories Table
class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    parent = db.relationship(
        'Category', 
        remote_side=[id],  # Refers to the 'id' column of this table
        backref='children'  # Allows easy access to child categories
    )





def init_db():
    db.create_all()  # Creates tables if they don't exist
