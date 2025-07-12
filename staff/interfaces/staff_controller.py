from flask import Blueprint, request, jsonify, current_app

staff_api = Blueprint('staff', __name__)

@staff_api.route('/create-staff', methods=['POST'])
def create_staff():
    data = request.get_json()
    staff_command_service = current_app.config["staff_command_service"]
    try:
        staff = staff_command_service.create(
            speciality=data['speciality'],
            name=data['name'],
            negocio_id=data['negocio_id'],
            max_capacity=data['max_capacity'],
            dni=data['dni']
        )
        return jsonify(staff_to_json(staff)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@staff_api.route('/update-staff', methods=['PUT'])
def update_staff():
    data = request.get_json()
    staff_command_service = current_app.config["staff_command_service"]
    try:
        staff = staff_command_service.update(
            id=data['id'],
            speciality=data['speciality'],
            name=data['name'],
            negocio_id=data['negocio_id'],
            max_capacity=data['max_capacity'],
            dni=data['dni']
        )
        return jsonify(staff_to_json(staff)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@staff_api.route('/get-staff', methods=['GET'])
def get_staff():
    staff_id = request.args.get('id', type=int)
    if not staff_id:
        return jsonify({"error": "Missing staff ID"}), 400

    staff_query_service = current_app.config["staff_query_service"]
    staff = staff_query_service.get_by_id(staff_id)
    if not staff:
        return jsonify({"error": "Staff not found"}), 404
    return jsonify(staff_to_json(staff)), 200

@staff_api.route('/list-staff', methods=['GET'])
def get_staff_list():
    staff_query_service = current_app.config["staff_query_service"]
    staff_list = staff_query_service.list_all()
    return jsonify([{
        "id": staff.id,
        "speciality": staff.speciality,
        "name": staff.name,
        "negocio_id": staff.negocio_id,
        "max_capacity": staff.max_capacity,
        "dni": staff.dni
    } for staff in staff_list]), 200

@staff_api.route('/get-staff-by-dni', methods=['GET'])
def get_staff_by_dni():
    staff_dni = request.args.get('dni', type=str)
    if not staff_dni:
        return jsonify({"error": "Missing staff DNI"}), 400
    staff_query_service = current_app.config["staff_query_service"]
    staff = staff_query_service.get_by_dni(staff_dni)
    if not staff:
        return jsonify({"error": "Staff not found"}), 404
    return jsonify(staff_to_json(staff)), 200

def staff_to_json(staff):
    return {
        "id": staff.id,
        "speciality": staff.speciality,
        "name": staff.name,
        "negocio_id": staff.negocio_id,
        "max_capacity": staff.max_capacity,
        "dni": staff.dni
    }
