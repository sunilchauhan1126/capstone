from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from auth.auth import requires_auth
from database.models import Employee, Department, Joining, setup_db


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

#  ----------------------------------------------------------------
#  Employee - GET ALL
#  ----------------------------------------------------------------
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

#  ----------------------------------------------------------------
#  Employee - GET for ID
#  ----------------------------------------------------------------
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

#  ----------------------------------------------------------------
#  Employee - POST
#  ----------------------------------------------------------------
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

#  ----------------------------------------------------------------
#  Employee - PATCH
#  ----------------------------------------------------------------
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

#  ----------------------------------------------------------------
#  Employee - DELETE
#  ----------------------------------------------------------------
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

#  ----------------------------------------------------------------
#  Department - GET ALL
#  ----------------------------------------------------------------
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

#  ----------------------------------------------------------------
#  Department - GET for ID
#  ----------------------------------------------------------------
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
            
#  ----------------------------------------------------------------
#  Department - POST
#  ----------------------------------------------------------------    
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

#  ----------------------------------------------------------------
#  Department - PATCH
#  ----------------------------------------------------------------
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
            
#  ----------------------------------------------------------------
#  Department - DELETE
#  ----------------------------------------------------------------
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

#  ----------------------------------------------------------------
#  Joining - GET ALL
#  ----------------------------------------------------------------
    @app.route('/joining', methods=['GET'])
    @requires_auth('get:joining')
    def joining(payload):
        try:
            joinings = db.session.query(Employee.id, Employee.name, Department.id, Department.name, Joining.joining_date).join(Joining, Joining.employee_id == Employee.id).join(Department, Department.id == Joining.department_id).all()
            joining_data = []
            for joining in joinings:
                joining_data.append({
                    "employee_id": joining[0],
                    "employee_name": joining[1],
                    "department_id": joining[2],
                    "department_name": joining[3],
                    "joining_date": str(joining[4])
                    })
            db.session.close()
                    
            response = {
                    'success': True,
                    'joining': joining_data
                }
            return jsonify(response), 200
    
        except Exception as e:
            abort(401)
            
#  ----------------------------------------------------------------
#  Joining - POST
#  ----------------------------------------------------------------
    @app.route('/joining', methods=['POST'])
    @requires_auth('post:joining')
    def add_joining(payload):
        try:
            new_data = request.json
            employee_id = new_data['employee_id']
            department_id = new_data['employee_id']
            joining_date = new_data['joining_date']
            
            new_joining = Joining(employee_id=employee_id, department_id=department_id, joining_date=joining_date)

            Joining.insert(new_joining)

            response = {
                'success': True,
                'message': 'Joining added successfully',
                'employee': new_joining.id
            }
            return jsonify(response), 201

        except Exception as e:
            abort(400)

app = create_app()

if __name__ == '__main__':
    app.run()
