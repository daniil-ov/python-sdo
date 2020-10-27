from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.dialects import mysql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import re

Base = declarative_base()

engine = create_engine('mysql://root:123@127.0.0.1/reshuege?charset=utf8', echo=True)

Session = sessionmaker(bind=engine)


class Rus_texts(Base):
    __tablename__ = 'rus_texts'

    text_id = Column(Integer, primary_key=True)
    text = Column(mysql.TEXT(collation=u'utf8_general_ci'), nullable=False)
    user_id = Column(Integer())


Base.metadata.create_all(bind=engine)


def rus_texts():
    regex = re.compile('\(([0-9]{1,2})\)')

    session = Session()

    find_rus_texts = session.query(Rus_texts).all()

    for item in find_rus_texts:
        strrrrrr = regex.findall(item.text)
        cnt_str = len(strrrrrr)

        if item.text_id >0:
            for number in range(cnt_str):
                # print(strrrrrr[number])
                if number != (cnt_str - 1):
                    if (int(strrrrrr[number + 1]) - int(strrrrrr[number])) == 1:
                        pass
                    else:
                        # result = re.sub(r'(\(' + strrrrrr[number] + '\))(.*)(\(([^0-9]{1,3})\))', r'\1\2' + '(' + str(int(strrrrrr[number]) + 1) + ')',
                        #                 item.text)
                        print('id текста', item.text_id, 'номер предложение', int(strrrrrr[number]) + 1)
                        # print('result', result)
                        # print('текст', item.text)
                else:
                    pass

    # print(str)
    # print(item.text)

    session.commit()
    session.close()


rus_texts()
