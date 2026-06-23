from flask_restful import Api, Resource
from flask import request

api=api()

from models import db, User 

class LoginResource(Resource):
    def post (self):
        data=request.get_json()
        if not data or not data.get('email') or not data.get('password'):
            return{"message": "Please provide email and password!"}, 400
        user = User.query.filter_by(email=data['email']).first()
        if not user or user.password != data['password']:
            return{"message": "Invalid email or password"},401
        return{"message" : "loged in succesfully"}
api.add_resource(LoginResource,'/login')


class ItemResource(Resource):
    def get(self, item_id=None):
        if item_id:
            item = Item.query.get(item_id)
            if not item:
                return {"message": f"Item with id {item_id} not found!"}, 404
            return {"message": f"Item {item_id} returned!", "item": {"id": item.id, "name": item.name, "description": item.description, "image_url": item.image_url}}
        items = [{"id": item.id, "name": item.name, "description": item.description, "image_url": item.image_url} for item in Item.query.all()]
        return {"message": f"All items returned!", "items": items}
    def post(self, item_id=None):
        if item_id:
            return {"message": "Item id is not required for creation of new items!"}, 400
        data = request.get_json()
        if not data or not data.get('name'):
            return {"message": "Please provide required fields!"}, 400
        item = Item(name=data['name'], description=data.get('description'), image_url=data.get('image_url'))
        db.session.add(item)
        db.session.commit()
        return {"message": f"Item created successfully!", "item": {"id": item.id, "name": item.name, "description": item.description, "image_url": item.image_url}}, 201
    def put(self, item_id):
        item = Item.query.get(item_id)
        if not item:
            return {"message": f"Item with id {item_id} not found!"}, 404
        data = request.get_json()
        if not data or not data.get('name'):
            return {"message": "Please provide required fields!"}, 400
        item.name = data['name']
        item.description = data.get('description')
        item.image_url = data.get('image_url')
        db.session.commit()
        return {"message": f"Successfully updated item {item_id}!", "item": {"id": item.id, "name": item.name, "description": item.description, "image_url": item.image_url}}
    def delete(self, item_id):
        item = Item.query.get(item_id)
        if not item:
            return {"message": f"Item with id {item_id} not found!"}, 404
        db.session.delete(item)
        db.session.commit()
        return {"message": f"Successfully deleted item {item_id}!"}
api.add_resource(ItemResource, '/items', '/items/<int:item_id>')
