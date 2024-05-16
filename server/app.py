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

@app.route('/messages')
def messages():
    return [message.to_dict() for message in Message.query.all()], 200
    

@app.post('/messages')
def post_message():
    new_message = Message(
        body=request.json.get('body'),
        username=request.json.get('username')
    )

    db.session.add( new_message )
    db.session.commit()

    return new_message.to_dict(), 201

@app.patch('/messages/<int:id>')
def patch_message(id):
    messages_update = Message.query.where(Message.id == id).first()

    if messages_update:
        for key in request.json.keys():
            if not key == 'id':
                setattr(messages_update, key, request.json[key])

        db.session.add( messages_update )
        db.session.commit()

        return messages_update.to_dict(), 202
    else:
        return { 'error': "Not found" }, 404


@app.route('/messages/<int:id>', methods=['DELETE'])
def messages_by_id(id):
    messages = Message.query.filter(Message.id == id).first()

    if request.method == 'DELETE':
        db.session.delete(messages)
        db.session.commit()

        response_body = {
            'delete_successful': True,
            'message': 'Message deleted'
        }

        response = make_response(
            response_body,
            200
        )
        return response
    
   



if __name__ == '__main__':
    app.run(port=5555)
