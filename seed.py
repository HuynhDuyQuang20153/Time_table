from app import db
from models import Subject, Teacher, Class, Schedule
from flask import Flask
import os
from datetime import datetime

app = Flask(__name__)

# Cấu hình Database (Chỉnh sửa tùy vào dự án của bạn)
BASE_FOLDER = "Database"
os.makedirs(BASE_FOLDER, exist_ok=True)
DATABASE_PATH = os.path.join(os.getcwd(), BASE_FOLDER, 'app.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DATABASE_PATH}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Seed Data Function
def seed_data():
    with app.app_context():
        # Xóa dữ liệu cũ (nếu cần)
        db.session.query(Class).delete()
        db.session.query(Schedule).delete()
        db.session.query(Subject).delete()
        db.session.query(Teacher).delete()

        # Thêm môn học
        subject1 = Subject(name_subject="Mathematics", type_class="LT")
        subject2 = Subject(name_subject="Physical", type_class="TH")
        db.session.add_all([subject1, subject2])
        db.session.commit()
        subject_1 = Subject.query.filter_by(name_subject="Mathematics").first()
        subject_2 = Subject.query.filter_by(name_subject="Physical").first()
        


        # Thêm giáo viên
        teacher1 = Teacher(name_teacher="John Doe")
        teacher2 = Teacher(name_teacher="Robin Hook")
        db.session.add_all([teacher1, teacher2])
        db.session.commit()
        teacher_1 = Teacher.query.filter_by(name_teacher="John Doe").first()
        teacher_2 = Teacher.query.filter_by(name_teacher="Robin Hook").first()

        # Thêm lớp học
        class1 = Class(
            id_subject=subject_1.id_subject, id_teacher=teacher_1.id_teacher, class_code="MTH101",
            team="A01", learning_facility="B", room="B.14-04",
            learning_software="Zoom", code_online="XYZ123", suspension_status="Active"
        )

        class2 = Class(
            id_subject=subject_2.id_subject, id_teacher=teacher_2.id_teacher, class_code="PHY102",
            team="A02", learning_facility="C", room="C.12-02",
            learning_software="Google Meet", code_online="ABC456", suspension_status="Active"
        )
        db.session.add_all([class1, class2])
        db.session.commit()

        # Thêm lịch học
        schedule1 = Schedule(
            id_class=class1.id_class, date_week=2, period_from=1, period_to=3,
            date_start=datetime.strptime("2025-01-15", "%Y-%m-%d").date(), 
            date_end=datetime.strptime("2025-06-15", "%Y-%m-%d").date()
        )

        schedule2 = Schedule(
            id_class=class2.id_class, date_week=5, period_from=2, period_to=4,
            date_start=datetime.strptime("2025-02-10", "%Y-%m-%d").date(), 
            date_end=datetime.strptime("2025-06-20", "%Y-%m-%d").date()
        )

        db.session.add_all([schedule1, schedule2])
        db.session.commit()

        print("✅ Dữ liệu đã được thêm thành công!")

# Chạy seeding
if __name__ == "__main__":
    seed_data()
