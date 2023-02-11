from flask import jsonify, request, url_for, abort
from app import db
from app.models import Cycle
from app.api import bp
from app.api.errors import bad_request
from app.api.auth import token_auth


@bp.route('/cycles/<int:id>', methods=['GET'])
@token_auth.login_required
def get_cycle(id):
    return jsonify(Cycle.query.get_or_404(id).to_dict())

@bp.route('/cycles', methods=['GET'])
@token_auth.login_required
def get_cycles():
    page = request.args.get('page', 1,  type=int)
    per_page = min(request.args.get('per_page',10, type=int), 100)
    data = Cycle.to_collection_dict(Cycle.query, page, per_page, 'api.get_cycles')
    return jsonify(data)

@bp.route('/cycles', methods=['POST'])
def create_cycle():
    data = request.get_json() or {}
    if 'room_id' not in data or 'type' not in data:
        return bad_request('must include room_id and type')
    cycle = Cycle()
    cycle.from_dict(data)
    db.session.add(cycle)
    db.session.commit()
    response = jsonify(cycle.to_dict())
    response.status_code = 200
    response.headers['Location'] = url_for('api.get_cycle', id=cycle.id)
    return response

@bp.route('/cycles/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_cycle(id):
    cycle = Cycle.query.get_or_404(id)
    data = request.get_json() or {}
    cycle.from_dict(data)
    db.session.commit()
    return jsonify(cycle.to_dict())

