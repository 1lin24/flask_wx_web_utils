## 环境

* 使用pyenv+virtualenv管理项目
* 环境名称统一使用.venv
* python3.6.2

## 使用

* 安装环境管理工具
    * 安装 pyevn
        * 安装依赖
            `yum install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel`
        * 安装pyenv
            ```
            mkdir ~/.pyenv
            git clone git://github.com/yyuu/pyenv.git ~/.pyenv  
            echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc  
            echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc  
            echo 'eval "$(pyenv init -)"' >> ~/.bashrc  
            source ~/.bashrc
            ```
    * 安装 virtualenv
        * `pip install virtualenv`

## 环境配置
    * 创建虚拟环境
        * `pyenv install -v 3.6.2`
        * `pyenv global 3.6.2`
        * `cd prj_root`
        * `virtualenv --no-site-packages venv`
    * 启动虚拟环境
        * `source venv/bin/activate`
    * 安装依赖
        * `pip install -r requirements.txt`

## 配置
* 修改config.py
    * 配置数据库地址
* 修改uwsgi.ini
    * 文件
        * uwsgi_dev.ini
        * uwsgi_pro.ini
    * 修改内容
        * socket
        * chdir
        * stats
        * logto

## 启动

```
uwsgi uwsgi/domain.ini
```

