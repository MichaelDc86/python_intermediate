import subprocess
import signal
import time
import psutil
import os

CLIENTS_QUANTITY = 7


def run_client(mode='r'):

    # command = ['fab client:', mode]
    command = f'fab client:{mode}'
    build = subprocess.Popen(
        command,
        shell=True,
        # creationflags=CREATE_NEW_CONSOLE,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
        # encoding='utf-8'
    )
    print(build)
    print(command)
    return build


def main():
    clients_list = []
    for i in range(CLIENTS_QUANTITY):
        r_client = run_client()
        clients_list.append(r_client)

    time.sleep(1)
    writer = run_client('w')
    # clients_list.append(writer)
    out = writer.communicate('echo\nHi!!!\n'.encode())[1]
    # writer.stdin.write('server_time\nOPA!!!\n'.encode())
    # writer.stdin.write('echo\nHi!!!\n'.encode())
    # writer.send_signal(signal.CTRL_BREAK_EVENT)
    # outs = writer.communicate('server_time\nOPA!!!\n'.encode())[1]
    # writer.send_signal(signal.CTRL_C_EVENT)
    # writer.send_signal(signal.CTRL_BREAK_EVENT)

    print(out)
    print('---------------------------------------------------------------------')
    # print(outs)

    for stream in clients_list:
        stream.send_signal(signal.CTRL_BREAK_EVENT)


main()
