import sys
import yaml
import zlib
from socket import socket
from argparse import ArgumentParser
import json
from datetime import datetime
import hashlib
import threading

from PyQt5.QtWidgets import (QApplication, QMainWindow, QDesktopWidget, QTextEdit,
                             QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QWidget)

from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon, QFont

from Cryptodome.Cipher import AES
from Crypto import Random

from log.client_log_config import get_logger


def int_to_bytes(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')


def int_from_bytes(xbytes: bytes) -> int:
    return int.from_bytes(xbytes, 'big')


class TypedProperty:

    def __init__(self, name):
        self.name = name
        self.args = None

    default_config = {
        'host': 'localhost',
        'port': 8000,
        'buffersize': 1024
    }

    def __get__(self, instance, cls):
        parser = ArgumentParser()

        parser.add_argument(
            '-c', '--config', type=str, required=False, help='Sets config file path'
        )
        self.args = parser.parse_args()
        if self.args.config:
            with open(self.args.config) as file:
                config_ = yaml.load(file, Loader=yaml.Loader)
                self.default_config.update(config_)

        return self.default_config.get(self.name)

    def __set__(self, instance, value):
        setattr(instance, self.name, value)

    def __delete__(self, instance):
        raise AttributeError("Невозможно удалить атрибут")


class ConfigClient:
    host = TypedProperty('host')
    port = TypedProperty('port')
    buffersize = TypedProperty('buffersize')

    @classmethod
    def get_logger_(cls):
        logger_ = get_logger()
        return logger_


class Client:

    def __init__(self):
        self.host = ConfigClient().host
        self.port = ConfigClient().port
        self.buffersize = ConfigClient().buffersize
        self.logger = ConfigClient().get_logger_()
        self.sock = None

    def __enter__(self):
        if not self.sock:
            self.sock = socket()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        message = 'Client shut down.'
        if exc_type:
            if exc_type is not KeyboardInterrupt:
                message = f'Client stopped with error {exc_type} {exc_val}!'
        self.logger.info(message)
        self.sock.close()
        return True

    def socket_bind(self):
        self.sock = socket()
        self.sock.connect(
            (self.host, self.port,)
        )
        self.logger.info(f'Client was started')

    def read(self, sock_, buffersize_):
        while True:
            try:
                compressed_response = sock_.recv(buffersize_)
                b_response = zlib.decompress(compressed_response)
                encrypted_request = json.loads(b_response)

                """decryption"""
                """create cipher"""

                key_raw = encrypted_request.get('key')
                key = int_to_bytes(key_raw)
                encode_list = encrypted_request.get('encode_list')
                encode_list = list(map(lambda x: int_to_bytes(x), encode_list))
                nonce, tag, ciphertext = [x for x in encode_list]

                cipher = AES.new(key, AES.MODE_EAX, nonce)

                """decryption part"""

                decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
                decrypted_response = encrypted_request.copy()
                try:
                    decrypted_response['data'] = decrypted_data.decode()
                    self.logger.info(f'RESPONSE: {decrypted_response}')
                    self.display_text.append(decrypted_response.get('data'))
                except TypeError:
                    self.logger.info(f'RESPONSE: empty message')
                    self.display_text.append('client sent nothing')
            except ConnectionAbortedError:
                print('here')
                client.logger.info(f'Client broke the connection.')
                break

    # def write(self, sock_):
    #     hash_obj = hashlib.sha256()
    #     hash_obj.update(
    #         str(datetime.now().timestamp()).encode()
    #     )
    #
    #     action = input('Specify action: ')
    #     id_req = None
    #     data = None
    #     if 'update' in action:
    #         id_req = input('Specify id of message to update: ')
    #         data = input('Enter data to update message:  ')
    #     elif 'delete' in action:
    #         id_req = input('Specify id of message to delete: ')
    #     else:
    #         data = input('Enter data:  ')
    #
    #     """encryption"""
    #     """create cipher"""
    #
    #     key_bytes = 16
    #     key = Random.get_random_bytes(key_bytes)
    #     key_int = int_from_bytes(key)
    #     cipher = AES.new(key, AES.MODE_EAX)
    #
    #     """encoding part"""
    #     ciphertext, tag = cipher.encrypt_and_digest(data.encode())
    #     encode_list = [x for x in (cipher.nonce, tag, ciphertext)]
    #     encode_list = list(map(lambda x: int_from_bytes(x), encode_list))
    #
    #     request = {
    #         'encode_list': encode_list,
    #         'key': key_int,
    #         'id_req': id_req,
    #         # 'data': encrypted_data,
    #         'time': datetime.now().timestamp(),
    #         'action': action,
    #         'token': hash_obj.hexdigest(),
    #     }
    #
    #     s_request = json.dumps(request)
    #     request_compressed = zlib.compress(s_request.encode())
    #     sock_.send(request_compressed)
    #     self.logger.debug(f'Client sent data: {data}')

    """write for PyQt"""
    def write(self):
        hash_obj = hashlib.sha256()
        hash_obj.update(
            str(datetime.now().timestamp()).encode()
        )

        action = 'echo'
        id_req = None
        data = self.enter_text.toPlainText()

        """encryption"""
        """create cipher"""

        key_bytes = 16
        key = Random.get_random_bytes(key_bytes)
        key_int = int_from_bytes(key)
        cipher = AES.new(key, AES.MODE_EAX)

        """encoding part"""
        ciphertext, tag = cipher.encrypt_and_digest(data.encode())
        encode_list = [x for x in (cipher.nonce, tag, ciphertext)]
        encode_list = list(map(lambda x: int_from_bytes(x), encode_list))

        request = {
            'encode_list': encode_list,
            'key': key_int,
            'id_req': id_req,
            'time': datetime.now().timestamp(),
            'action': action,
            'token': hash_obj.hexdigest(),
        }

        s_request = json.dumps(request)
        request_compressed = zlib.compress(s_request.encode())
        self.enter_text.clear()
        print(type(self.sock))
        self.sock.send(request_compressed)
        self.logger.debug(f'Client sent data: {data}')

    def render(self):
        app = QApplication(sys.argv)
        window = QMainWindow()
        window.setGeometry(400, 600, 400, 600)

        central_widget = QWidget()

        self.display_text = QTextEdit()
        self.display_text.setReadOnly(True)
        self.enter_text = QTextEdit()
        self.send_button = QPushButton('Send', window)
        self.enter_text.setMaximumHeight(64)
        self.send_button.setMaximumHeight(64)

        base_layout = QVBoxLayout()

        top_layout = QHBoxLayout()
        footer_layout = QHBoxLayout()
        top_layout.addWidget(self.display_text)
        footer_layout.addWidget(self.enter_text)
        footer_layout.addWidget(self.send_button)
        base_layout.addLayout(top_layout)
        base_layout.addLayout(footer_layout)

        central_widget.setLayout(base_layout)
        window.setCentralWidget(central_widget)

        """actions with text"""

        def actionBold():
            myFont = QFont()
            myFont.setBold(True)
            self.enter_text.setFont(myFont)

        def actionItalic():
            myFont = QFont()
            myFont.setItalic(True)
            self.enter_text.setFont(myFont)

        def actionUnderlined():
            myFont = QFont()
            myFont.setUnderline(True)
            self.enter_text.setFont(myFont)

        our_bold = QAction(QIcon('pyqt_examples/b.jpg'), 'Bold', window)
        our_bold.triggered.connect(actionBold)

        our_italic = QAction(QIcon('pyqt_examples/i.jpg'), 'Italic', window)
        our_italic.triggered.connect(actionItalic)

        our_underlined = QAction(QIcon('pyqt_examples/u.jpg'), 'Underlined', window)
        our_underlined.triggered.connect(actionUnderlined)

        # smiles

        def actionSmile():
            url = 'pyqt_examples/1lesson_source/Smile/ab.gif'
            self.enter_text.setHtml('<img src="%s" />' % url)

        def actionMelancholy():
            url = 'pyqt_examples/1lesson_source/Smile/ac.gif'
            self.enter_text.setHtml('<img src="%s" />' % url)

        def actionSurprise():
            url = 'pyqt_examples/1lesson_source/Smile/ai.gif'
            self.enter_text.setHtml('<img src="%s" />' % url)

        smile = QAction(QIcon('pyqt_examples/1lesson_source/Smile/ab.gif'), 'Smile', window)
        smile.triggered.connect(actionSmile)

        melancholy = QAction(QIcon('pyqt_examples/1lesson_source/Smile/ac.gif'), 'Melancholy', window)
        melancholy.triggered.connect(actionMelancholy)

        surprise = QAction(QIcon('pyqt_examples/1lesson_source/Smile/ai.gif'), 'Surprise', window)
        surprise.triggered.connect(actionSurprise)

        # ------------------------------------------------

        tool_b = window.addToolBar('Formatting')
        tool_b.addAction(our_bold)
        tool_b.addAction(our_italic)
        tool_b.addAction(our_underlined)
        tool_b.addAction(smile)
        tool_b.addAction(melancholy)
        tool_b.addAction(surprise)


        dsk_widget = QDesktopWidget()
        geometry = dsk_widget.availableGeometry()
        center_position = geometry.center()
        frame_geometry = window.frameGeometry()
        frame_geometry.moveCenter(center_position)
        window.move(frame_geometry.topLeft())

        self.send_button.clicked.connect(self.write)

        window.show()
        sys.exit(app.exec_())

    def read_write(self):
        read_thread = threading.Thread(
            target=self.read,
            args=(
                self.sock,
                self.buffersize
            )
        )

        read_thread.start()

        # while True:
        #     self.write(self.sock)
        self.render()


"""left this commented lines for myself(another solution)"""

# client = Client()
# client.socket_bind()
#
# try:
#     client.read_write()
#
# except KeyboardInterrupt:
#     client.sock.close()
#     client.logger.info(f'Client shutdown.')

"""solution with context manager(added __enter__ and __exit__ to Client)"""

with Client() as client:
    client.socket_bind()
    client.read_write()
