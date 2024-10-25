import jwt
from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
from __init__ import app
from api.jwt_authorize import token_required
from model.post import Post

post_api = Blueprint('post_api', __name__,
                   url_prefix='/api')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(post_api)

class PostAPI: 
    
    class _CRUD(Resource):
        @token_required()
        def post(self):
            # obtain the current user from the global context
            current_user = g.current_user
            # obtain the request data
            data = request.get_json()
            # create a new post
            post = Post(data['title'], data['content'], current_user.id, data['group_id'])
            # save the post
            post.create()
            # return response
            return jsonify(post.read())

        @token_required()
        def get(self):
            # obtain the current user from the global context
            current_user = g.current_user
            # find all posts by the current user
            posts = Post.query.filter(Post._user_id == current_user.id).all()            
            # prepare a json list of user dictionaries
            json_ready = []
            for post in posts:
                post_data = post.read()
                json_ready.append(post_data)
            
            # return response, a json list of user dictionaries
            return jsonify(json_ready)
        
        @token_required()
        def put(self):
            # obtain the current user from the global context
            current_user = g.current_user
            # obtain the request data
            data = request.get_json()
            # find the post to update
            post = Post.query.get(data['id'])
            # update the post
            post._title = data['title']
            post._content = data['content']
            post._group_id = data['group_id']
            # save the post
            post.update()
            # return response
            return jsonify(post.read())
        
        @token_required()
        def delete(self):
            # obtain the current user from the global context
            current_user = g.current_user
            # obtain the request data
            data = request.get_json()
            # find the post to delete
            post = Post.query.get(data['id'])
            # delete the post
            post.delete()
            # return response
            return jsonify({"message": "Post deleted"})
            
    api.add_resource(_CRUD, '/post')