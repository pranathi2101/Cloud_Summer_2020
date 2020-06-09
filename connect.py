import ibm_db, os, json

# if 'VCAP_SERVICES' in os.environ:
# 	db2info = json.loads(os.environ['VCAP_SERVICES'])['dashDB'][0]
# 	db2cred = db2info["credentials"]
# 	appenv = json.loads(os.environ['VCAP_APPLICATION'])
# else:
# 	raise ValueError('Expected cloud environment')

# connection = ibm_db.connect("DATABASE="+db2cred['db']+";HOSTNAME="+db2cred['hostname']+";PORT="+str(db2cred['port'])+";UID="+db2cred['username']+";PWD="+db2cred['password']+";","","")

connection = ibm_db.connect('DATABASE=BLUDB;'
	'HOSTNAME=dashdb-txn-sbox-yp-dal09-04.services.dal.bluemix.net;'
	'PORT=50000;'
	'PROTOCOL=TCPIP;'
	'UID=kdw79117;'
	'PWD=d86d^m38fg0sc237;', '', '')
