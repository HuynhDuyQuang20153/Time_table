from datetime import datetime, timedelta
from models import Subject, Class, Schedule, Teacher
from sqlalchemy.orm import contains_eager
from flask import jsonify
from extensions import db


def is_item_in_week(item, week_start, week_end):
    # Kiểm tra xem môn học (item) có nằm trong khoảng thời gian từ week_start đến week_end hay không.
    Date_end = item['date_end']
    Date_start = item['date_start']
    Date_end_format = datetime.strptime(Date_end, '%Y-%m-%d')
    Date_start_format = datetime.strptime(Date_start, '%Y-%m-%d')

    # Nếu ngày bắt đầu của môn học lớn hơn ngày kết thúc của tuần và ngày kết thúc của môn học nhỏ hơn ngày bắt đầu của tuần
    if Date_end < week_start or Date_start > week_end :  
        return False  # Không hiển thị môn học này

    # Kiểm tra nếu môn học nằm trong tuần cuối cùng và ngày học không lớn hơn ngày kết thúc
    date_of_week = int(item.get('date_week'))
    week_start = datetime.strptime(week_start, '%Y-%m-%d')
    current_date = week_start + timedelta(days=date_of_week - 1) 
    if Date_end <= week_end and current_date > Date_end_format:
        return False 

    # Kiểm tra nếu môn học nằm trong tuần đầu tiên và ngày học không bé hơn ngày bắt đầu
    if Date_start_format >= week_start and current_date < Date_start_format:
        return False  

    return True


def get_week_dates(week_offset):
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday()) + timedelta(weeks=week_offset)      # Lấy thứ 2 của tuần được chỉ định
    end_of_week = start_of_week + timedelta(days=6)                                             # Lấy chủ nhật của tuần        
    return start_of_week.strftime('%Y-%m-%d'), end_of_week.strftime('%Y-%m-%d')


def filter_items_for_week(items, week_offset):
    week_start, week_end = get_week_dates(week_offset)
    filtered_items = [item for item in items if is_item_in_week(item, week_start, week_end)]
    return filtered_items


def get_full_schedule(schedule_id):
    schedules = (
        Schedule.query
        .join(Class, Schedule.id_class == Class.id_class)  
        .join(Subject, Class.id_subject == Subject.id_subject)
        .join(Teacher, Class.id_teacher == Teacher.id_teacher, isouter=True)  
        .options(
            contains_eager(Schedule.class_info).contains_eager(Class.subject),
            contains_eager(Schedule.class_info).contains_eager(Class.teacher)
        )
    )

    # Nếu schedule_id là số hợp lệ, thực hiện lọc
    if isinstance(schedule_id, int):
        schedules = schedules.filter(Schedule.id_schedule == schedule_id)

    schedules.all()

    schedule_data = [
        {
            "id": schedule.id_class,
            "id_class": schedule.class_info.id_class,
            "id_subject": schedule.class_info.id_subject,
            "id_schedule": schedule.id_schedule,
            "id_teacher": schedule.class_info.id_teacher,
            "class_code": schedule.class_info.class_code,
            "team": schedule.class_info.team,
            "learning_facility": schedule.class_info.learning_facility,
            "room": schedule.class_info.room,
            "learning_software": schedule.class_info.learning_software,
            "suspension_status": schedule.class_info.suspension_status,
            "code_online": schedule.class_info.code_online,
            "subject_name": schedule.class_info.subject.name_subject,
            "type_class": schedule.class_info.subject.type_class,
            "teacher_name": schedule.class_info.teacher.name_teacher if schedule.class_info.teacher else "Chưa có GV",
            "date_week": schedule.date_week,
            "period_from": schedule.period_from,
            "period_to": schedule.period_to,
            "date_start": schedule.date_start.strftime('%Y-%m-%d'),
            "date_end": schedule.date_end.strftime('%Y-%m-%d'),
        }
        for schedule in schedules
    ]

    return schedule_data


def get_time_table(week_offset):
    data = get_full_schedule(None)
    filtered_items = filter_items_for_week(data, week_offset)
    week_start, week_end = get_week_dates(week_offset)
    return jsonify({
        'filtered_items': filtered_items,
        'week_start': week_start,
        'week_end': week_end
    })


def get_subject_name():
    data = get_full_schedule(None)
    return jsonify({
        'data': data
    })  


def get_data_details(schedule_id):
    data = get_full_schedule(schedule_id)
    return jsonify({
        'data': data
    }) 


def get_facilities():
    facilities = db.session.query(Class.learning_facility).distinct().all()  # Lấy danh sách cơ sở không trùng lặp
    return [facility[0] for facility in facilities]  # Chuyển thành danh sách đơn giản