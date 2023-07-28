from flask import Flask, request, make_response, jsonify 
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api , Resource

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

# GET /messages: returns an array of all messages as JSON, ordered by created_at in ascending order.
class Messages(Resource):
    def get(self):
        messages = Message.query.order_by(Message.created_at).all()

        message_list =[]
        for message in messages:
            message_dict = {
                "id": message.id,
                "body": message.body,
                "username": message.username,
                "created_at": message.created_at
            }
            message_list.append(message_dict)
        response = make_response(message_list, 200)
        return response
    
# POST /messages: creates a new message with a body and username from params, and returns the newly created post as JSON.
    def post(self):
        # taking the request and turing it into something we can work on in python
        data = request.get_json() 
        message = Message(
            body = data["body"],
            username = data ["username"]
        )
        db.session.add(message)
        db.session.commit()

        response_dict = {
            "id": message.id,
            "body": message.body,
            "username": message.username,
            "created_at": message.created_at
        }
        response = make_response(jsonify(response_dict) , 201 )
        return response
api.add_resource(Messages, "/messages")


# PATCH /messages/<int:id>: updates the body of the message using params, and returns the updated message as JSON.
class Messages_by_id(Resource):
    def patch(self, id):
        message = Message.query.filter(Message.id == id).first()
        data = request.get_json()
        for attr in data:
            setattr(message, attr, data[attr])
        
        db.session.commit()
        response_dict = message.to_dict()
        response = make_response(response_dict, 200)
        return response

# DELETE /messages/<int:id>: deletes the message from the database.
    def delete(self, id):
        message = Message.query.filter(Message.id == id).first()
        db.session.delete(message)
        db.session.commit()
        response_dict = {
            "message": f'You have deleted {id}'
        }
        response = make_response(response_dict , 200)
        return response
api.add_resource(Messages_by_id, "/messages/<int:id>")


# @app.route('/messages')
# def messages():
#     return ''

# @app.route('/messages/<int:id>')
# def messages_by_id(id):
#     return ''

if __name__ == '__main__':
    app.run(port=4000 , debug = True)
