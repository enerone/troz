from flask import jsonify, request, url_for, abort
from app import db
from app.models import Plant
from app.api import bp
from app.api.errors import bad_request
from app.api.auth import token_auth


@bp.route('/plants/<int:id>', methods=['GET'])
@token_auth.login_required
def get_plant(id):
    return jsonify(Plant.query.get_or_404(id).to_dict())

@bp.route('/plants', methods=['GET'])
@token_auth.login_required
def get_plants():
    page = request.args.get('page', 1,  type=int)
    per_page = min(request.args.get('per_page',10, type=int), 100)
    data = Plant.to_collection_dict(Plant.query, page, per_page, 'api.get_plants')
    return jsonify(data)

@bp.route('/plants', methods=['POST'])
def create_plant():
    data = request.get_json() or {}
    if 'cycle_id' not in data or 'germoplasm_id' not in data:
        return bad_request('must include cycle_id and germoplasm_id')
    plant = Plant()
    plant.from_dict(data)
    db.session.add(plant)
    db.session.commit()
    response = jsonify(plant.to_dict())
    response.status_code = 200
    response.headers['Location'] = url_for('api.get_plant', id=plant.id)
    return response

@bp.route('/plants/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_plant(id):
    plant = Plant.query.get_or_404(id)
    data = request.get_json() or {}
    plant.from_dict(data)
    db.session.commit()
    return jsonify(plant.to_dict())

