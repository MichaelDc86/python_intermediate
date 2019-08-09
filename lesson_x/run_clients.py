import subprocess
import signal
import time

CLIENTS_QUANTITY = 3


def run_client():

    command = f'fab client'
    build = subprocess.Popen(
        command,
        shell=True,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    print(build)
    print(command)
    return build


def main():
    clients_list = []
    for i in range(CLIENTS_QUANTITY):
        tmp_client = run_client()
        clients_list.append(tmp_client)
        try:
            out = tmp_client.communicate('echo\nHi!!!\n'.encode(), timeout=1)
        # out = tmp_client.communicate('echo\nHi!!!\n'.encode())[1]
            print(out)
        except subprocess.TimeoutExpired:
            print('---------------------------------------------------------------------')
            continue
        # time.sleep(1)

    for stream in clients_list:
        stream.send_signal(signal.CTRL_BREAK_EVENT)


main()
