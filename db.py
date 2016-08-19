#!/usr/bin/env python

import pymongo

try:
	dummy = os.environ['OPENSHIFT_HOMEDIR']
	mongodb_host = os.environ['OPENSHIFT_MONGODB_DB_URL']
	mongodb_db_name = os.environ['OPENSHIFT_APP_NAME']
except:    
	mongodb_host = 'mongodb://localhost:27017'
	mongodb_db_name = 'simplerestaurant'      


# retornar conexao de base de dados mongodb
def get_database_connection():
	conn = pymongo.MongoClient(mongodb_host)
	return conn[mongodb_db_name]
