import hmac
import hashlib
from database import session_scope

from .settings import SECRET_KEY
from .models import User, Session


def authenticate(login, password):
    with session_scope() as db_session:
        user = db_session.query(User).filter_by(name=login).first()
        hmac_obj = hmac.new(SECRET_KEY, password)
        password_digest = hmac_obj.digest()

        if user and hmac.compare_digest(password_digest, user.password):
            return user


def login(request, user):
    with session_scope() as db_session:
        hash_obj = hashlib.sha256()
        hash_obj.update(SECRET_KEY.encode())
        hash_obj.update(str(request.get('time').encode()))
        token = hash_obj.hexdigest()
        user_session = Session(user=user, token=token)
        db_session.add(user_session)
        return token