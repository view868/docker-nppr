### 介绍
使用Docker创建Nginx+Django+Postgresql+Redis快速创建部署环境 

### 安装
pip install nppr


### 使用
在项目根目录创建fab.py文件 内容参照examples.py

部署项目

执行 fab deploy

更新项目

执行 fab update


### 配置项
name 项目名称 默认：test

deploy 部署目录 默认：/home

build 本地构建目录(一般情况下使用 os.path.abspath(os.path.dirname(__file__))) *

git_user git账户 @符号用%40代替

git_pwd git密码

git_remote git仓库路径 不要http://

git_remote_url git最终路径 如果是公开的项目 git_user/git_pwd/git_remote不用设置

python_command python容器启动命令 默认：python manage.py runserver 0.0.0.0:80

nginx_port nginx监听端口 默认：80

nginx_host nginx主机 一般为域名或主机IP 默认：127.0.0.1 *

psql_database 默认：db_django

psql_user 默认：root

psql_pwd 默认：root

psql_port 默认：5432

### hosts
postgresql->postgres

redis->redis

### tasks
get_cid 获取容器ID

get_cip 获取容器IP

docker_install 安装 docker/docker-compose/postgresql/git

docker_clean 删除docker容器和镜像

docker_create 构建容器

config_build 构建配置文件（本地）

config_upload 上传配置文件

config_update 等于config_build+config_upload

deploy 部署项目 等于docker_install+config_update+docker_create

update 更新项目

restart 重启服务