from datetime import datetime
from models import Subject, Class, Schedule, Teacher
from flask import jsonify
from extensions import db


def add_data(data):
    # Thêm môn học
    subject = Subject(name_subject=data["subject"], type_class=data["type_class"])
    db.session.add(subject)
    subject_ = Subject.query.filter_by(name_subject=data["subject"]).first()
    
    # Thêm giáo viên
    teacher = Teacher(name_teacher=data["Teacher"])
    db.session.add(teacher)
    teacher_ = Teacher.query.filter_by(name_teacher=data["Teacher"]).first()

    # Thêm lớp học
    if "suspension" in data:
        suspension = data["suspension"]
    else:
        suspension = ''
    class_mode = Class(
        id_subject=subject_.id_subject, id_teacher=teacher_.id_teacher, class_code=data["class_code"],
        team=data["Team"], learning_facility=data["Learning_facility"], room=data["Room"],
        learning_software=data["Learning_software"], code_online=data["Code_online"], suspension_status=suspension
    )
    db.session.add(class_mode)
    db.session.commit()

    # Thêm lịch học
    schedule = Schedule(
        id_class=class_mode.id_class, date_week=data["date_week"], period_from=data["Period_from"], period_to=data["Period_to"],
        date_start=datetime.strptime(data["Date_start"], "%Y-%m-%d").date(), 
        date_end=datetime.strptime(data["Date_end"], "%Y-%m-%d").date()
    )

    db.session.add(schedule)

    db.session.commit()
    return jsonify({"message": "Bạn đã sửa lịch học thành công!", "status": "success"}), 200