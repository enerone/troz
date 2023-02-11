
from flask import jsonify, request, url_for, abort
from app import db
from app.models import Notification
from app.api import bp
from app.api.errors import bad_request
from app.api.auth import token_auth


@bp.route('/notifications/<int:id>', methods=['GET'])
@token_auth.login_required
def get_notification(id):
    return jsonify(Notification.query.get_or_404(id).to_dict())

@bp.route('/notifications', methods=['GET'])
@token_auth.login_required
def get_notifications():
    page = request.args.get('page', 1,  type=int)
    per_page = min(request.args.get('per_page',10, type=int), 100)
    data = Notification.to_collection_dict(Notification.query, page, per_page, 'api.get_notifications')
    return jsonify(data)

@bp.route('/notifications', methods=['POST'])
def create_notification():
    data = request.get_json() or {}
    if 'employee_id' not in data or 'message' not in data:
        return bad_request('must include employee, phone and message')
    notification = Notification()
    notification.from_dict(data)
    db.session.add(notification)
    db.session.commit()
    response = jsonify(notification.to_dict())
    response.status_code = 200
    response.headers['Location'] = url_for('api.get_notification', id=notification.id)
    return response

@bp.route('/notifications/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_notifications(id):
    notification = Notification.query.get_or_404(id)
    data = request.get_json() or {}
    notification.from_dict(data)
    db.session.commit()
    return jsonify(notification.to_dict())