from db.models.users import Users, db


# 新規ユーザー登録
def create_user(user_id, user_name, password):
    # user_idで検索し、既存ユーザーがいる場合は登録しない
    if Users.query.filter_by(user_id=user_id).first():
        return None

    # ユーザ情報を設定
    new_user = Users(user_id=user_id, user_name=user_name)
    new_user.set_password(password)  # パスワードをハッシュ化して保存

    # DBに新しいユーザを追加
    db.session.add(new_user)
    db.session.commit()

    return new_user
