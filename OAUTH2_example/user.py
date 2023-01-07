from flask_login import UserMixin


class UserDB:

    users = {}

    @classmethod
    def add(cls, user):
        cls.users.update({user.id: user})
        return user

    @classmethod
    def get(cls, id_=None, username=None):
        return cls.users.get(id_) if id_ \
            else [user for user in cls.users.values() if user.username == username][0]


class User(UserMixin):

    def __init__(self, id_, name, username, email, profile_pic):
        self.id = id_
        self.name = name
        self.username = username
        self.email = email
        self.profile_pic = profile_pic

    @classmethod
    def get(cls, id_):
        return UserDB.get(id_=id_)

    @classmethod
    def get_public_by_username(cls, username):
        user = UserDB.get(username=username)
        return User('', '', user.username, '', user.profile_pic)

    @classmethod
    def create(cls, id_, name, email, profile_pic):
        username = str.join('_', name.lower().split(' '))
        user = User(id_, name, username, email, profile_pic)
        return UserDB.add(user)


