# 配置文件
import os

class Config:
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = 'mysql://hcs:uway123@192.168.254.136:3306/procurement_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 密钥配置
    SECRET_KEY = os.urandom(24)
    
    # 上传文件配置
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
