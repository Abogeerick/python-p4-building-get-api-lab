#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def get_bakeries():
    bakeries = Bakery.query.all()
    response = Response(response=json.dumps([bakery.serialize() for bakery in bakeries]), 
                        status=200, 
                        mimetype='application/json')
    return response

@app.route('/bakeries/<int:id>')
def get_bakery_by_id(id):
    bakery = Bakery.query.get(id)
    if bakery is None:
        response = Response(response=json.dumps({"error": "Bakery not found"}), 
                            status=404, 
                            mimetype='application/json')
        return response
    response = Response(response=json.dumps(bakery.serialize_with_baked_goods()), 
                        status=200, 
                        mimetype='application/json')
    return response


@app.route('/baked_goods/by_price', methods=['GET'])
def get_baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    response = Response(response=json.dumps([good.serialize() for good in baked_goods]), 
                        status=200, 
                        mimetype='application/json')
    return response


@app.route('/baked_goods/most_expensive', methods=['GET'])
def get_most_expensive_baked_good():
    most_expensive_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if most_expensive_good is None:
        response = Response(response=json.dumps({"error": "No baked goods found"}), 
                            status=404, 
                            mimetype='application/json')
        return response
    response = Response(response=json.dumps(most_expensive_good.serialize()), 
                        status=200, 
                        mimetype='application/json')
    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)
