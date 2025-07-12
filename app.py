from flask import Flask

from shared.factory.container_factory import build_services
from shared.infrastructure.database import init_db
from appointment.interfaces.appointment_controller import appointment_api
from schedules.interfaces.schedule_controller import schedule_api
from staff.interfaces.staff_controller import staff_api

app = Flask(__name__)
app.register_blueprint(staff_api)
app.register_blueprint(schedule_api)
app.register_blueprint(appointment_api)

first_request = True

@app.before_request
def setup():
    global first_request
    if first_request:
        first_request = False
        init_db()
        # Inyecta los services en la app (lo hace solo una vez)
        services = build_services()
        for key, value in services.items():
            app.config[key] = value

if __name__ == '__main__':
    app.run(debug=True)
