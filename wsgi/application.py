#!/usr/bin/env python

import os, pymongo, json, hashlib, bson
from bson.json_util import dumps as mongo_dumps
from bottle import Bottle, request, response, HTTPResponse

from db import get_database_connection

from auth import auth_app, jwt_required, admin_required, authenticate

application = Bottle()
app = application
app.merge(auth_app)

# curl -H "Content-Type: application/json" -X GET  http://localhost:8080/
@app.get('/')
def index():
    return "Hello World!"

# curl -H "Content-Type: application/json" -X POST -d '{"email":"scott@gmail.com", "password":"12345"}' http://localhost:8080/api/v1/signin
@app.post('/api/v1/signin')
def login():
	data = request.json
	encoded = authenticate(data['email'], data['password'])
	if encoded:
		return encoded
	else:
		return HTTPResponse(status=401, body="Unauthorized.")

# curl -H "Content-Type: application/json" -X POST -d '{"name": "Eduardo", "email": "xyz@gmail.com", "password":"xyz"}' http://localhost:8080/api/v1/users/create
@app.post('/api/v1/users/create')
def create_user():	
	response.content_type='application/json'
	data = request.json	
	name = data["name"] 
	email = data["email"] 
	password = hashlib.md5(data["password"].encode()).hexdigest()
	db = get_database_connection()
	user = db.users.find_one({'email': email})
	if user:
		return json.dumps({'success': True, 'msg': 'user already exists.'})
	else:
		db.users.insert({'name': name, 'email': email, 'password': password})
		return json.dumps({'success': True, 'msg': 'user added.'})

# curl -H "Content-Type: application/json" -X GET  http://localhost:8080/api/v1/users
@app.get('/api/v1/users')
@jwt_required
def list_user(user):
	response.content_type='application/json'
	db = get_database_connection() 
	users = db.users.find()		
	return mongo_dumps(users)

# curl -H "Content-Type: application/json" -X GET  http://localhost:8080/api/v1/admin/users
@app.get('/api/v1/admin/users')
@admin_required
def list_user_from_admin(user):
	response.content_type='application/json'
	db = get_database_connection() 
	users = db.users.find()		
	return mongo_dumps(users)
