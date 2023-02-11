
from flask import jsonify, request, url_for, abort
from app import db
from app.models import Employee
from app.api import bp
from app.api.errors import bad_request
from app.api.auth import token_auth


@bp.route('/employees/<int:id>', methods=['GET'])
@token_auth.login_required
def get_employee(id):
    return jsonify(Employee.query.get_or_404(id).to_dict())

@bp.route('/employees', methods=['GET'])
@token_auth.login_required
def get_employees():
    page = request.args.get('page', 1,  type=int)
    per_page = min(request.args.get('per_page',10, type=int), 100)
    data = Employee.to_collection_dict(Employee.query, page, per_page, 'api.get_employees')
    return jsonify(data)

@bp.route('/employees', methods=['POST'])
def create_employee():
    data = request.get_json() or {}
    if 'first_name' not in data or 'last_name' not in data:
        return bad_request('must include first_name and last_name')
    employee = Employee()
    employee.from_dict(data)
    db.session.add(employee)
    db.session.commit()
    response = jsonify(employee.to_dict())
    response.status_code = 200
    response.headers['Location'] = url_for('api.get_employee', id=employee.id)
    return response

@bp.route('/employees/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_employee(id):
    employee = Employee.query.get_or_404(id)
    data = request.get_json() or {}
    employee.from_dict(data)
    db.session.commit()
    return jsonify(employee.to_dict())

