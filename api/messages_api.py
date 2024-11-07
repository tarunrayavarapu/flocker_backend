# by P5 G1
from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource
# from api.jwt_authorize import token_required

# Create a Blueprint for the messages API
messages_api = Blueprint('messages_api', __name__, url_prefix='/api')
api = Api(messages_api)

# path for the messages file
MESSAGE_FILE_PATH = 'Period-5/aaak/messages.txt'  

class MessagesAPI:

    # Define the API CRUD endpoints for the messages file.


    class _Messages(Resource):
        def get(self):

            #Retrieve all messages without authentication.

            try:
                with open(MESSAGE_FILE_PATH, 'r') as file:
                    messages = file.readlines()
                # Return messages as a JSON array
                return jsonify({'messages': [msg.strip() for msg in messages]})
            except FileNotFoundError:
                return jsonify({'message': 'Messages file not found.'}), 404

        def post(self):

            # Append a new message to the messages file.

            data = request.get_json()
            message = data.get('message')
            if not message:
                return {'message': 'Message content is required.'}, 400
            try:
                with open(MESSAGE_FILE_PATH, 'a') as file:
                    file.write(f"{message}\n")
                return jsonify({'message': 'Message added successfully'}), 201
            except Exception as e:
                return {'message': f'Failed to add message: {str(e)}'}, 500

        def delete(self):

            # Clear all messages from the messages file.

            try:
                with open(MESSAGE_FILE_PATH, 'w') as file:
                    file.write("")  # Clear the file
                return jsonify({'message': 'All messages deleted successfully'}), 200
            except Exception as e:
                return {'message': f'Failed to delete messages: {str(e)}'}, 500

    # make link for /messages.
    api.add_resource(_Messages, '/messages')
