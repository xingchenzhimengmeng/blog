# 部署笔记

### 一、本机操作

首先保证Django项目在自己电脑上能够用虚拟环境运行。

创建虚拟环境venv

```shell
#安装虚拟环境包
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple virtualenv virtualenvwrapper-win
workon		# 找所有虚拟环境
mkvirtualenv venv		# 创建虚拟环境
workon venv	# 进入虚拟环境
# 在虚拟环境安装好项目需要的第三方库。
```

##### 1 导出第三方模块

```shell
pip freeze > requirements.txt
```

##### 2 收集静态资源

如果DEBUG=True，那么django完成静态资源的分发

项目上线，DEBUG一定要改为False。使用nginx做静态文件转发。

setting.py配置

```python
import os
STATIC_URL = 'static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'app01', 'static'),
    os.path.join(BASE_DIR, 'ys', 'static'),
    os.path.join(BASE_DIR, 'play', 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')  # 收集的静态文件位置
```

收集命令

```shell
python manage.py collectstatic
```

##### 3 配置uwsgi

在项目根目录创建uwsgi.ini文件。文件内容如下：

```ini
[uwsgi]
# 开启主进程
master = true
# 指定uwsgi工作的进程数
processes = 1
# 指定工作的每个进程下的线程数
threads = 2
# 在服务器上时，项目的根目录位置
chdir = /home/blog	
# wsgi.py文件的位置,setting.py文件同级目录的该文件
wsgi-file= %(chdir)/item/wsgi.py
# 使用nginx这里就要用socket
socket = 127.0.0.1:8000
# 日志  需要去创建这个文件
logto = %(chdir)/logs/error.log
chmod-socket = 660
vacuum = true
max-requests = 1000
# uwsgi的运行状态
stats=%(chdir)/uwsgi.status
# uwsgi的进程id
pidfile=%(chdir)/uwsgi.pid
```

创建logs文件夹，在其中创建error.log文件。

##### 4 配置nginx

在项目根目录创建nginx.conf文件，文件内容如下：

```shell
# nginx配置

server {
    listen   80;
    server_name 120.79.36.136;      # 部署网站域名或ip
    location / {
        uwsgi_pass   127.0.0.1:8000;  # uwsgi运行的主机和端口，
        include uwsgi_params;
    }
    location /static{
      alias  /home/blog/static;  # 你收集的静态文件的位置，由nginx管理转发所有静态文件
    }
}
```

重启nginx命令

```shell
nginx -s reload
```

##### 5 通过git克隆代码

把整个项目上传到gitee或github，不用上传虚拟环境venv文件夹。注意：项目里面包含了requirements.txt,nginx.conf,uwsgi.ini这些文件。

### 二、服务器操作

##### 1 服务器需要安装的软件

mysql和python的版本应当与电脑上保持一致。非常重要！

需要安装的软件如下：

```
git  
mysql #version8.0
nginx
python3 #3.10
```

查看软件版本命令

```shell
mysql -V
python3 -V
```

##### 2 通过git克隆代码到服务器

```shell
# 进入/home目录
cd /home
# 克隆
git clone http... # 你的项目地址
# 进入项目根目录
cd ./blog
```

##### 3 创建项目的虚拟环境

```shell
# 安装虚拟环境的第三方包 virtualenv
pip3 install virtualenv

# 创建虚拟环境（虚拟环境一般放在项目根目录下）
virtualenv venv

# 进入虚拟环境
source venv/bin/activate

# 退出虚拟环境
deactivate
```

安装好了之后，进入虚拟环境。

##### 4 安装第三方库

```shell
# 安装项目在电脑运行所需所有第三方库。
pip install -r requirements.txt
```

##### 5 数据库迁移

```mysql
# 在服务器的数据库中创建项目需要的数据库
CREATE DATABASE beautiful CHARACTER SET utf8;
```

如果数据库名或密码与项目setting文件不匹配。需要进行修改。使用`vim 文件名`。
```shell
vim ./item/settings.py
```
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        "NAME": 'beautiful',        # 数据库名字
        "USER": "root",
        "PASSWORD": "root",  		# 密码
        "HOST": "127.0.0.1",        # 哪台机器安装了mysql
        "PORT": "3306",
    }
}
```
数据库迁移命令

```shell
python manage.py makemigrations
python manage.py migrate
```

如果存在报错，一定要进行解决，无法进行下一步。

##### 6 服务器配置nginx

进入nginx的配置文件。路径  /etc/nginx/nginx.conf

在http内部加上：

```
include /home/blog/nginx.conf;
```

这里表示包含了项目目录里面的nginx.conf文件，使得之前手动配置的文件生效。

把http内部其他server加上#注释。每行前面加#

重启nginx

```
nginx -s reload
```

##### 7 启动uwsgi

```shell
# 运行
uwsgi --ini uwsgi.ini
# 停止
uwsgi --stop uwsgi.pid
# 重启
uwsgi --reload uwsgi.pid
```

部署成功！
```shell
# 使用kill命令发送信号
# uWSGI支持通过发送信号来控制进程。常用的信号是SIGTERM和SIGUSR1。

# 查找uWSGI进程ID：

pgrep -f uwsgi


# 发送SIGTERM信号来停止uWSGI：
kill -TERM <pid>
Copy
# 发送SIGUSR1信号来重新加载uWSGI：
kill -USR1 <pid>
```
