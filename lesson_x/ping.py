import subprocess
import ipaddress
import random
try:
    from tabulate import tabulate
except ModuleNotFoundError:
    pass

NUMBER_OF_IPS = 1
IP_LENGTH = 4


def get_yandex_different_ip():

    address_list = []
    for x in range(NUMBER_OF_IPS):

        rand_address = '77.88.55.' + str(random.randint(0, 255))
        address_list.append(rand_address)
    ips_list = [ipaddress.ip_address(_).__str__() for _ in address_list]
    return ips_list


def get_address_list():
    address_list = []
    for x in range(NUMBER_OF_IPS):
        rand_val_list = [str(random.randint(0, 63)*i) for i in range(1, IP_LENGTH + 1)]
        rand_address = '.'.join(rand_val_list)
        address_list.append(rand_address)
    ips_list = [ipaddress.ip_address(_).__str__() for _ in address_list]
    return ips_list


def host_ping(ip_address_list):
    result_list = []
    result_list_modified = []

    for i in ip_address_list:
        command = 'ping ' + i
        result = bool(not subprocess.run(command, shell=True).returncode)
        if result:
            result_list_modified.append(dict(reachable=i))  # , unreachable=''))
        else:
            result_list_modified.append(dict(unreachable=i))  # , reachable=''))
        result_list.append(dict(host=i, result=result))

    return tabulate(result_list_modified, headers='keys', tablefmt='grid')
    # return tabulate(result_list, headers='keys', tablefmt='grid')


addrr_list = get_address_list()
addrr_list.append('localhost')
addrr_ya_list = get_yandex_different_ip()
addrr_ya_list.extend(['localhost', 'ya.ru', 'google.com'])
print(host_ping(addrr_ya_list))
