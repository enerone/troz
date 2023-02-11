from flask import jsonify, request, url_for, abort
from app import db
from app.models import Room
from app.api import bp
from app.api.errors import bad_request
from app.api.auth import token_auth


@bp.route('/rooms/<int:id>', methods=['GET'])
@token_auth.login_required
def get_room(id):
    return jsonify(Room.query.get_or_404(id).to_dict())

@bp.route('/rooms', methods=['GET'])
@token_auth.login_required
def get_rooms():
    page = request.args.get('page', 1,  type=int)
    per_page = min(request.args.get('per_page',10, type=int), 100)
    data = Room.to_collection_dict(Room.query, page, per_page, 'api.get_rooms')
    return jsonify(data)

@bp.route('/rooms', methods=['POST'])
def create_room():
    data = request.get_json() or {}
    if 'name' not in data or 'type' not in data:
        return bad_request('must include name and type')
    room = Room()
    room.from_dict(data)
    db.session.add(room)
    db.session.commit()
    response = jsonify(room.to_dict())
    response.status_code = 200
    response.headers['Location'] = url_for('api.get_room', id=room.id)
    return response

@bp.route('/rooms/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_room(id):
    room = Room.query.get_or_404(id)
    data = request.get_json() or {}
    room.from_dict(data)
    db.session.commit()
    return jsonify(room.to_dict())

