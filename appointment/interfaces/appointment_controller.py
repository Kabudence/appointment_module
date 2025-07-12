from flask import Blueprint, request, jsonify, current_app
from datetime import datetime

appointment_api = Blueprint('appointment_api', __name__)

# Crear una cita
@appointment_api.route('/appointments', methods=['POST'])
def create_appointment():
    data = request.get_json()
    try:
        start_time = datetime.fromisoformat(data['start_time'])
        end_time = datetime.fromisoformat(data['end_time'])
        client_id = data['client_id']
        negocio_id = data['negocio_id']
        staff_id = data['staff_id']
        business_id = data['business_id']
        service_id = data['service_id']

        # Usa el service inyectado
        appointment_command_service = current_app.config["appointment_command_service"]

        appointment = appointment_command_service.create(
            start_time=start_time,
            end_time=end_time,
            client_id=client_id,
            negocio_id=negocio_id,
            staff_id=staff_id,
            business_id=business_id,
            service_id=service_id,
        )
        return jsonify(appointment.to_dict()), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Obtener una cita por ID
@appointment_api.route('/appointments/<int:appointment_id>', methods=['GET'])
def get_appointment(appointment_id):
    appointment_query_service = current_app.config["appointment_query_service"]
    appointment = appointment_query_service.get_by_id(appointment_id)
    if appointment:
        return jsonify(appointment.__dict__), 200
    else:
        return jsonify({'error': 'Appointment not found'}), 404

# Listar citas por día y negocio o staff
@appointment_api.route('/appointments', methods=['GET'])
def list_appointments():
    day = request.args.get('day')
    negocio_id = request.args.get('negocio_id', type=int)
    staff_id = request.args.get('staff_id', type=int)

    appointment_query_service = current_app.config["appointment_query_service"]

    if staff_id and day:
        appointments = appointment_query_service.list_by_staff_and_day(staff_id, day)
    elif day and negocio_id:
        appointments = appointment_query_service.list_by_day_and_negocio(day, negocio_id)
    else:
        return jsonify({'error': 'Missing required query params'}), 400

    result = [a.__dict__ for a in appointments]
    return jsonify(result), 200

# Cancelar cita
@appointment_api.route('/appointments/<int:appointment_id>/cancel', methods=['POST'])
def cancel_appointment(appointment_id):
    appointment_command_service = current_app.config["appointment_command_service"]
    try:
        appointment = appointment_command_service.cancel(appointment_id)
        return jsonify(appointment.__dict__), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Actualizar estado
@appointment_api.route('/appointments/<int:appointment_id>/status', methods=['POST'])
def update_appointment_status(appointment_id):
    appointment_command_service = current_app.config["appointment_command_service"]
    data = request.get_json()
    try:
        new_status = data['status']
        appointment = appointment_command_service.update_status(appointment_id, new_status)
        return jsonify(appointment.__dict__), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Endpoint para ver slots disponibles
@appointment_api.route('/available-slots', methods=['GET'])
def get_available_slots():
    negocio_id = request.args.get('negocio_id', type=int)
    business_id = request.args.get('business_id', type=int)
    day = request.args.get('day', type=str)
    duration = request.args.get('service_duration_min', type=int, default=60)

    if not (negocio_id and day):
        return jsonify({"error": "Missing required params"}), 400

    # Llama al query service inyectado
    availability_query_service = current_app.config["availability_query_service"]

    slots = availability_query_service.get_available_slots(
        negocio_id, business_id, day, duration
    )
    return jsonify({"available_slots": slots}), 200
