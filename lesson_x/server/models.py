class Client:
    def __init__(self, login, information):
        self.login = login
        self.information = information

    def __str__(self):
        return self.login


class ClientHistory:
    def __init__(self, enter_time, ip_address):
        self.enter_time = enter_time
        self.ip_address = ip_address

    def __str__(self):
        return self.ip_address


class Contacts:
    def __init__(self, id_owner, id_client):
        self.id_owner = id_owner
        self.id_client = id_client

    def __str__(self):
        return self.id_owner
