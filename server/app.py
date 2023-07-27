from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Message
import ipdb
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


class Messages(Resource):
    def get(self):
        messages = Message.query.all()
        messages_list = []
        for message in messages:
            message_dict = message.to_dict()
            messages_list.append(message_dict)
        response = make_response(jsonify(messages_list), 200)
        return response

    def post(self):
        data = request.get_json()
        message = Message(
            body = data['body'],
            username = data['username']
        )
        db.session.add(message)
        db.session.commit()

        response_dict = message.to_dict()
        response = make_response(jsonify(response_dict), 200)
        return response   
api.add_resource(Messages, '/messages')



class Messages_by_id(Resource):
    def patch(self, id):
        message = Message.query.filter(Message.id == id).first()
        data = request.get_json()
        for attr in data:
            setattr(message, attr, data[attr])
        db.session.commit()
        response_dict = message.to_dict()
        response = make_response(jsonify(response_dict), 200)
        return response
    
    def delete(self, id):
        message = Message.query.filter(Message.id == id).first()
        db.session.delete(message)
        db.session.commit()

        response_dict = {f'message': "Message from {message.username} deleted!"}

api.add_resource(Messages_by_id, '/messages/<int:id>')

if __name__ == '__main__':
    app.run(port=4000, debug=True)
