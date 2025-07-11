
from flask import Blueprint,request
from schedules.application.commands.schedule_command_service import ScheduleCommandService
from schedules.application.queries.schedule_query_service import ScheduleQueryService
from schedules.infraestructure.repositories.schedule_repository import ScheduleRepository
from schedules.infraestructure.repositories.schedule_staff_repository import ScheduleStaffRepository


repo_schedule=ScheduleRepository()
repo_schedule_staff=ScheduleStaffRepository()
schedule_command_service = ScheduleCommandService( repo_schedule, repo_schedule_staff)
schedule_query_service = ScheduleQueryService(repo_schedule)

schedule_api = Blueprint('schedule', __name__)

from flask import jsonify


@schedule_api.route('/schedules', methods=['GET'])
def get_all_schedules():
    negocio_id = request.args.get('negocio_id', type=int)
    business_id = request.args.get('business_id', type=int)

    if not negocio_id:
        return jsonify({"error": "Missing negocio_id"}), 400

    schedules = schedule_query_service.get_all_days_by_negocio_business(
        negocio_id=negocio_id,
        business_id=business_id
    )
    return jsonify({"schedules": [schedule.to_dict() for schedule in schedules]}), 200

@schedule_api.route('/schedule-with-staff', methods=['GET'])
def get_schedule_with_staff():
    # Recupera los parámetros de la URL
    negocio_id = request.args.get('negocio_id', type=int)
    business_id = request.args.get('business_id', type=int)
    day = request.args.get('day', type=str)

    # Validaciones básicas
    if not (negocio_id and business_id and day):
        return jsonify({"error": "Missing one or more required params (negocio_id, business_id, day)"}), 400

    try:
        result = schedule_query_service.get_schedule_with_staff_by_negocio_business_and_day(
            negocio_id=negocio_id,
            business_id=business_id,
            day=day
        )
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@schedule_api.route('/schedule', methods=['GET'])
def get_schedule():
    negocio_id = request.args.get('negocio_id', type=int)
    business_id = request.args.get('business_id', type=int)
    day = request.args.get('day', type=str)

    # Validaciones básicas
    if not (negocio_id and business_id and day):
        return jsonify({"error": "Missing one or more required params (negocio_id, business_id, day)"}), 400

    try:
        result = schedule_query_service.get_by_negocio_business_and_day(
            negocio_id=negocio_id,
            business_id=business_id,
            day=day
        )
        return jsonify(result.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@schedule_api.route('/create-schedule', methods=['POST'])
def create_schedule():
    data = request.get_json()

    if not data or not all(key in data for key in ['negocio_id', 'business_id', 'day', 'start_time', 'end_time', 'staff_ids']):
        return jsonify({"error": "Missing required fields"}), 400

    staff_ids = data['staff_ids']

    if not (isinstance(staff_ids, list) or isinstance(staff_ids, int)):
        return jsonify({"error": "'staff_ids' must be a list or an integer"}), 400


    try:
        schedule = schedule_command_service.create(
            negocio_id=data['negocio_id'],
            business_id=data['business_id'],
            day=data['day'],
            start_time=data['start_time'],
            end_time=data['end_time'],
            staff_ids=staff_ids
        )
        return jsonify(schedule.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@schedule_api.route('/update-schedule', methods=['PUT'])
def update_schedule():
    data = request.get_json()

    if not data or not all(key in data for key in ['id', 'negocio_id', 'business_id', 'day', 'start_time', 'end_time', 'staff_ids']):
        return jsonify({"error": "Missing required fields"}), 400

    staff_ids = data['staff_ids']

    if not (isinstance(staff_ids, list) or isinstance(staff_ids, int)):
        return jsonify({"error": "'staff_ids' must be a list or an integer"}), 400

    try:
        schedule = schedule_command_service.update(
            schedule_id=data['id'],
            negocio_id=data['negocio_id'],
            business_id=data['business_id'],
            day=data['day'],
            start_time=data['start_time'],
            end_time=data['end_time'],
            staff_ids=staff_ids
        )
        return jsonify(schedule.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400