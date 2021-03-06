from email.policy import default
from app import db


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    postal_code = db.Column(db.String(64))
    city = db.Column(db.String(120))
    street = db.Column(db.String(128))
    house_number_start = db.Column(db.Integer, default=0)
    house_number_end = db.Column(db.Integer)
    unit_price = db.Column(db.Integer)
    grid_fees = db.Column(db.Integer)
    kwh_price = db.Column(db.Integer)

    def __init__(self, postal_code, city, street, house_number_start, house_number_end, unit_price, grid_fees, kwh_price):
        self.postal_code = postal_code
        self.city = city
        self.street = street
        self.house_number_start = house_number_start
        self.house_number_end = house_number_end
        self.unit_price = unit_price
        self.grid_fees = grid_fees
        self.kwh_price = kwh_price
        
    def __repr__(self):
        return '<Location postal_code: {}>'.format(self.postal_code)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


db.create_all()