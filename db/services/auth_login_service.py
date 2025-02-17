from db.models.users import Users, db
from flask_jwt_extended import create_access_token

# ユーザー認証（DBから検索）
def authenticate(user_id, password):
    # user_idで検索
    user = Users.query.filter_by(user_id=user_id).first()
    
    # user_idが存在、かつパスワードが一致する場合
    if user and user.check_password(password):
        return user
    return None

def generate_token(user):
    """ JWTトークンを生成 """
    return create_access_token(identity=user.user_id)
