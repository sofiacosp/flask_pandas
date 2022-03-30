from shared import db
from sqlalchemy import column, String, Integer
from sqlalchemy_utils import ChoiceType
from sqlalchemy.orm import relationship
import enum


class IntEnum(db.TypeDecorator):
    impl = db.Integer()

    def __init__(self, enumtype, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._enumtype = enumtype

        def process_bind_param(self, value, dialect):
                if isinstance(value, enum):
                    return value
                elif isinstance(value, int):
                    return value
                return value.value

        def process_result_value(self, value, dialect):
            return self._enumtype(value)


class Opciones(enum.Enum):
    varon= 'varón'
    mujer= 'mujer'
    general= 'general'


class Usuarios(db.Model):
    id = db.Column(Integer, primary_key=True)
    nombre= db.Column(String(length=50), nullable=False)
    edad = db.Column(Integer)


class Examenes(db.Model):

    id = db.Column(Integer, primary_key=True)
    item1= db.Column(Integer)
    item2= db.Column(Integer)
    item3= db.Column(Integer)
    alumno = relationship("Usuarios", back_populates="nombre")
    baremo= db.Column(db.Enum(Opciones), default= Opciones.general)