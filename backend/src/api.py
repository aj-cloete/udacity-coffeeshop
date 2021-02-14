import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()


# # ROUTES

@app.route('/drinks')
def drinks_short():
    """
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
    """

    drinks = Drink.query.all()
    return (jsonify(dict(
        success=True,
        drinks=[drink.short() for drink in drinks],
    )),
            200) if drinks else (jsonify({}), 404)


# @requires_auth('get:drinks-detail')
@app.route('/drinks-detail')
def drinks_long():
    """
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
    """
    drinks = Drink.query.all()
    return (jsonify(dict(
        success=True,
        drinks=[drink.long() for drink in drinks],
    )),
            200) if drinks else (jsonify({}), 404)


# @requires_auth('post:drinks')
@app.route('/drinks', methods=["POST"])
def create_drink():
    """
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
    """
    req = request.json.get
    drink = Drink(title=req('title'), recipe=req('recipe'))
    return (jsonify(dict(
        success=True,
        drinks=[drink],
    )), 200) if drink else (jsonify({}), 406)


# @requires_auth('patch:drinks')
@app.route('/drinks/<int:id>', methods=["PATCH"])
def patch_drink():
    """
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
    """
    drink = Drink.query.filter(Drink.id == id).one_or_none()
    for att in request.json:
        setattr(drink, att, request.json.get(att))
    drink.update()

    return (jsonify(dict(
        success=True,
        drinks=[drink],
    )), 200) if drink else (jsonify({}), 405)


# @requires_auth('delete:drinks')
@app.route('/drinks/<int:id>', methods=["DELETE"])
def delete_drink():
    """
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
    """
    drink = Drink.query.filter(Drink.id == id).one_or_none()
    id = drink.id
    drink.delete()

    return (jsonify(dict(
        success=True,
        delete=id,
    )), 200) if drink else (jsonify({}), 405)


# # Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "not found"
    }), 404


@app.errorhandler(AuthError)
def unauthorised(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "unauthorised"
    }), 401
