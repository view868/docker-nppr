import platform
import re

import os
import shutil

import yaml
from fabric.context_managers import settings, cd, lcd
from fabric.contrib.console import confirm
from fabric.contrib.files import exists
from fabric.decorators import task
from fabric.operations import run, local, put

from nppr.settings import dep

TASKS_DIR = os.path.abspath(os.path.dirname(__file__))
CONTAINERS_DIR = os.path.abspath(os.path.dirname(__file__)) + '/containers'


@task()
def get_cid(name='python'):
    """
    获取服务器容器ID
    :param name: 容器包含的名称 例如python、nginx
    :return: xxx_python_xxx 为django运行容器
    """
    cid = None
    containers = run('docker inspect --format="{{.ID}}{{.Name}}" `docker ps -q`')
    for item in containers.splitlines():
        if name in item:
            cid = item[0:5]
    if not cid:
        raise Exception('找不到对应的容器！请检查容器是否存在或容器名称是否正确')
    return cid


@task()
def get_cip(name='python'):
    """
    获取服务器容器IP
    :param name: 容器包含的名称 例如python、nginx
    :return: xxx_python_xxx 为django运行容器
    """
    cid = get_cid(name=name)
    cip = None
    if cid:
        rs_ps = run('docker inspect "%s"|grep IPAddress' % cid)
        # 正则表达式提取IP
        regip = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')
        cip = regip.findall(rs_ps)[0]
    if not cid:
        raise Exception('找不到容器IP!请检查容器是否成功启动')
    return cip


@task()
def docker_install():
    """
    安装必要软件 docker docker-compose postgredql git
    :return:
    """
    #
    with settings(warn_only=True):
        print('安装docker...')
        run('curl -sSL https://get.docker.com/ | sh ')
        #
        print('安装docker-compose...')
        cmd = ''.join(['sudo curl -L',
                       ' https://github.com/docker/compose/releases/download/1.19.0/',
                       'docker-compose-`uname -s`-`uname -m`',
                       ' -o /usr/local/bin/docker-compose'])
        run(cmd)
        run('chmod +x /usr/local/bin/docker-compose')
        print('安装postgresql...')
        run('sudo apt install -y postgresql')
        print('安装git...')
        run('sudo apt install -y git')


@task()
def docker_clean(level=1):
    """
    清理docker的容器和镜像
    :return:
    """
    with settings(warn_only=True):
        print('停止所有container...')
        run('docker stop $(docker ps -a -q)')
        print('删除所有container...')
        run('docker rm $(docker ps -a -q)')
        if level == 2:
            print('删除所有images...')
            run('docker rmi $(docker images -q)')
            print('删除同ID的镜像(如果有)')
            images = run('docker images --format="{{.Repository}}" ')
            for item in images.splitlines():
                run('docker rmi %s' % item)


@task()
def config_build():
    """
    构建配置文件
    :return:
    """
    # 复制文件到build目录
    if not os.path.exists(dep.build_dir):
        print('复制构建文件...')
        shutil.copytree(CONTAINERS_DIR, dep.build_dist, symlinks=True, ignore=shutil.ignore_patterns('*.py'))
    print('构建/docker-compose.yaml文件...')
    with open(CONTAINERS_DIR + '/docker-compose.yml', 'r') as fr:
        temp = yaml.load(fr.read())
        if 'postgres' in temp['services'].keys():
            temp['services']['postgres']['expose'] = [str(dep.psql_port)]
            temp['services']['postgres']['environment']['POSTGRES_DB'] = dep.psql_database
            temp['services']['postgres']['environment']['POSTGRES_USER'] = dep.psql_user
            temp['services']['postgres']['environment']['POSTGRES_PASSWORD'] = dep.psql_pwd
        if 'nginx' in temp['services'].keys():
            temp['services']['nginx']['environment']['NGINX_PORT'] = dep.nginx_port
            temp['services']['nginx']['environment']['NGINX_HOST'] = dep.nginx_host
        # 重新命名容器名称=项目名称_环境名称
        for item in temp['services']:
            container_name = temp['services'][item]['container_name']
            temp['services'][item]['container_name'] = dep.name + '_' + container_name
        with open(dep.build_dir + '/docker-compose.yml', 'w') as fw:
            yaml.dump(temp, stream=fw)


@task()
def config_upload():
    """
    上传dockerfile和相关配置文件
    :return:

    """
    if not exists(dep.deploy_dir):
        print('创建远程目录...')
        run('mkdir -p %s' % dep.deploy_dir)
    print('打包文件...')
    tar_name = 'containers.tar.gz'
    with lcd(dep.build):
        local('tar -zcvf %s containers' % tar_name)
        print('上传压缩文件...')
        with settings(warn_only=True):
            result = put(dep.build + '/%s' % tar_name, dep.deploy_dir + '/%s' % tar_name)
            print('删除本地文件...')
            local('rm %s' % tar_name)
        if result.failed and not confirm("put file failed, Continue[Y/N]?"):
            os.abort("上传文件失败")
    with cd(dep.deploy_dir):
        print('解压远程文件...')
        run('tar -xzvf %s' % tar_name)
        print('删除远程文件...')
        run('rm %s' % tar_name)


@task()
def container_build():
    """
    初始化项目
    :return:
    """
    if not exists(dep.remote_dir + '/python/data/.git'):
        with cd(dep.remote_dir + '/python'):
            print('开始克隆项目...')
            run('git clone ' + dep.git_remote_url + ' data')
    with cd(dep.remote_dir):
        print('开始构建Docker容器...')
        run('docker-compose up -d')
        #
        cid = get_cid()
        print('更新pip...')
        run('docker exec %s pip install --upgrade pip' % cid)
        print('安装新的包...')
        run('docker exec %s pip install -r /www/requirements.txt' % cid)
        print('收集静态文件...')
        run('docker exec %s python manage.py collectstatic' % cid)
        print('生成数据库语句...')
        run('docker exec %s python manage.py makemigrations' % cid)
        print('同步数据结构...')
        run('docker exec %s python manage.py migrate' % cid)
        print('载入数据...')
        run('docker exec %s python manage.py loaddata fixtures/all.json' % cid)
        print('重启容器...')
        run('docker-compose restart')


@task()
def deploy():
    """
    部署
    :return:
    """
    docker_install()
    config_build()
    config_upload()
    container_build()
    print('部署完成！')


@task()
def update():
    """
    更新python
    :return:
    """
    with cd(dep.remote_dir + '/python'):
        print('获取git更新...')
        run('git pull')
        cid = get_cid()
        print('安装新的包...')
        run('docker exec %s pip install -r /www/requirements.txt' % cid)
        print('生成数据库语句...')
        run('docker exec %s python manage.py makemigrations' % cid)
        print('同步数据结构...')
        run('docker exec %s python manage.py migrate' % cid)
        print('载入数据...')
        run('docker exec %s python manage.py loaddata fixtures/all.json' % cid)
    with cd(dep.remote_dir):
        print('重启容器...')
        run('docker-compose restart')