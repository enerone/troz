from datetime import datetime, timedelta
from hashlib import md5
from time import time
from flask import current_app, url_for
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import base64
import os
from app import db, login


followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page=page, per_page=per_page,
                                   error_out=False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data

class User(PaginatedAPIMixin, UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')
        
    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token
    
    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)
        
    @staticmethod
    def check_token(token):
        user=User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user
        

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)
    
    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username,
            'last_seen': self.last_seen.isoformat() + 'Z' if self.last_seen else None,
            'about_me': self.about_me,
            'post_count': self.posts.count(),
            'follower_count': self.followers.count(),
            'followed_count': self.followed.count(),
            '_links': {
                'self': url_for('api.get_user', id=self.id),
                'followers': url_for('api.get_user', id=self.id),
                'followed': url_for('api.get_user', id=self.id),
                'avatar': url_for('api.get_followed', id=self.id)
            }
            
        }
        if include_email:
            data['email'] = self.email
        return data
    
    def from_dict(self, data, new_user=False):
        for field in ['username', 'email', 'about_me']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])
           
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    language = db.Column(db.String(5))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class Bank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    qr = db.Column(db.String(255))
    name = db.Column(db.String(70))
    phone = db.Column(db.String(20))
    contact_name = db.Column(db.String(100))
    comments = db.Column(db.String(255))
    
    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'qr': self.qr,
            'name': self.name,
            'phone': self.phone,
            'contact_name': self.contact_name,
            'comments': self.comments            
        }
        return data
    
    def from_dict(self, data):
        for field in ['qr', 'name', 'phone', 'contact_name', 'comments']:
            if field in data:
                setattr(self, field, data[field])
                                 
class Genetic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    qr = db.Column(db.String(255))
    bank_id = db.Column(db.Integer, db.ForeignKey('bank.id'))
    name = db.Column(db.String(100))
    genealogy = db.Column(db.String(100))
    parent1_id = db.Column(db.Integer, db.ForeignKey('genetic.id'))
    parent2_id = db.Column(db.Integer, db.ForeignKey('genetic.id'))
    flowering_days = db.Column(db.Integer)
    ratio = db.Column(db.String(100))
    description = db.Column(db.Text())
    
    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'qr': self.qr,
            'bank': self.bank,
            'name': self.name,
            'phone': self.phone,
            'genealogy': self.genealogy,
            'parent1_id': self.parent1_id,
            'parent2_id': self.parent2_id,
            'flowering_days': self.flowering_days,
            'ratio': self.ratio,
            'description': self.description            
        }
        return data
    
    def from_dict(self, data):
        for field in ['qr', 'bank', 'name', 'phone', 'genealogy', 'parent1_id', 'parent2_id', 'flowering_days', 'ratio', 'description']:
            if field in data:
                setattr(self, field, data[field])

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    type = db.Column(db.String(50))
    message = db.Column(db.String(255))
    date = db.Column(db.DateTime)
    priority = db.Column(db.Integer)
    
    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'employee_id': self.employee_id,
            'type': self.type,
            'message': self.message,
            'date': self.date,
            'priority': self.priority                    
        }
        return data
    
    def from_dict(self, data):
        for field in ['employee_id', 'type', 'message', 'date', 'priority']:
            if field in data:
                setattr(self, field, data[field])


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    qr = db.Column(db.String(255))
    supervisor = db.Column(db.Integer, db.ForeignKey("employee.id"))
    state = db.Column(db.String(50))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(100))
    address = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    birthdate = db.Column(db.DateTime)
    notifications_profile_id = db.Column(db.Integer, db.ForeignKey("notification.id"))
    
    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'qr': self.qr,
            'supervisor': self.supervisor,
            'state': self.state,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'address': self.address,
            'phone': self.phone,
            'birthdate': self.birthdate,
            'notifications_profile_id': self.notifications_profile_id
                    
        }
        return data
    
    def from_dict(self, data):
        for field in ['qr', 'supervisor', 'state', 'first_name', 'last_name', 'address', 'phone', 'birthdate', 'notifications_profile_id']:
            if field in data:
                setattr(self, field, data[field])
    
class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    qr = db.Column(db.String(255))
    name = db.Column(db.String(255))
    type = db.Column(db.String(50))
    size = db.Column(db.Float)
    state = db.Column(db.String(50))
    max_plants = db.Column(db.Integer)
    description = db.Column(db.Text())
        
    def to_dict(self, include_email=False):
        data = {            
            'id': self.id,
            'qr': self.qr,
            'name': self.name,
            'type': self.type,
            'size': self.size,
            'state': self.state,
            'max_plants': self.max_plants,
            'description': self.description                    
        }
        return data
    
    def from_dict(self, data):
        for field in ['qr', 'name', 'type', 'size','state', 'max_plants', 'description']:
            if field in data:
                setattr(self, field, data[field])
                
class Line(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    qr = db.Column(db.String(255))
    x_axix_qty = db.Column(db.Integer)
    y_axix_qty = db.Column(db.Integer)
    description = db.Column(db.Text())
        
    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'qr': self.qr,
            'x_axis_qty': self.x_axis_qty,
            'y_axis_qty': self.y_axis_qty,
            'description': self.description                    
        }
        return data
    
    def from_dict(self, data):
        for field in ['qr', 'x_axis_qty', 'y_axis_qty', 'description']:
            if field in data:
                setattr(self, field, data[field])

