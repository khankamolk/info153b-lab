from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from db import db
from schemas import ItemSchema, ItemUpdateSchema
from models import ItemModel

# blue print divides data into multiple segments
blp = Blueprint("items", __name__, description="Items APIs")

@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item 
    
    def delete(self, item_id):
        item  = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "item deleted"}

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(id="item_id", **item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Error occured while updating item")


@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True)) # returns a list of ItemSchemas
    def get(self):
        return ItemModel.query.all()

    @blp.arguments(ItemSchema)
    @blp.response(200, ItemSchema)
    def post(self, item_data):
        # uniqueness of name and item already checked in the models, so we dont have to check here. 
        item = ItemModel(**item_data) # converts dictionary to keyword arguments

        # save it to db
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Error occured while inserting item")

        return item, 201
