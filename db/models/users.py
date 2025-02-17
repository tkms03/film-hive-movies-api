from flask_sqlalchemy import SQLAlchemy
from db.database import db
from werkzeug.security import generate_password_hash, check_password_hash

class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String, unique=True, nullable=False)
    user_name = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String(512), nullable=False)
    # password = db.Column(db.String, nullable=False)

    # パスワードをハッシュ化して保存
    def set_password(self, password):
        self.password = generate_password_hash(password)

    # 入力されたパスワードが一致するか検証
    def check_password(self, password):
        return check_password_hash(self.password, password)
