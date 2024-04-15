from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Enable CORS to allow frontend requests
CORS(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Initialize SQLAlchemy
db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        
        messages = Message.query.order_by(Message.created_at.asc()).all()
        messages_json = [message.to_dict() for message in messages]
        return jsonify(messages_json)
    
    elif request.method == 'POST':
        data = request.get_json()
        new_message = Message(body=data.get('body'), username=data.get('username'))
        db.session.add(new_message)
        db.session.commit()
        
        return jsonify(new_message.to_dict()), 201

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def message_by_id(id):
    # Retrieve the message by ID
    message = Message.query.get(id)
    
    if not message:
        # Return 404 error if message not found
        return make_response(jsonify({'error': 'Message not found'}), 404)
    
    if request.method == 'PATCH':
    
        data = request.get_json()
    
        message.body = data.get('body', message.body)
    
        db.session.commit()
    
        return jsonify(message.to_dict())
    
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        return make_response('', 204)

if __name__ == '__main__':
    app.run(port=5555)
