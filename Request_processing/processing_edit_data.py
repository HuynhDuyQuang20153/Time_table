from datetime import datetime
from models import Subject, Class, Schedule, Teacher
from flask import jsonify
from extensions import db


def change_data(data):
    id_subject = data["subject_id"]
    id_teacher = data["teacher_id"]
    id_class = data["class_id"]
    id_schedule = data["schedule_id"]

    # Cập nhật Subject
    if id_subject:
        subject = Subject.query.get(id_subject)
        subject.type_class = data["type_class"]  

    # Cập nhật Teacher
    if id_teacher:
        teacher = Teacher.query.get(id_teacher)
        teacher.name_teacher = data["Teacher"]  

    # Cập nhật Class
    if id_class:
        class_mode = Class.query.get(id_class)
        class_mode.class_code = data["class_code"]  
        class_mode.team = data["Team"]  
        class_mode.learning_facility = data["Learning_facility"]   
        class_mode.room = data["Room"]   
        class_mode.learning_software = data["Learning_software"]   
        class_mode.code_online = data["Code_online"]   
        if "suspension" in data:
            class_mode.suspension_status = data["suspension"]
        else:
            class_mode.suspension_status = None

    # Cập nhật Schedule
    if id_schedule:
        schedule = Schedule.query.get(id_schedule)
        schedule.date_week = data["date_week"]   
        schedule.period_from = data["Period_from"]  
        schedule.period_to = data["Period_to"]  
        schedule.date_start = datetime.strptime(data["Date_start"] , "%Y-%m-%d").date()
        schedule.date_end = datetime.strptime(data["Date_end"] , "%Y-%m-%d").date()

    db.session.commit()
    return jsonify({"message": "Bạn đã sửa lịch học thành công!", "status": "success"}), 200