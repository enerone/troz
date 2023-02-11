
from flask import jsonify, request, url_for, abort
from app import db
from app.models import Genetic
from app.api import bp
from app.api.errors import bad_request
from app.api.auth import token_auth


@bp.route('/genetics/<int:id>', methods=['GET'])
@token_auth.login_required
def get_genetic(id):
    return jsonify(Genetic.query.get_or_404(id).to_dict())

@bp.route('/genetics', methods=['GET'])
@token_auth.login_required
def get_genetics():
    page = request.args.get('page', 1,  type=int)
    per_page = min(request.args.get('per_page',10, type=int), 100)
    data = Genetic.to_collection_dict(Genetic.query, page, per_page, 'api.get_genetics')
    return jsonify(data)

@bp.route('/genetics', methods=['POST'])
def create_genetic():
    data = request.get_json() or {}
    if 'name' not in data or 'flowering_days' not in data:
        return bad_request('must include name, phone and flowering_days')
    genetic = Genetic()
    genetic.from_dict(data)
    db.session.add(genetic)
    db.session.commit()
    response = jsonify(genetic.to_dict())
    response.status_code = 200
    response.headers['Location'] = url_for('api.get_genetic', id=genetic.id)
    return response

@bp.route('/genetics/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_genetic(id):
    genetic = Genetic.query.get_or_404(id)
    data = request.get_json() or {}
    genetic.from_dict(data)
    db.session.commit()
    return jsonify(genetic.to_dict())

