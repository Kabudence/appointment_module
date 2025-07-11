from flask import Flask

import staff.application.commands
import staff.application.queries
from staff.interfaces.staff_controller import staff_api
from shared.infrastructure.database import init_db

app = Flask(__name__)

app.register_blueprint(staff_api)

first_request = True

@app.before_request
def setup():
    global first_request
    if first_request:
        first_request = False
        # Initialize the database and create a test device on the first request
        init_db()


if __name__ == '__main__':
    app.run(debug=True)