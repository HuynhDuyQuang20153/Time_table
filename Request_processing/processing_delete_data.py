from flask import jsonify
from extensions import db


def delete_db():
    for table in reversed(db.metadata.sorted_tables):  # Lấy tất cả bảng và đảo ngược thứ tự để tránh lỗi khóa ngoại
        db.session.execute(table.delete())  # Xóa tất cả dữ liệu của bảng
    db.session.commit()
    return jsonify({"status": "success", "message": "Xóa toàn bộ dữ liệu thành công!"}), 200