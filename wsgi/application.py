#!/usr/bin/env python

import os, pymongo, json, hashlib, bson

from bson.json_util import dumps as mongo_dumps
from bson.objectid import ObjectId
from bottle import Bottle, request, response, HTTPResponse

from db import get_database_connection

from auth import auth_app, jwt_required, admin_required, authenticate

from datetime import datetime

application = Bottle()
app = application
app.merge(auth_app)

@app.post('/api/v1/signin')
def login():
	data = request.json
	encoded = authenticate(data['email'], data['password'])
	if encoded:
		return encoded
	else:
		return HTTPResponse(status=401, body="Unauthorized.")

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

@app.post('/api/v1/user/<user_id>/edit')
@jwt_required
def edit_user(user, user_id):
	if user['id']!=user_id and user['is_admin']==False:
		HTTPResponse(status=401, body="Unauthorized.")
	response.content_type='application/json'
	data = request.json
	db = get_database_connection()	
	db.users.update(
		{'_id':ObjectId(user_id)},
		{'$set':
			{'name':data['name']}
		})
	return json.dumps({'success': True, 'msg': 'User edited.'})	

@app.get('/api/v1/menu/items')
def show_menu():
	db = get_database_connection()	
	data = db.menu.find()
	return mongo_dumps({'success': True, 'menu': data})

@app.post('/api/v1/user/<user_id>/orders/create')
@jwt_required
def create_order(user, user_id):
	if user['id']!=user_id and user['is_admin']==False:
		HTTPResponse(status=401, body="Unauthorized.")
	response.content_type='application/json'
	data = request.json
	order_date = datetime.now()
	order = {'user': user_id, 'items': data, 'date': order_date}
	db = get_database_connection()
	objs = []
	for item in data:
		obj = db.items.find_one({'_id': ObjectId(item['id'])})
		if obj:
			item['name'] = obj['name']
			item['value'] = item['quantity'] * obj['price']
			objs.append(item)
		else:
			return json.dumps({'success': True, 'msg': 'Invalid Item in Order.'})
	db.orders.insert(order)	
	return mongo_dumps({'success': True, 'msg': 'Order created.', 
						'orders': objs, 'date': order_date.strftime('%d/%m/%y %H:%M:%s')})

@app.post('/api/v1/menu/sessions/create')
@admin_required
def create_menu_session(user):
	response.content_type='application/json'
	data = request.json
	db = get_database_connection()
	session = db.menu.find_one({'_id': data['name']})
	if session:
		return json.dumps({'success': True, 'msg': 'Menu session already exists.'})
	else:
		db.menu.insert({'_id': data['name']})
		return json.dumps({'success': True, 'msg': 'Menu session created.'})

@app.post('/api/v1/menu/items/create')
@admin_required
def create_item(user):
	response.content_type='application/json'
	data = request.json
	db = get_database_connection()
	session = db.menu.find_one({'_id': data['session']})
	if session:
		if session.get('menu_items', False):
			for item in session.get('menu_items', []):
				if item['name']==data['name']:
					return json.dumps({'success': True, 'msg': 'Item already exists.'})
	else:
		return json.dumps({'success': True, 'msg': 'Menu session doesn`t exists.'})
	oid_ins = db.items.insert({'name': data['name'], 'price': data['price']})
	id_ins = str(oid_ins)
	db.menu.update(
		{'_id': data['session']}, 
		{'$push': {'menu_items': {'id': id_ins, 'name': data['name'], 'price': data['price']} }})
	return json.dumps({'success': True, 'msg': 'Item created.'})	
