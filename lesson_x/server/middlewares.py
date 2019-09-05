import zlib
import json
import hmac
from functools import wraps
from protocol import make_response
from Cryptodome.Cipher import AES
from Crypto import Random
from database import Session
from auth.models import User


def int_to_bytes(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')


def int_from_bytes(xbytes: bytes) -> int:
    return int.from_bytes(xbytes, 'big')


def compression_middleware(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        b_request = zlib.decompress(request)
        b_response = func(b_request, *args, **kwargs)
        return zlib.compress(b_response)
    return wrapper


def encryption_middleware(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):

        encrypted_request = json.loads(request)
        """creating cipher"""

        key_bytes = 16
        key_send = Random.get_random_bytes(key_bytes)

        key_read_int = encrypted_request.get('key')
        key_read = int_to_bytes(key_read_int)

        encode_list = encrypted_request.get('encode_list')
        encode_list = list(map(lambda x: int_to_bytes(x), encode_list))
        nonce, tag, ciphertext = [x for x in encode_list]

        cipher_send = AES.new(key_send, AES.MODE_EAX)
        cipher_read = AES.new(key_read, AES.MODE_EAX, nonce)

        """decryption part"""

        decrypted_data = cipher_read.decrypt_and_verify(ciphertext, tag)
        decrypted_request = encrypted_request.copy()
        decrypted_request['data'] = decrypted_data.decode()
        bytes_request = json.dumps(decrypted_request).encode()

        b_response = func(bytes_request, *args, **kwargs)

        """encryption part"""

        decrypted_response = json.loads(b_response)
        decrypted_data = json.dumps(decrypted_response.get('data'))

        ciphertext, tag = cipher_send.encrypt_and_digest(decrypted_data.encode())
        encrypted_response = decrypted_response.copy()
        encode_list = [x for x in (cipher_send.nonce, tag, ciphertext)]
        encode_list = list(map(lambda x: int_from_bytes(x), encode_list))
        encrypted_response['key'] = int_from_bytes(key_send)
        encrypted_response['encode_list'] = encode_list

        try:
            return json.dumps(encrypted_response, ensure_ascii=False).encode()
        except Exception as err:
            print(err)

    return wrapper


def auth_middleware(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):

        authenticated = True

        request_obj = json.loads(request)
        login = request_obj.get('login')
        time = request_obj.get('time')
        token = request_obj.get('token')

        session = Session()
        user = session.query(User).filter_by(name=login).first()

        if user:
            digest = hmac.new(time, user.password)

            if hmac.compare_digest(digest, token):
                authenticated = False
        else:
            authenticated = False

        if authenticated:
            func(*args, **kwargs)
        response = make_response(request, 401, 'Access denied!')
        return json.dumps(response)

    return wrapper
