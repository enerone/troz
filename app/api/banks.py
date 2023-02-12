
from flask import jsonify, request, url_for, abort
from app import db
from app.models import Bank
from app.api import bp
from app.api.errors import bad_request
from app.api.auth import token_auth


@bp.route('/banks/<int:id>', methods=['GET'])
@token_auth.login_required
def get_bank(id):
    return jsonify(Bank.query.get_or_404(id).to_dict())

@bp.route('/banks', methods=['GET'])
@token_auth.login_required
def get_banks():
    page = request.args.get('page', 1,  type=int)
    per_page = min(request.args.get('per_page',10, type=int), 100)
    data = Bank.to_collection_dict(Bank.query, page, per_page, 'api.get_banks')
    return jsonify(data)

@bp.route('/banks', methods=['POST'])
@token_auth.login_required
def create_bank():
    data = request.get_json() or {}
    if 'name' not in data or 'phone' not in data:
        return bad_request('must include name, phone and contact_name')
    bank = Bank()
    bank.from_dict(data)
    db.session.add(bank)
    db.session.commit()
    response = jsonify(bank.to_dict())
    response.status_code = 200
    response.headers['Location'] = url_for('api.get_bank', id=bank.id)
    return response

@bp.route('/banks/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_bank(id):
    bank = Bank.query.get_or_404(id)
    data = request.get_json() or {}
    bank.from_dict(data)
    db.session.commit()
    return jsonify(bank.to_dict())

