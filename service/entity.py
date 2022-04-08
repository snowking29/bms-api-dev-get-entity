import uuid
import json
import bson
import traceback
import pymongo as py
from db_util.get_connection import mongodb_conn
from db_util.get_collection import mongodb_collection

def getAll(entity,params):
    conn = mongodb_conn()
    print("Info Base de datos: ", conn.server_info())
    if conn is None:
        #No conexión, salida anticipada
        return
    try:
        collection = conn.bmsDB[entity]
    except py.errors.CollectionInvalid as e:
        traceback.print_exc()
        print("No se encontró la colección en la base de datos: %s" %e)
        return
    
    data = json.loads(json.dumps(list(collection.find(params,{"_id":0}))))
    
    if len(data) == 0:
        data = {}
        success = "false"
        code = "01"
        value = "No se encontró información."
    else:
        data = data[0]
        success = "true"
        code = "00"
        value = "Se proceso correctamente la solicitud."
    
    conn.close() 
    
    response = {
        "success": success,
        "configuration": {
            "data": json.loads(json.dumps(data)),
            "meta": {
                "status": {
                    "code": code,
                    "message_ilgn": [{
                        "locale": "es_PE",
                        "value": value
                    }]
                }
            }
        }
    }
    print("Response payload: ", json.dumps(response))
    return response