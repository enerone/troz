from flask import jsonify, request, url_for, abort
from app import db
from app.models import Bitacora
from app.api import bp
from app.api.errors import bad_request
from app.api.auth import token_auth


@bp.route('/bitacoras/<int:id>', methods=['GET'])
@token_auth.login_required
def get_bitacora(id):
    return jsonify(Bitacora.query.get_or_404(id).to_dict())

@bp.route('/bitacoras', methods=['GET'])
@token_auth.login_required
def get_bitacoras():
    page = request.args.get('page', 1,  type=int)
    per_page = min(request.args.get('per_page',10, type=int), 100)
    data = Bitacora.to_collection_dict(Bitacora.query, page, per_page, 'api.get_bitacoras')
    return jsonify(data)

@bp.route('/bitacoras', methods=['POST'])
def create_bitacora():
    data = request.get_json() or {}
    if 'plant_id' not in data or 'name' not in data:
        return bad_request('must include plant_id and name')
    bitacora = Bitacora()
    bitacora.from_dict(data)
    db.session.add(bitacora)
    db.session.commit()
    response = jsonify(bitacora.to_dict())
    response.status_code = 200
    response.headers['Location'] = url_for('api.get_bitacora', id=bitacora.id)
    return response

@bp.route('/bitacoras/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_bitacora(id):
    bitacora = Bitacora.query.get_or_404(id)
    data = request.get_json() or {}
    bitacora.from_dict(data)
    db.session.commit()
    return jsonify(bitacora.to_dict())

