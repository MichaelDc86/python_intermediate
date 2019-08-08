import subprocess
import signal
import psutil

CLIENTS_QUANTITY = 2


def run_client(mode='r'):

    # command = ['fab client:', mode]
    command = f'fab client:{mode}'
    build = subprocess.Popen(
        command,
        shell=True,
        # shell=False,
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
        clients_list.append(run_client())

    writer = run_client('w')
    clients_list.append(writer)
    out = writer.communicate('echo\nHi!!!\n'.encode())[0]
    # out = writer.communicate('server_time\nHallo!!!\n'.encode())[0]
    # out = writer.stdin.write('echo\ndte\n'.encode())
    # writer.send_signal(signal.CTRL_C_EVENT)
    # writer.send_signal(signal.CTRL_BREAK_EVENT)

    print(out)

    for stream in clients_list:
        # outs, errs = stream.communicate()
        # stream.kill()
        # subprocess.Popen("TASKKILL /F /PID {pid} /T".format(pid=stream.pid))
        # outs = stream.communicate('\n'.encode())[0]
        # print(outs)
        print(stream.terminate())
        # stream.send_signal(signal.CTRL_C_EVENT)
        # outs = stream.communicate()[0]


main()
