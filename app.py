from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from auth.auth import requires_auth
from database.models import Employee, Department, Joining, setup_db, db
from sqlalchemy import func
from flask import Flask, request, Response
from datetime import datetime



def create_app(flag_db=True, test_config=None):
    app = Flask(__name__)
    with app.app_context():
        if flag_db:
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
                return jsonify(
                    {'success': False, 'error': 'Employee Not Found'}), 404

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
            department_id = new_data['department_id']
            joining_date = new_data['joining_date']

            # Add a new employee
            new_employee = Employee(name=name, designation=designation)
            Employee.insert(new_employee)

            # Get the Employee ID of newly added Employee
            employee = db.session.query(Employee.id).filter(Employee.name == name).all()

            #Insert a new row in the Joining table for the new employee
            new_joining = Joining(employee_id=employee[0][0], department_id=department_id, joining_date=joining_date)
            Joining.insert(new_joining)
            response = {
                'success': True,
                'message': 'Employee added successfully',
                'employee': name
                }
            db.session.close()
            return jsonify(response), 200

        except Exception as e:
            db.session.close()
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
                return jsonify(
                    {'success': False, 'error': 'Employee Not Found'}), 422

            update_data = request.json
            name = update_data['name']
            designation = update_data['designation']

            Employee.patch(employee, name, designation)
            
            response = {
                'success': True,
                'message': 'Employee updated successfully',
                'employee': update_data['name']
                }
            return jsonify(response), 200

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
                return jsonify(
                    {'success': False, 'error': 'Employee Not Found'}), 422
            
            # If there are employees associated to a joining table then it is also required to deleted
            employee_count = db.session.query(func.count(Joining.id)).filter(Joining.employee_id == employee_id).all()
            if employee_count[0][0] > 0:
                joinings = db.session.query(Joining.id).filter(Joining.employee_id == employee_id).all()
                delete_joining = Joining.query.get(joinings[0][0])
                Joining.delete(delete_joining)

            # Delete employee once joinings are deleted
            Employee.delete(employee)

            response = {
                'success': True,
                'message': 'Employee deleted successfully',
                'employee': employee.name
                }
            db.session.close()
            return jsonify(response), 200

        except Exception as e:
            abort(401)

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
                    'name': department.name
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
                'name': department.name
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
            return jsonify(response), 200

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
               return jsonify(
                    {'success': False, 'error': 'Department Not Found'}), 404

            update_data = request.json
            name = update_data['name']

            Department.patch(department, name)
            
            response = {
                'success': True,
                'message': 'Department updated successfully',
                'department': department.name
                }
            return jsonify(response), 200

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
                return jsonify(
                    {'success': False, 'error': 'Department Not Found'}), 422
            
            # If there are employees associated to a department then it can be deleted
            employee_count = db.session.query(func.count(Joining.employee_id)).filter(Joining.department_id == department_id).all()
            if employee_count[0][0] > 0:
                db.session.rollback()   
                return jsonify(
                    {'success': False, 'error': 'Employee Found as a Child record, Dept can not be deleted'}), 422

            # Delete the department if there are no employee associated to it
            Department.delete(department)

            response = {
                'success': True,
                'message': 'Department deleted successfully',
                'department': department.name
                }
            db.session.close()
            return jsonify(response), 200

        except Exception as e:
            db.session.rollback()       
            abort(404)



#  ----------------------------------------------------------------
#  Joining - GET ALL
#  ----------------------------------------------------------------
    @app.route('/joining', methods=['GET'])
    @requires_auth('get:joining')
    def joining(payload):
        try:
            joinings = db.session.query(Joining.id, Employee.id, Employee.name, Department.id, Department.name, Joining.joining_date).join(Joining, Joining.employee_id == Employee.id).join(Department, Department.id == Joining.department_id).all()
            joining_data = []
            for joining in joinings:
                joining_data.append({
                    "joining_id":joining[0],
                    "employee_id": joining[1],
                    "employee_name": joining[2],
                    "department_id": joining[3],
                    "department_name": joining[4],
                    "joining_date": str(joining[5])
                    })
                    
            response = {
                    'success': True,
                    'joining': joining_data
                    }
            db.session.close()
            return jsonify(response), 200
    
        except Exception as e:
            db.session.rollback()
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
            department_id = new_data['department_id']
            joining_date = new_data['joining_date']
    
            new_joining = Joining(employee_id=employee_id, department_id=department_id, joining_date=joining_date)
            Joining.insert(new_joining)

            response = {
                'success': True,
                'message': 'Joining added successfully',
                'employee': new_joining.id
                }
            return jsonify(response), 200

        except Exception as e:
            abort(400)


    #app = create_app()
    # error handlers
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({"success": False, "error": 400, "message": "bad request"}),
            400,
        )    

    @app.errorhandler(405)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 405, "message": "method not allowed"}),
            405,
        )

    @app.errorhandler(500)
    def server_error(error):
        return (
            jsonify({"success": False, "error": 500, "message": "Internal Server Error"}),
            500,
        )
    
    return app

app = create_app()
if __name__ == '__main__':
    app.run()
