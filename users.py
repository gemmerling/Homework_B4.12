# Импортируем datatime
from datetime import datetime
# Импортируем sqlalchemy
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# Заводим константу для соединения с базой данных и базовый класс для моделей будущих таблиц:
# константа, указывающая способ соединения с базой данных
DB_PATH = "sqlite:///sochi_athletes.sqlite3"
# базовый класс моделей таблиц
Base = declarative_base()


# Опишем модель таблицы user — для хранения данных вводимых пользователей
class User(Base):
    """
    Описывает структуру таблицы user для хранения регистрационных данных пользователей
    """
    # задаем название таблицы
    __tablename__ = 'user'

    # идентификатор пользователя, первичный ключ
    id = sa.Column(sa.Integer, primary_key=True)
    # имя пользователя
    first_name = sa.Column(sa.Text)
    # фамилия пользователя
    last_name = sa.Column(sa.Text)
    # пол пользователя
    gender = sa.Column(sa.Text)
    # адрес электронной почты пользователя
    email = sa.Column(sa.Text)
    # дата рождения пользователя
    birthdate = sa.Column(sa.Text)
    # рост пользователя
    height = sa.Column(sa.Float)


def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    # создаем соединение к базе данных
    engine = sa.create_engine(DB_PATH)
    # создаем описанные таблицы
    Base.metadata.create_all(engine)
    # создаем фабрику сессию
    # Sessions = sessionmaker(engine)
    # cоздаем сессию
    # session = Sessions()
    session = sessionmaker(engine)
    return session()


def request_data():
    """
    Запрашивает у пользователя данные и добавляет их в список users
    """
    # выводим приветствие
    print("Привет! Я запишу данные!")
    # запрашиваем у пользователя данные
    first_name = input("Введите своё имя: ")
    last_name = input("Введите свою фамилию: ")
    birthdate = input("Ваша дата рождения в формате гггг-мм-дд: ")
    # добиваемся, чтобы пользователь ввел данные в корректном формате
    while not birthdate_check(birthdate):
        birthdate = input("Введите дату в корректном формате гггг-мм-дд: ")
    gender = input("Ваш пол (Male/Female): ")
    height_str = input("Ваш рост в формате м.см: ")
    # добиваемся, чтобы пользователь ввел данные в корректном формате
    while not height_check(height_str):
        height_str = input("Введите рост в корректном формате м.см: ")
    height = float(height_str)
    email = input("Ваш адрес электронной почты: ")
    # проверяем корретность e-mail'а:
    while not valid_email(email):
        email = input("Введите корректный адрес электронной почты: ")
    # создаем нового пользователя
    user = User(
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        email=email,
        birthdate=birthdate,
        height=height
    )
    # возвращаем созданного пользователя
    return user
    # Когда все данные введены пользователем, функция конструирует объект модели 
    # user, в котором заполняются все поля таблицы. Этот объект мы будем использовать 
    # для сохранения результатов в базу данных.


def birthdate_check(birthdate):
    """
    Проверяет формат ввода даты рождения
    """
    try:
        datetime.strptime(birthdate, '%Y-%m-%d').date()
        return True
    except ValueError as ve:
        print ('Ошибка ввода даты: ', ve)
        return False


def height_check(height):
    """
    Проверяет формат ввода роста
    """
    # проверяем позицию точки и проверяем, что все, что осталось - цифры:
    if height.count('.') == 1:
        if height.index(".") == 1:
            height_list = height.split('.')
            height_str = ''.join(height_list)
        return height_str.isdigit()
    else:
        return False


def valid_email(email):
    """
    Проверяет наличие хотя бы одной точки в домене и знака @ в email. Возвращает True, если email допустимый и False - в противном случае.
    """
    if email.count("@") == 1:
        domain = email.split("@")[1]
        if domain.count(".") == 0:
            return False
        else:
            return True
    else:
        return False


def main():
    """
    Осуществляет взаимодействие с пользователем, обрабатывает пользовательский ввод
    """
    session = connect_db()
    # запрашиваем данные пользователя
    user = request_data()
    # добавляем нового пользователя в сессию
    session.add(user)
    # сохраняем все изменения, накопленные в сессии
    session.commit()
    print("Спасибо, данные сохранены!")


if __name__ == "__main__":
    main()
