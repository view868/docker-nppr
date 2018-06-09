import os

# 部署设置
from nppr.utils import AttributeDict

depc = AttributeDict({
    'name': 'test',  # 项目名称
    'deploy': '/home',  # 项目部署在服务器的目录
    'deploy_dir': '{deploy}/{name}',  # 项目部署最终目录
    'build': '',  # 构建目录 *
    'build_dir': '{build}/containers',
    'git_user': '',
    'git_pwd': '',
    'git_remote': '',
    'git_remote_url': 'https://{git_user}:{git_pwd}@{git_remote}',  # git仓库最终路径 如果是公开仓库 直接写这里
    'python_command': 'python manage.py runserver 0.0.0.0:80',
    'nginx_port': 80,
    'nginx_host': '127.0.0.1',  # ip或者域名
    'psql_database': 'db_django',
    'psql_user': 'root',
    'psql_pwd': 'root',
    'psql_port': 5432,
    'psql_cmd': 'psql "host=%s port={port} user={user} password={pwd} dbname={database}" --command "%s"'

})

SETTING_DIR = os.path.abspath(os.path.dirname(__file__))

if __name__ == '__main__':
    pass
