import subprocess
import signal

CLIENTS_QUANTITY = 2


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
        # encoding='utf-8'
    )
    print(build)
    print(command)
    return build


    # if result:
    #     return f'Client with mode: {mode} started'
    # else:
    #     return f'Something`s wrong!!!'


def main():
    clients_list = []
    # for i in range(CLIENTS_QUANTITY):
    #     clients_list.append(run_client())

    # clients_list.append(run_client('w'))
    # writer = run_client('w').communicate('echo'.encode())
    # writer.stdout
    # clients_list.append(writer)

    writer = run_client('w')

    try:
        writer.communicate('echo\ndta\n'.encode(), timeout=0)
        # writer.stdin.write('echo\ndte\n'.encode())
    except TimeoutExpired:
        writer.kill()
    # writer.stdin.write('dte\n'.encode())

    # writer.send_signal(signal.CTRL_C_EVENT)


    # for stream in clients_list:
    #     print(stream.args)
    #     print(stream.communicate())
    #     print(stream.kill())


main()
