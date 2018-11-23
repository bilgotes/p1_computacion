from flask import Flask
from pymongo import MongoClient
from flask import jsonify
from flask import render_template
from flask import json
from flask import g
from flask import request
from flask import make_response
import urllib2 as ul

# añadir event listener para mongoDB
class ServerLogger(monitoring.ServerListener):

    def opened(self, event):
        logging.info("Server {0.server_address} added to topology "
                     "{0.topology_id}".format(event))

    def description_changed(self, event):
        previous_server_type = event.previous_description.server_type
        new_server_type = event.new_description.server_type
        if new_server_type != previous_server_type:
            # server_type_name was added in PyMongo 3.4
            logging.info(
                "Server {0.server_address} changed type from "
                "{0.previous_description.server_type_name} to "
                "{0.new_description.server_type_name}".format(event))

    def closed(self, event):
        logging.warning("Server {0.server_address} removed from topology "
                        "{0.topology_id}".format(event))


app = Flask(__name__)


# Local database connection parameters
db_host = "localhost"
db_port = "27017"

# Remote database connection parameters
channel = 622234
baseURL = 'http://api.thingspeak.com/channels/%s/fields/3.json' % channel

@app.route('/')
def indice():
    ultima_entrada=getLastN()[1]
    return render_template('index.html',entradas=ultima_entrada)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/umbral_historico', methods=['POST','GET'])
def umbral_historico():
    selected = []
    umbral = int(request.form['umbral'])
    for elem in getLastN():
	if int(elem['clics']) > umbral and not any(d['titulo'] == elem['titulo'] for d in selected):
		selected.append(elem)
		if len(selected) == 10:
			break
    return render_template('umbral_historico.html',umbral=umbral,entradas=selected)

@app.route('/valor_medio', methods=['POST','GET'])
def valor_medio():
    acumulado=0
    media = 0
    if request.cookies.get('bd') == 'externa' :
	# recoge los datos de mi canal de ThingSpeak usando GET
	database="ThingSpeak"
        get_request = baseURL
	response=ul.urlopen(baseURL)
	webdata = json.loads(response.read())
	feeds =  webdata['feeds']
	counter = 0
	for elem in feeds:
		try:
			acumulado = acumulado+int(elem['field3'])
			counter = counter+1
		except TypeError:
			pass
	media = acumulado / counter
	resp = make_response(render_template('valor_medio.html',database=database,media=media,counter=counter))
    	resp.set_cookie('bd','',expires=0)
    else :
	database="Local"
	curs_entr = getLastN()
	for elem in curs_entr:
                acumulado = acumulado+int(elem['clics'])
	counter = curs_entr.count()
	media = acumulado / counter
	resp = make_response(render_template('valor_medio.html',database=database,media=media,counter=counter))
    	resp.set_cookie('bd','externa')
    return resp

def getLastN():
    pymdb = get_db()["p1"]
    pymco = pymdb["meneos"]
    return pymco.find().sort("ts", -1) # find() devuelve un objeto cursor

def get_db():
    db = getattr(g, '_database', None)	# devuelve el valor del atributo _database de g. Si no existe devuelve None para escapar de la excepcion y crear una conexion
    if db is None:
        #db = g._database = MongoClient("mongodb://%s:%s/" %(db_host,db_port))
        db = g._database = MongoClient("mongodb://%s:%s/" %(db_host,db_port),event_listeners=[ServerLogger()])
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run(debug=True)	
