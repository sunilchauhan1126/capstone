from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from auth.auth import requires_auth
from database.models import Employee, Department, setup_db


def create_app(active=True, test_config=None):
    app = Flask(__name__)
    with app.app_context():
        if active:
            setup_db(app)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PUT, PATCH, DELETE')
        return response

# --------------------------------------------------------------
# Employee
# --------------------------------------------------------------

    @app.route('/employee', methods=['GET'])
    @requires_auth('get:employee')
    def employee(payload):
        try:
            employees = Employee.query.all()
            employee_data = []
            for employee in employees:
                employee_data.append({
                    'id': employee.id,
                    'name': employee.name,
                    'designation': employee.designation
                })
            response = {
                'success': True,
                'employees': employee_data
            }
            return jsonify(response), 200

        except Exception as e:
            abort(401)

    @app.route('/employee/<int:employee_id>', methods=['GET'])
    @requires_auth('get:employees')
    def employee_detail(payload, employee_id):
        try:
            employee = Employee.query.get(employee_id)

            if not employee:
                abort(404)

            response = {
                'success': True,
                'id': employee.id,
                'name': employee.name,
                'designation': employee.designation
            }
            return jsonify(response), 200

        except Exception as e:
            abort(401)

    @app.route('/employee', methods=['POST'])
    @requires_auth('post:employee')
    def add_employee(payload):
        try:

            new_data = request.json
            name = new_data['name']
            designation = new_data['designation']

            new_employee = Emplyee(name=name, designation=designation)

            Emplyee.insert(new_employee)

            response = {
                'success': True,
                'message': 'Employee added successfully',
                'employee': new_employee.name
            }
            return jsonify(response), 201

        except Exception as e:
            abort(422)

    @app.route('/employee/<int:employee_id>', methods=['PATCH'])
    @requires_auth('patch:employee')
    def patch_employee(payload, employee_id):
        try:
            employee = Employee.query.get(employee_id)

            if not employee:
                abort(404)

            updated_data = request.json
            name = updated_data['name']
            designation = updated_data['designation']

            Employee.patch(employee, title, release_date)

            response = {
                'success': True,
                'message': 'Employee updated successfully',
                'employee': updated_data.name
            }
            return jsonify(response), 201

        except Exception as e:
            abort(422)

    @app.route('/employee/<int:employee_id>', methods=['DELETE'])
    @requires_auth('delete:employee')
    def delete_employeee(payload, employee_id):
        try:
            employee = Employee.query.get(employee_id)

            if not employee:
                abort(404)

            Employee.delete(employee)

            response = {
                'success': True,
                'message': 'Employee deleted successfully',
                'employee': employee.name
            }
            return jsonify(response), 201

        except Exception as e:
            abort(422)

# --------------------------------------------------------------
# Department
# --------------------------------------------------------------

    @app.route('/department', methods=['GET'])
    @requires_auth('get:department')
    def department(payload):
        try:
            departments = Department.query.all()
            department_data = []
            for department in departments:
                department_data.append({
                    'id': department.id,
                    'name': department.name,
                })
                
            response = {
                'success': True,
                'departments': department_data
            }
            return jsonify(response), 200

        except Exception as e:
            abort(401)

    @app.route('/department/<int:department_id>', methods=['GET'])
    @requires_auth('get:department')
    def department_detail(payload, department_id):
        try:
            department = Department.query.get(department_id)

            if not department:
                return jsonify(
                    {'success': False, 'error': 'Department Not Found'}), 404

            response = {
                'success': True,
                'id': department.id,
                'name': department.name,
            }
            return jsonify(response), 200

        except Exception as e:
            abort(401)

    @app.route('/department', methods=['POST'])
    @requires_auth('post:department')
    def add_department(payload):
        try:
            new_data = request.json
            name = new_data['name']
            
            new_department = Department(name=name)

            Department.insert(new_department)

            response = {
                'success': True,
                'message': 'Department added successfully',
                'department': new_department.name
            }
            return jsonify(response), 201

        except Exception as e:
            abort(400)

    @app.route('/department/<int:department_id>', methods=['PATCH'])
    @requires_auth('patch:department')
    def patch_department(payload, department_id):
        try:
            department = Department.query.get(department_id)

            if not department:
                abort(404)

            update_data = request.json
            name = update_data['name']

            Department.patch(department, name)

            response = {
                'success': True,
                'message': 'Department updated successfully',
                'department': department.name
            }
            return jsonify(response), 201

        except Exception as e:
            abort(422)

    @app.route('/department/<int:department_id>', methods=['DELETE'])
    @requires_auth('delete:department')
    def delete_department(payload, department_id):
        try:
            department = Department.query.get(department_id)

            if not department:
                abort(404)

            Department.delete(department)

            response = {
                'success': True,
                'message': 'Department deleted successfully',
                'department': department.name
            }
            return jsonify(response), 201

        except Exception as e:
            abort(422)

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
