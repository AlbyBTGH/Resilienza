# Classi/ClasseUtenti/Classe_t_ruolo/Controller_t_ruolo.py
from flask import Blueprint, request, jsonify
from Classi.ClasseUtenti.Classe_t_ruolo.Service_t_ruolo import Service_t_ruolo

t_ruolo_controller = Blueprint('ruolo', __name__)
service_t_ruolo = Service_t_ruolo()

@t_ruolo_controller.route("/<int:ruolo_id>", methods=['GET'])
def get_ruolo(ruolo_id):
    ruolo = service_t_ruolo.get_by_id(ruolo_id)
    if ruolo:
        return jsonify(ruolo)
    else:
        return jsonify({'error': 'Ruolo non trovato'}), 404

@t_ruolo_controller.route("/", methods=['GET'])
def get_all_ruoli():
    ruoli = service_t_ruolo.get_all()
    return jsonify(ruoli)

@t_ruolo_controller.route("/", methods=['POST'])
def create_ruolo():
    data = request.json
    cod_ruolo = data.get('COD_RUOLO')
    descr = data.get('DESCR')
    dt_fine_val = data.get('DT_FINE_VAL')
    modificato_da = data.get('MODIFICATO_DA')
    ordinatore = data.get('ORDINATORE')
    visualizza_notifiche = data.get('VISUALIZZA_NOTIFICHE')

    if not descr:
        return jsonify({'error': 'Descrizione del ruolo mancante'}), 400
    
    result = service_t_ruolo.create(cod_ruolo, descr, dt_fine_val, modificato_da, ordinatore, visualizza_notifiche)
    if 'Error' in result:
        return jsonify(result), 500
    return jsonify(result), 201

@t_ruolo_controller.route("/<int:ruolo_id>", methods=['PUT'])
def update_ruolo(ruolo_id):
    data = request.json
    cod_ruolo = data.get('COD_RUOLO')
    descr = data.get('DESCR')
    dt_fine_val = data.get('DT_FINE_VAL')
    modificato_da = data.get('MODIFICATO_DA')
    ordinatore = data.get('ORDINATORE')
    visualizza_notifiche = data.get('VISUALIZZA_NOTIFICHE')
    
    result = service_t_ruolo.update(ruolo_id, cod_ruolo, descr, dt_fine_val, modificato_da, ordinatore, visualizza_notifiche)
    if 'Error' in result:
        return jsonify(result), 500
    return jsonify(result)

@t_ruolo_controller.route("/<int:ruolo_id>", methods=['DELETE'])
def delete_ruolo(ruolo_id):
    result = service_t_ruolo.delete(ruolo_id)
    if 'Error' in result:
        return jsonify(result), 500
    return jsonify(result)
