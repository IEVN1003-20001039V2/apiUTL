from flask import Flask, jsonify, request
from flask_mysqldb import MYSQL
from flask_cors import CORS


from config import config 

app=Flask(__name__)


CORS(app, resources={r"/alumnos/*":  {"origins":"http://localhost:4200"}})

conexion=MYSQL(app)

@app.route("/alumnos", methods=["GET"])
def listar_alumnos():
    try:
        cursor=conexion.connection.cursor()
        sql="SELECT * FROM alumnos ORDER BY nombre ASC"
        cursor.execute(sql)
        datos=cursor.ferchall()
        alumnos=[]
        for fila in datos:
            alumno={"matricula":fila[0],"nombre":fila[1],"apaterno":fila[2],"amaterno":fila[3],"corre":fila[4]}
            
        alumnos.append(alumno)
        return jsonify({'alumno':alumnos, 'mensajes':'Alumnos listados',"exito":True})
        
    except Exception as e:
        return jsonify({"mensaje":"error al conectar BD{}".format(ex),'exito':False})
    
    
def pagina_no_encontrada(errot):
        return jsonify({"mensaje": "Error 404: {}".format(errot),'exito':False})


if __name__=="__main__":
      app.config.from_object(config['development'])
      app.register_error_handler(400,pagina_no_encontrada)
      app.run()