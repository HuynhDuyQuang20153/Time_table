from extensions import db

class Class(db.Model):
    __tablename__ = 'class'
    id_class = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    id_subject = db.Column(db.Integer, db.ForeignKey('subject.id_subject'), nullable=False)
    id_teacher = db.Column(db.Integer, db.ForeignKey('teacher.id_teacher'), nullable=False)
    class_code = db.Column(db.String(20), nullable=False) 
    team = db.Column(db.String(10))  # Nhóm (A07)
    learning_facility = db.Column(db.String(10))  # Cơ sở học (B)
    room = db.Column(db.String(20))  # Phòng học (B.14-04)
    learning_software = db.Column(db.String(255))  # Phần mềm học online
    code_online = db.Column(db.String(100))  # Mã lớp online
    suspension_status = db.Column(db.String(50))  # Trạng thái hoãn học

    # Thiết lập quan hệ
    subject = db.relationship('Subject', backref='subjects')
    teacher = db.relationship('Teacher', backref='teachers')

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}




