import sqlite3
import time

connection = sqlite3.connect('users.db')
cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
    ID_User INTEGER PRIMARY KEY NOT NULL,
    Username VARCHAR(20) DEFAULT 'Unknown_user',
    Login TEXT NOT NULL,
    Password TEXT NOT NULL,
    Role VARCHAR(20) NOT NULL
    )
    ''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Appeals (
    ID_Appeal INTEGER PRIMARY KEY NOT NULL,
    Username VARCHAR(20) NOT NULL,
    Text_of_the_appeal TEXT NOT NULL
    )
    ''')


class Menu:
    def First_admin(self):
        answer = get_choice(["Изменить роль пользователя", "Удалить пользователя",
                             "Посмотреть все обращения", "Оставить обращение", "Выход"])
        if answer == 1:
            answer = "Изменить роль пользователя"
        elif answer == 2:
            answer = "Удалить пользователя"
        elif answer == 3:
            answer = "Посмотреть, выписанные рецепты"
        elif answer == 4:
            answer = "Выписать рецепт"
        elif answer == 5:
            answer = "Выход"

        return answer

    def Admin(self):
        answer = get_choice(["Посмотреть, выписанные рецепты", "Выписать рецепт", "Выход"])
        if answer == 1:
            answer = "Посмотреть, выписанные рецепты"
        elif answer == 2:
            answer = "Выписать рецепт"
        elif answer == 3:
            answer = "Выход"

        return answer

    def User(self):
        answer = get_choice(["Выписать рецепт", "Выход"])
        if answer == 1:
            answer = "Выписать рецепт"
        elif answer == 2:
            answer = "Выход"

        return answer

    def change_role(self):
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        a = True
        while a:
            username = input("Введите имя пользователя, роль которого хотите изменить: ")
            if has_value_in_column(cursor, 'Users', 'Username', username):
                new_role = input("Введите новую роль пользователя: ")

                cursor.execute('UPDATE Users SET Role = ? WHERE Username = ?', (new_role, username))
                connection.commit()

                break
            else:
                print("Пользователя с таким именем не существует, попробуйте снова.")
                time.sleep(1)
                clear_screen()

    def del_user(self):
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()

        a = True
        while a:
            username = input("Введите имя пользователя, которого хотите удалить: ")
            if has_value_in_column(cursor, 'Users', 'Username', username):
                connection = sqlite3.connect('users.db')
                cursor = connection.cursor()
                cursor.execute("DELETE FROM Users Where Username = ?", (username,))
                connection.commit()
                break
            else:
                print("Пользователя с таким именем не существует, попробуйте снова.")
                time.sleep(1)
                clear_screen()

    def check_appeals(self):
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        connection.commit()

        clear_screen()
        all_appeals = cursor.execute("SELECT Appeal_text FROM Appeals WHERE Username NOT NULL").fetchall()

        for i in range(len(all_appeals)):
            print(f"{i + 1}. {all_appeals[i]}")

        a = input("Нажмите Enter, чтобы продолжить ")

    def set_appeal(self, username):
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()

        text = input("Введите текст обращения: ")

        cursor.execute('INSERT INTO Appeals (Username, Appeal_text) VALUES (?, ?)', (username, text,))
        connection.commit()
        connection.close()


def clear_screen():
    print("\033[H\033[J")


def get_choice(options):
    for i, option in enumerate(options):
        print(f"{i + 1}. {option}")
    choice = input("Выберите вариант: ")
    while not choice.isdigit() or int(choice) < 1 or int(choice) > len(options):
        choice = input("Пожалуйста, выберите номер варианта: ")
    return int(choice)


def has_value_in_column(cursor, table, column, value):
    query = 'SELECT 1 from {} WHERE {} = ? LIMIT 1'.format(table, column)
    return cursor.execute(query, (value,)).fetchone() is not None


def close_connection():
    connection.commit()
    connection.close()


def new_user(Username, Login, Password, Role="User"):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO Users (Username, Login, Password, Role) VALUES (?, ?, ?, ?)',
                   (Username, Login, Password, Role))
    connection.commit()


if has_value_in_column(cursor, 'Users', 'Username', 'First'):
    pass
else:
    new_user("First", "Lili", "LiAtlant", "First-admin")
connection.commit()


def reg():
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    a = True
    while a:
        clear_screen()
        print("Для продолжение вам необходимо войти")
        b = True
        while b:
            nickname = input("Введите свое имя пользователя: ")
            if has_value_in_column(cursor, 'Users', 'Username', nickname):
                c = True
                while c:
                    User_login = \
                    (cursor.execute("SELECT * FROM Users WHERE Username = '{}'".format(nickname)).fetchone())[2]
                    User_password = \
                    (cursor.execute("SELECT * FROM Users WHERE Username = '{}'".format(nickname)).fetchone())[3]
                    Role = (cursor.execute("SELECT * FROM Users WHERE Username = '{}'".format(nickname)).fetchone())[4]
                    print(User_login, User_password)
                    peremennaya = True

                    while peremennaya:
                        login = input("Введите логин: ")
                        password = input("Пароль: ")
                        if login == User_login and password == User_password:
                            print("Вход прошел успешно. Добро пожаловать, " + nickname)
                            a, b, c, peremennaya = False, False, False, False
                            clear_screen()
                        else:
                            print("Неправильный логин или пароль. Попробуйте снова.")
                            clear_screen()
                    c = False

                b = False
                a = False
            else:
                print("Такого имени нет, желаете зарегистрироваться?")
                answer = get_choice(["Да", "Нет"])
                clear_screen()
                if answer == 1:
                    print(
                        "                                                                                  Регистрация")
                    z = True
                    while z:
                        nickname = input("Введите новое имя пользователя: ")
                        if has_value_in_column(cursor, 'Users', 'Username', nickname):
                            print("Пользователь с таким именем уже есть. Попробуйте еще раз.")
                        else:
                            z = False
                    h = True
                    while h:
                        login = input("Введите логин: ")
                        password = input("Введите пароль: ")
                        print("Вы уверены, что вы ввели данные правильно?")
                        answer = get_choice(["Да", "Нет"])
                        if answer == 1:
                            Role = "User"
                            connection = sqlite3.connect('users.db')
                            cursor = connection.cursor()
                            new_user(nickname, login, password)
                            print("User added")
                            b = False
                            h = False
                        else:
                            clear_screen()
                            print("Тогда введите данные еще раз")
                            time.sleep(1)
                            clear_screen()

    return nickname, login, password, Role



connection = sqlite3.connect('users.db')
cursor = connection.cursor()


def main():
    clear_screen()
    a = True
    while a:
        print("Добро пожаловать!!")
        ans = get_choice(["Вход/Регистрация", "Выход"])
        if ans == 1:
            nickname, login, password, Role = reg()
            menu = Menu()
            b = True
            while b:
                print("Меню")
                if Role == "First-admin":
                    choice = menu.First_admin()

                    if choice == "Изменить роль пользователя":
                        menu.change_role()
                        clear_screen()
                        print("Успешно")
                        time.sleep(1)
                        clear_screen()


                    elif choice == "Удалить пользователя":
                        menu.del_user()
                        clear_screen()
                        print("Успешно")
                        time.sleep(1)
                        clear_screen()


                    elif choice == "Посмотреть, выписанные рецепты":
                        menu.check_appeals()
                        clear_screen()


                    elif choice == "Выписать рецепт":
                        menu.set_appeal(nickname)
                        clear_screen()
                        print("Успешно")
                        time.sleep(1)
                        clear_screen()


                    elif choice == "Выход":
                        clear_screen()
                        break

                elif Role == "Admin":
                    choice = menu.Admin()

                    if choice == "Посмотреть, выписанные рецепты":
                        menu.check_appeals()
                        clear_screen()


                    elif choice == "Выписать рецепт":
                        menu.set_appeal(nickname)
                        clear_screen()
                        print("Успешно")
                        time.sleep(1)
                        clear_screen()

                    elif choice == "Выход":
                        clear_screen()
                        break

                elif Role == "User":
                    choice = menu.User()
                    if choice == "Выписать рецепт":
                        menu.set_appeal(nickname)
                        clear_screen()
                        print("Успешно")
                        time.sleep(1)
                        clear_screen()
                    elif choice == "Выход":
                        clear_screen()
                        break

        else:
            break


main()

connection.commit()
connection.close()

clear_screen()
print("Программа завершена")