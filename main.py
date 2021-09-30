#!/usr/bin/env python3
import argparse
import libtmux
import tqdm
import uuid
import os
import binascii


def start(num_users, base_dir='./'):
    """
    Запустить $num_users ноутбуков. У каждого рабочай директория $base_dir+$folder_num
    """
    server = libtmux.Server()
    session_name = 'jupyter_notebooks_session'
    ip='localhost'
    port = 10660

    # create clear session
    session = server.new_session(session_name, kill_session=True)
    
    print('session_name:', session_name)

    # create windows
    base_dir = os.path.abspath(base_dir)
    for i in tqdm.tqdm(range(num_users)):
        # token = uuid.uuid4()
        token = binascii.b2a_hex(os.urandom(24)).decode("utf-8")
        notebook_dir = os.path.join(base_dir, session_name+str(i))
        if not os.path.isdir(notebook_dir):
            os.mkdir(notebook_dir)

        cmd = 'jupyter notebook --ip {0} --port {1} '\
            '--NotebookApp.token={2} --NotebookApp.notebook_dir={3}'.format(ip, port+i, token, notebook_dir)
        w = session.new_window(attach=False, window_name=str(i),\
                            window_shell=cmd)


def stop(session_name, num):
    """
    @:param session_name: Названия tmux-сессии, в которой запущены окружения
    @:param num: номер окружения, кот. можно убить
    """
    server = libtmux.Server()
    session = server.find_where({ "session_name": session_name })
    if session is None:
        print('Session', session_name, 'not found')
        return

    try:
        session.kill_window(num)
    except Exception:
        print('window was not found')
        return
    print('OK!')


def stop_all(session_name):
    """
    @:param session_name: Названия tmux-сессии, в которой запущены окружения
    """
    server = libtmux.Server()
    session = server.find_where({ "session_name": session_name })
    if session is None:
        print('Session', session_name, 'not found')
        return

    for window in session.list_windows():
        window.kill_window()
    
    print('OK!')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["start", "stop"], help="action type")

    args, rem_args = parser.parse_known_args()

    if args.action == "start":
        parser.add_argument('--num-users', required=True, type=int, help='Count of notebooks')
        parser.add_argument('--base-dir', default='./', type=str, help='Base path for notebooks')
    else:
        parser.add_argument('--session-name', required=True, type=str, help='tmux-session name')
        parser.add_argument('--num', required=False, help='session number')

    parser.parse_args(namespace=args)
    return args


def main():
    args = parse_args()

    func = {
        "start": lambda args: start(args.num_users, args.base_dir),
        "stop": lambda args: stop(args.session_name, args.num) if args.num is not None \
                        else stop_all(args.session_name)
    }

    func[args.action](args)


if __name__ == '__main__':
    main()
