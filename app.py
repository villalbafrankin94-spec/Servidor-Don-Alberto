from flask import Flask, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

ruta_archivo = '/var/www/html/peritajes.json'

# Crear archivo si no existe
if not os.path.exists(ruta_archivo):
    with open(ruta_archivo, 'w') as f:
        json.dump([], f)

# Inventario inventado
registros = {
    "servidor": "Servidor Villalba",
    "hora": str(datetime.now()),
    "inventario": [
        {
            "moto": "Yamaha FZ",
            "placa": "LAC167",
            "estado": "Cambio de aceite"
        },
        {
            "moto": "Pulsar NS200",
            "placa": "FSV228",
            "estado": "Revision de frenos"
        }
    ]
}

# Ruta GET inventario
@app.route('/api/registros', methods=['GET'])
def ver_registros():
    return jsonify(registros)

# Ruta GET peritajes
@app.route('/api/peritajes', methods=['GET'])
def ver_peritajes():
    with open(ruta_archivo, 'r') as f:
        peritajes = json.load(f)

    return jsonify(peritajes)

# Ruta POST peritajes
@app.route('/api/peritajes', methods=['POST'])
def agregar_peritaje():
    data = request.get_json()

    with open(ruta_archivo, 'r') as f:
        peritajes = json.load(f)

    nueva_placa = {
        "placa": data["placa"].upper(),
    }

    peritajes.append(nueva_placa)

    with open(ruta_archivo, 'w') as f:
        json.dump(peritajes, f, indent=4)

    return jsonify({
        "mensaje": "Moto registrada correctamente",
        "datos": nueva_placa
    }), 201

# Ruta DELETE peritajes
@app.route('/api/peritajes/<placa>', methods=['DELETE'])
def eliminar_peritaje(placa):

    with open(ruta_archivo, 'r') as f:
        peritajes = json.load(f)

    nueva_lista = []
    moto_removida = None

    for moto in peritajes:
        if moto["placa"] == placa:
            moto_removida = moto
        else:
            nueva_lista.append(moto)

    if moto_removida is None:
        return jsonify({
            "error": "Vehículo no encontrado"
        }), 404

    with open(ruta_archivo, 'w') as f:
        json.dump(nueva_lista, f, indent=4)

    return jsonify({
        "message": f"Vehículo {placa} entregado al cliente con éxito",
        "moto_removida": moto_removida
    }), 200

@app.route('/api/inventario')
def inventario():
    return jsonify({
        "mensaje": "Modulo inventario"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
