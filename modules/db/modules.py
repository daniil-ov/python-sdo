from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

engine = create_engine('mysql://root:123@127.0.0.1/sdo?charset=utf8', echo=True)

Session = sessionmaker(bind=engine)


class Modules(Base):
    __tablename__ = 'modules'
    id = Column(Integer, primary_key=True)
    name_module = Column(String(100), unique=True)
    test_id = Column(
        String(100),
        ForeignKey('tests.id'),
        nullable=False)
    theory_id = Column(
        String(50),
        ForeignKey('theory.id'),
        nullable=False)
    description = Column(String(1000), unique=True)
    created_date = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, name_module, test_id, theory_id, description):
        self.name_module = name_module
        self.test_id = test_id
        self.theory_id = theory_id
        self.description = description


Base.metadata.create_all(bind=engine)
