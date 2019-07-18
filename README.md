## 项目描述
这是一个利用python的Django框架开发的博客系统，记录以及分享一些工作上遇到的问题，以及解决办法。还有一些python开发的小应用。

## 下载后本地注意项
* 在 myblog/setting.py 修改自己的本地数据库密码，线上同理。
* 运行根目录下的myblog.sql，不允许也可以。
* 初始化数据库，运行：python manage.py makemigrations
                    python manage.py migrate
    
## 一些基本命令
* 安装Django：	pip install django  指定版本 pip3 install django==2.0

* 新建项目：	django-admin.py startproject mysite

* 新建APP :	python manage.py startapp blog

* 启动：python manage.py runserver 8080

* 同步或者更改生成 数据库：

* python manage.py makemigrations

* python manage.py migrate

* 清空数据库：	python manage.py flush

* 创建管理员：	python manage.py createsuperuser

* 修改用户密码： python manage.py changepassword username

* Django项目环境终端： python manage.py shell