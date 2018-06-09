from fabric.state import env
from nppr.tasks import *

env.hosts = [
    'root@ip',  # 这里是服务器IP
]
env.passwords = {
    'root@ip:22': 'ssh password',  # 和上面服务器对应的密码 注意带上端口号
}

TESTS_DIR = os.path.abspath(os.path.dirname(__file__))

depc.build = TESTS_DIR
# depc.git_user = 'git账户'
# depc.git_pwd = 'git密码'
# depc.git_remote = 'git仓库路径'
depc.git_remote_url = 'https://github.com/view868/docker-nppr'
depc.python_command = 'python manage.py runserver 0.0.0.0:80'
depc.nginx_port = 80
depc.nginx_hosw = 'www.google.com'
