# models/__init__.py
# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()

# Import models ở cuối file để tránh lỗi Circular Import
from .subject import Subject
from .class_model import Class  # Đổi tên tránh trùng keyword "class"
from .schedule import Schedule
from .teacher import Teacher
