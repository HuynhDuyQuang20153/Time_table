from extensions import db
# from models.class_model import Class

class Schedule(db.Model):
    __tablename__ = 'schedule'
    id_schedule = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    id_class = db.Column(db.Integer, db.ForeignKey('class.id_class'), nullable=False)
    date_week = db.Column(db.Integer, nullable=False)  # Ngày trong tuần (5 = Thứ Sáu)
    period_from = db.Column(db.Integer, nullable=False)  # Tiết bắt đầu
    period_to = db.Column(db.Integer, nullable=False)  # Tiết kết thúc
    date_start = db.Column(db.Date, nullable=False)  # Ngày bắt đầu
    date_end = db.Column(db.Date, nullable=True)  # Ngày kết thúc

    # Thiết lập quan hệ
    class_info = db.relationship('Class', backref='schedules')

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}




