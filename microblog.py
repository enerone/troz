from app import create_app, db, cli
from app.models import User, Post, Bank, Genetic, Cycle, Employee, Germoplasm, Line, Multimedia, Notification, Plant, Room, Spot

app = create_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {    
            'db': db, 
            'User': User, 
            'Post': Post, 
            'Bank':Bank, 
            'Genetic': Genetic, 
            'Cycle': Cycle,
            'Room': Room,
            'Employee': Employee,
            'Line': Line,
            'Plant': Plant,
            'Multimedia': Multimedia,
            'Notification': Notification,
            'Germoplasm' : Germoplasm,
            'Spot' : Spot           
            }
