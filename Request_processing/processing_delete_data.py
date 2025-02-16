from flask import jsonify
from extensions import db
from models import Subject, Class, Schedule, Teacher


def delete_db():
    for table in reversed(db.metadata.sorted_tables):  # Lấy tất cả bảng và đảo ngược thứ tự để tránh lỗi khóa ngoại
        db.session.execute(table.delete())  # Xóa tất cả dữ liệu của bảng
    db.session.commit()
    return jsonify({"status": "success", "message": "Xóa toàn bộ dữ liệu thành công!"}), 200


def delete_schedule(class_id):
    if (class_id == None):
        return jsonify({"status": "error", "message": "Hãy chọn lớp học để xóa!"}), 404

    class_to_delete = Class.query.get(class_id)
    if not class_to_delete:
        return jsonify({"status": "error", "message": "Lớp học không tồn tại"}), 404

    Schedule.query.filter_by(id_class=class_id).delete()
    Class.query.filter_by(id_class=class_id).delete()
    db.session.commit()

    return jsonify({"status": "success", "message": "Xóa lịch học thành công!"}), 200