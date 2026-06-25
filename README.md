# 完整环境配置

## 一、创建虚拟环境（只需执行一次）

powershell

//进入项目目录

cd C:\Users\12526\Downloads\face-checkin

//创建虚拟环境

python -m venv venv

## 二、激活虚拟环境（每次新开终端都要执行）

powershell

//PowerShell 用户（你当前用的）

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

venv\Scripts\activate

激活成功后，命令行前面会出现 (venv)

## 三、安装依赖（只需执行一次）

确保已激活虚拟环境（看到 (venv)），然后执行：

powershell

//升级 pip

python -m pip install --upgrade pip

//核心框架

pip install Flask==2.3.3 Werkzeug==2.3.7

//跨域支持

pip install flask-cors==4.0.0

//数据库

pip install PyMySQL==1.1.0 SQLAlchemy==1.4.50

//OBS 存储（S3 兼容）

pip install boto3==1.34.69

//华为云 FRS（如果失败，见下方替代方案）

pip install huaweicloudsdkcore

pip install huaweicloudsdkfrs

## 四、验证安装

powershell

pip list

确认包含以下包（版本可能略有不同）：

plain

Flask              2.3.3

flask-cors         4.0.0

PyMySQL            1.1.0

SQLAlchemy         1.4.50

boto3              1.34.69

botocore           x.x.x  (boto3自动安装)

huaweicloudsdkcore x.x.x

huaweicloudsdkfrs  x.x.x

## 五、后续每次启动项目的步骤

powershell

//1. 进入项目目录

cd C:\Users\12526\Downloads\face-checkin

//2. 激活虚拟环境

venv\Scripts\activate

//3. 启动项目

python app.py
