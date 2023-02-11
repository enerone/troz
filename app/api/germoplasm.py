from flask import jsonify, request, url_for, abort
from app import db
from app.models import Germoplasm
from app.api import bp
from app.api.errors import bad_request
from app.api.auth import token_auth


@bp.route('/germoplasms/<int:id>', methods=['GET'])
@token_auth.login_required
def get_germoplasm(id):
    return jsonify(Germoplasm.query.get_or_404(id).to_dict())

@bp.route('/germoplasms', methods=['GET'])
@token_auth.login_required
def get_germoplasms():
    page = request.args.get('page', 1,  type=int)
    per_page = min(request.args.get('per_page',10, type=int), 100)
    data = Germoplasm.to_collection_dict(Germoplasm.query, page, per_page, 'api.get_germoplasms')
    return jsonify(data)

@bp.route('/germoplasms', methods=['POST'])
def create_germoplasm():
    data = request.get_json() or {}
    if 'first_name' not in data or 'last_name' not in data:
        return bad_request('must include first_name and last_name')
    germoplasm = Germoplasm()
    germoplasm.from_dict(data)
    db.session.add(germoplasm)
    db.session.commit()
    response = jsonify(germoplasm.to_dict())
    response.status_code = 200
    response.headers['Location'] = url_for('api.get_germoplasm', id=germoplasm.id)
    return response

@bp.route('/germoplasms/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_germoplasm(id):
    germoplasm = Germoplasm.query.get_or_404(id)
    data = request.get_json() or {}
    germoplasm.from_dict(data)
    db.session.commit()
    return jsonify(germoplasm.to_dict())

