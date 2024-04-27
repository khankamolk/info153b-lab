from db import db

class TaskModel(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    is_completed = db.Column(db.Boolean, default=False, nullable=False)
    user_email = db.Column(db.String(100), nullable=False)