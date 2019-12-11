# Импортируем datatime
from datetime import datetime
# Импортируем модуль стандартной библиотеки time
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# Заводим константу для соединения с базой данных и базовый класс для моделей будущих таблиц:
# константа, указывающая способ соединения с базой данных
DB_PATH = "sqlite:///sochi_athletes.sqlite3"
# базовый класс моделей таблиц
Base = declarative_base()

# Опишем модели таблиц в базе данных. 
# Будем использовать 2 таблицы:
# user — для хранения данных вводимых пользователей
# athelete — для хранения данных атлетов.
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


class Athelete(Base):
    """
    Описывает структуру таблицы athelete для хранения данных атлетов
    """
    # задаем название таблицы
    __tablename__ = 'athelete'
    # идентификатор атлета, первичный ключ
    id = sa.Column(sa.Integer, primary_key=True)
    # возраст атлета
    age = sa.Column(sa.Integer)
    # дата рождения атлета
    birthdate = sa.Column(sa.Text)
    # пол атлета
    gender = sa.Column(sa.Text)
    # рост атлета
    height = sa.Column(sa.Float)
    # имя атлета
    name = sa.Column(sa.Text)
    # вес атлета
    weight = sa.Column(sa.Integer)
    # золотые медали
    gold_medals = sa.Column(sa.Integer)
    # серебряные медали
    silver_medals = sa.Column(sa.Integer)
    # бронзовые медали
    bronze_medals = sa.Column(sa.Integer)
    # ВСЕГО медали
    total_medals = sa.Column(sa.Integer)
    # вид спорта
    sport = sa.Column(sa.Text)
    # страна
    country = sa.Column(sa.Text)


def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    # создаем соединение к базе данных
    engine = sa.create_engine(DB_PATH)
    # создаем описанные таблицы
    Base.metadata.create_all(engine)
    # cоздаем сессию
    session = sessionmaker(engine)
    return session()


def request_data():
    """
    Запрашивает у пользователя данные и добавляет их в список users
    """
    # выводим приветствие
    print("Привет! Введите идентификатор пользователя в базе User!\n")
    # просим пользователя ввести идентификатор пользователя
    id_str = input("Введите id: ")
    user_id = int(id_str)
    # возвращаем id пользователя
    return user_id


def find_bdate_neighbour(user_birthdate, session):
    """
    Функция ищет в базе данных athelets атлета с днем рождения, ближайшим к user_birthdate
    Возвращает словарь bdate_neighbour = {'name': <name>, 'birthdate': <birthdate>}
    с данными найденного атлета
    """
    # считывем базу атлетов:
    athelete_list = session.query(Athelete).all()
    # задаем исходные значения для цикла и для функции
    delta = None
    bdate_neighbour = {'name': "", 'birthdate': ""}
    # цикл по всем атлетам
    for athelete in athelete_list:
        # считываем дату рождения атлета и переводим ее в формат даты с помощью библиотеки datetime
        bdate = datetime.strptime(athelete.birthdate, '%Y-%m-%d').date()
        # сравниваем разницу дат рождения пользователя и атлета с delta (на первом цикле None)
        if not delta or abs(bdate - user_birthdate) < delta:
            # если разница меньше delta, записываем ее в delta 
            delta = abs(bdate - user_birthdate)
            # а данные атлета записываем в словарь
            bdate_neighbour['name'] = athelete.name
            bdate_neighbour['birthdate'] = athelete.birthdate
    # возвращаем словарь с данными найденного атлета:
    return bdate_neighbour


def find_height_neighbour(user_height, session):
    """
    Функция ищет в базе данных athelets атлета с ростом, ближайшим к user_height
    Возвращает словарь height_neighbour = {'name': <name>, 'heigth': <height>}
    с данными найденного атлета
    """
    # считывем базу атлетов:
    athelete_list = session.query(Athelete).all()
    # задаем исходные значения для цикла и для функции
    delta = None
    height_neighbour = {'name': "", 'heigth': ""}
    # цикл по атлетам
    for athelete in athelete_list:
        # считываем рост атлета
        height = athelete.height
        # боремся с пропусками в параметре height атлетов
        if height:
            # сравниваем разницу роста пользователя и роста атлета с delta (на первом цикле None)
            if not delta or abs(height - user_height) < delta:
                # если разница меньше delta, записываем ее в delta
                delta = abs(height - user_height)
                # а данные атлета записываем в словарь
                height_neighbour['name'] = athelete.name
                height_neighbour['height'] = athelete.height
    # возвращаем словарь с данными найденного атлета:
    return height_neighbour


def find(user, session):
    """
    Для заданного пользователя user находит в базе atheletes: 
    - ближайшего по дате рождения к данному пользователю = bdate_neighbour
    - ближайшего по росту к данному пользователю = height_neighbour
    Возвращает словари:
    bdate_neighbour = {'name': <name>, 'birthdate': <birthdate>} 
    height_neighbour = {'name': <name>, 'heigth': <height>}
    """
    # считываем параметры пользователя:
    # переводим дату рождения пользователя из str в формат даты с помощью библиотеки datetime
    user_birthdate = datetime.strptime(user.birthdate, '%Y-%m-%d').date()
    # считываем рост пользователя в формате float
    user_height = user.height
    # ищем соседа по дню рождения
    bdate_neighbour = find_bdate_neighbour(user_birthdate, session)
    # ищем соседа по росту
    height_neighbour = find_height_neighbour(user_height, session)
    return (bdate_neighbour, height_neighbour)


# Оформим вывод результатов поиска в отдельную функцию:
def print_users_list(user, bdate_neighbour, height_neighbour):
    """
    Выводит на экран результаты поиска ближайшего по дате рождения к данному пользователю 
    и ближайшего по росту к данному пользователю.
    """
    # user точно не пуст. Это проверено ранее
    # печатаем заголовок с именем и id пользователя:
    print("Для пользователя {} {} c id={}, ростом {} и датой рождения {} найдены:".format(
        user.first_name, user.last_name, user.id, user.height, user.birthdate))
    # печатаем ближайшего атлета по росту:
    print("- ближайший по росту атлет - {} с ростом {},".format(
        height_neighbour['name'], height_neighbour['height']))
    # печатаем ближайшего атлета по дате рождения:
    print("- ближайший по дате рождения атлет - {} с датой рождения {}.".format(
        bdate_neighbour['name'], bdate_neighbour['birthdate']))


def main():
    """
    Осуществляет взаимодействие с пользователем, обрабатывает пользовательский ввод
    """
    session = connect_db()
    # запускаем функцию ввода данных
    user_id = request_data()
    # ищем в базе user пользователя с введенным id:
    user = session.query(User).filter(User.id == user_id).first()
    # проверяем, что такой пользователь есть
    # TODO: перенести проверку наличия пользователя в find
    if not user:
        print("Пользователя с таким id не существует")
    else:
        bdate_neighbour, height_neighbour = find(user, session)
        print_users_list(user, bdate_neighbour, height_neighbour)


if __name__ == "__main__":
    main()
