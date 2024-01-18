from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return 'Messaging App'

@app.route('/messages')
def messages():
    messages = []
    for message in Message.query.all():
        message_dict = message.to_dict()
        messages.append(message_dict)
        
    response = make_response(
        jsonify(messages),
        200
    )
    
    return response

@app.route('/messages/<int:id>', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.get(id)
    
    if request.method == 'GET':
        if message is None:
            response = make_response(
                jsonify({'error': 'Not found'}),
                404
            )
        else:
            response = make_response(
                jsonify(message.to_dict()),
                200
            )
    elif request.method == 'POST':
        if message is None:
            response = make_response(
                jsonify({'error': 'Not found'}),
                404
            )
        else:
            message.body = request.json['body']
            message.username = request.json['username']
            db.session.commit()
            
            response = make_response(
                jsonify(message.to_dict()),
                200
            )
    elif request.method == 'PATCH':
        if message is None:
            response = make_response(
                jsonify({'error': 'Not found'}),
                404
            )
        else:
            message.body = request.json['body']
            message.username = request.json['username']
            db.session.commit()
            
            response = make_response(
                jsonify(message.to_dict()),
                200
            )
    elif request.method == 'DELETE':
        if message is None:
            response = make_response(
                jsonify({'error': 'Not found'}),
                404
            )
        else:
            db.session.delete(message)
            db.session.commit()
            
            response = make_response(
                jsonify(message.to_dict()),
                200
            )
    else:
        response = make_response(
            jsonify({'error': 'Method not allowed'}),
            405
        )
        
    return response

if __name__ == '__main__':
    app.run(port=5555)
