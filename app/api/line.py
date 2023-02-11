from flask import jsonify, request, url_for, abort
from app import db
from app.models import Line
from app.api import bp
from app.api.errors import bad_request
from app.api.auth import token_auth


@bp.route('/lines/<int:id>', methods=['GET'])
@token_auth.login_required
def get_line(id):
    return jsonify(Line.query.get_or_404(id).to_dict())

@bp.route('/lines', methods=['GET'])
@token_auth.login_required
def get_lines():
    page = request.args.get('page', 1,  type=int)
    per_page = min(request.args.get('per_page',10, type=int), 100)
    data = Line.to_collection_dict(Line.query, page, per_page, 'api.get_lines')
    return jsonify(data)

@bp.route('/lines', methods=['POST'])
def create_line():
    data = request.get_json() or {}
    if 'first_name' not in data or 'last_name' not in data:
        return bad_request('must include first_name and last_name')
    line = Line()
    line.from_dict(data)
    db.session.add(line)
    db.session.commit()
    response = jsonify(line.to_dict())
    response.status_code = 200
    response.headers['Location'] = url_for('api.get_line', id=line.id)
    return response

@bp.route('/lines/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_line(id):
    line = Line.query.get_or_404(id)
    data = request.get_json() or {}
    line.from_dict(data)
    db.session.commit()
    return jsonify(line.to_dict())