class Spot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    qr = db.Column(db.String(255))
    room_id = db.Column(db.Integer, db.ForeignKey("room.id"))
    line_id = db.Column(db.Integer, db.ForeignKey("line.id"))
    coor_x = db.Column(db.Integer)
    coord_y = db.Column(db.Integer)
    description = db.Column(db.Text())
        
    def to_dict(self, include_email=False):
        data = {
            
            'id': self.id,
            'qr': self.qr,
            'room_id': self.room_id,
            'line_id': self.line_id,
            'coord_x': self.coord_x,
            'coord_y': self.coord_y,
            'description': self.description                    
        }
        return data
    
    def from_dict(self, data):
        for field in ['qr', 'room_id', 'line_id', 'coord_x', 'coord_y', 'description']:
            if field in data:
                setattr(self, field, data[field])
               
class Germoplasm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    qr = db.Column(db.String(255))
    genetic_id = db.Column(db.Integer, db.ForeignKey("genetic.id"))
    format = db.Column(db.String(50))
    start_date = db.Column(db.DateTime)
    comments = db.Column(db.Text())
        
    def to_dict(self, include_email=False):
        data = {
            
            'id': self.id,
            'qr': self.qr,
            'genetic_id': self.genetic_id,
            'format': self.format,
            'start_date': self.start_date,                  
            'comments': self.comments                  
        }
        return data
    
    def from_dict(self, data):
        for field in ['qr', 'genetic_id', 'format', 'start_date', 'comments']:
            if field in data:
                setattr(self, field, data[field])     

class Cycle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    qr = db.Column(db.String(255))
    room_id = db.Column(db.Integer, db.ForeignKey("room.id"))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    type = db.Column(db.String(50))
    plants_qty = db.Column(db.Integer)
    comments = db.Column(db.Text())
        
    def to_dict(self, include_email=False):
        data = {
            
            'id': self.id,
            'qr': self.qr,
            'room_id': self.room_id,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'type': self.type,
            'plants_qty': self.plants_qty,
            'comments': self.comments,
        }
        return data
    
    def from_dict(self, data):
        for field in ['qr', 'room_id', 'start_date', 'end_date', 'type', 'plants_qty', 'comments']:
            if field in data:
                setattr(self, field, data[field])         
          
class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    qr = db.Column(db.String(255))
    cycle_id = db.Column(db.Integer, db.ForeignKey("cycle.id"))
    genetic_id = db.Column(db.Integer, db.ForeignKey("genetic.id"))
    germoplasm_id = db.Column(db.Integer, db.ForeignKey("germoplasm.id"))
    spot_id = db.Column(db.Integer, db.ForeignKey("spot.id"))
    trimmer_id = db.Column(db.Integer, db.ForeignKey("employee.id"))    
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    plants_qty = db.Column(db.Integer)
    comments = db.Column(db.Text())

    
    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'qr': self.qr,
            'cycle_id': self.cycle_id,
            'genetic_id': self.genetic_id,
            'germoplasm_id': self.germoplasm_id,
            'spot_id': self.spot_id,
            'trimmer_id': self.trimmer_id,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'plants_qty': self.plants_qty,
            'comments': self.comments
                    
        }
        return data
    
    def from_dict(self, data):
        for field in ['qr', 'cycle_id', 'genetic_id', 'germoplasm_id', 'spot_id', 'trimmer_id', 'start_date', 'end_date', 'plants_qty', 'comments']:
            if field in data:
                setattr(self, field, data[field])
                
class Multimedia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plant_id = db.Column(db.Integer, db.ForeignKey("plant.id"))
    name = db.Column(db.String(100))
    url = db.Column(db.String(100))
    date = db.Column(db.DateTime)
    description = db.Column(db.Text())
        
    def to_dict(self, include_email=False):
        data = {
            
            'id': self.id,
            'plant_id': self.plant_id,
            'name': self.name,
            'url': self.url,
            'date': self.date,
            'description': self.description,
        }
        return data
    
    def from_dict(self, data):
        for field in ['plant_id', 'name', 'url', 'date', 'description']:
            if field in data:
                setattr(self, field, data[field])
    
    
class Bitacora(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plant_id = db.Column(db.Integer, db.ForeignKey("plant.id"))
    cycle_id = db.Column(db.Integer, db.ForeignKey("cycle.id"))
    room_id = db.Column(db.Integer, db.ForeignKey("room.id"))
    title = db.Column(db.String(255))
    description = db.Column(db.Text())
        
    def to_dict(self, include_email=False):
        data = {
            
            'id': self.id,
            'plant_id': self.plant_id,
            'cycle_id': self.cycle_id,
            'room_id': self.room_id,
            'title': self.title,
            'description': self.description,
        }
        return data
    
    def from_dict(self, data):
        for field in ['plant_id', 'cycle_id', 'room_id', 'title', 'description']:
            if field in data:
                setattr(self, field, data[field])