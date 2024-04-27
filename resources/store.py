from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models import StoreModel
from schemas import StoreSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

# blue print divides data into multiple segments
blp = Blueprint("stores", __name__, description="Stores APIs")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "store deleted"}

@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()
    
    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data):
        new_store = StoreModel(**store_data)
        try:
            db.session.add(new_store)
            db.session.commit()
        except IntegrityError:
            abort(500, message="Store with that name already exists")
        except SQLAlchemyError:
            abort(500, message="Error occured while inserting item")

        return new_store, 201
