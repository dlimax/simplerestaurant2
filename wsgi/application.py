#!/usr/bin/env python

import os, pymongo, json, hashlib, bson
from bson.json_util import dumps as mongo_dumps
from bottle import Bottle, request, response, HTTPResponse

from db import get_database_connection

from auth import auth_app, jwt_required, admin_required, authenticate

application = Bottle()
app = application
app.merge(auth_app)

user = None

# atender requisicoes do tipo get para /
@app.get('/')
def index():
    return "Boa sorte!"

# atender requisicoes do tipo post para /api/v1/signin
# curl -H "Content-Type: application/json" -X POST -d '{"email":"scott@gmail.com", "password":"12345"}' http://localhost:8080/api/v1/signin
@app.post('/api/v1/signin')
def login():
	data = request.json
	encoded = authenticate(data['email'], data['password'])
	if encoded:
		return encoded
	else:
		return HTTPResponse(status=401, body="Nao autorizado.")

# atender requisicoes do tipo post para /api/v1/users/create
# curl -i -H "Content-Type: application/json" -X POST -d '{"name": "Eduardo", "email": "xyz@gmail", "password":"xyz"}' http://localhost:8080/api/v1/users/create
@app.post('/api/v1/users/create')
def create_user():	
	response.content_type='application/json'
	data = request.json	
	name = data["name"] # obtem nome enviado por parametro postado.
	email = data["email"] # obtem email enviado por parametro postado.
	password = hashlib.md5(data["password"].encode()).hexdigest() # obtem hash md5 da senha enviada.
	db = get_database_connection() # conecta com a base de dados e armazena a conexao em db.
	user = db.users.find_one({'email': email}) # find_one retorna um documento, 												
											   # ou None se nao encontrar nenhum.
	if user:
		# usuario ja existe. retornar em formato JSON padrao com mensagem.
		return json.dumps({'success': True, 'msg': 'usuario ja existente.'})
	else:
		# usuario nao existe. inserir novo usuario.
		db.users.insert({'name': name, 'email': email, 'password': password})
		# retornar em formato JSON padrao com mensagem.
		return json.dumps({'success': True, 'msg': 'usuario cadastrado.'})


# atender requisicoes do tipo get para /api/v1/users
# curl -i -H "Content-Type: application/json" -X GET  http://localhost:8080/api/v1/users
@app.get('/api/v1/users')
@jwt_required
def list_user(user):
	response.content_type='application/json'
	db = get_database_connection() # conecta com a base de dados e armazena a conexao em db.
	users = db.users.find()		
	return mongo_dumps(users)


# atender requisicoes do tipo get para /api/v1/admin/users
# curl -i -H "Content-Type: application/json" -X GET  http://localhost:8080/api/v1/admin/users
@app.get('/api/v1/admin/users')
@admin_required
def list_user_from_admin(user):
	response.content_type='application/json'
	db = get_database_connection() # conecta com a base de dados e armazena a conexao em db.
	users = db.users.find()		
	return mongo_dumps(users)
