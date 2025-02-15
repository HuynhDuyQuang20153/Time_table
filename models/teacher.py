from extensions import db

class Teacher(db.Model):
    __tablename__ = 'teacher'
    id_teacher = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name_teacher = db.Column(db.String(100), nullable=False)

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}




