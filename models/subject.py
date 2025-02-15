from extensions import db

class Subject(db.Model):
    __tablename__ = 'subject'
    id_subject = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
    name_subject = db.Column(db.String(255), nullable=False)
    type_class = db.Column(db.String(10), nullable=False)  # LT/TH (Lý thuyết / Thực hành)

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}




