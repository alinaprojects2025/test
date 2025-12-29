import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        login TEXT UNIQUE,
        password TEXT,
        balance DECIMAL
    )
""")
conn.commit()

def register():
    login = input("Введите логин: ")
    password = input("Введите пароль: ")
    balance = float(input("Введите начальный баланс: "))
    try:
        cursor.execute("""
            INSERT INTO users (login, password, balance)
            VALUES (?, ?, ?)
        """, (login, password, balance))
        conn.commit()
        print(f"Пользователь {login} зарегистрирован с балансом {balance}")
    except sqlite3.IntegrityError:
        print("Такой логин уже существует!")

def login_user():
    login = input("Введите логин: ")
    password = input("Введите пароль: ")
    cursor.execute("""
        SELECT id, balance FROM users
        WHERE login = ? AND password = ?
    """, (login, password))
    result = cursor.fetchone()
    if result:
        user_id, balance = result
        print(f"Добро пожаловать, {login}! Ваш ID: {user_id}, Баланс: {balance}")
    else:
        print("Неверный логин или пароль")

def check_balance():
    login = input("Введите логин: ")
    cursor.execute("SELECT balance FROM users WHERE login = ?", (login,))
    result = cursor.fetchone()
    if result:
        print(f"Баланс пользователя {login}: {result[0]}")
    else:
        print("Пользователь не найден")

while True:
    choice = input("\nВыберите действие:\n[1] Регистрация\n[2] Вход\n[3] Проверить баланс\n[4] Выход\nВаш выбор: ")
    if choice == "1":
        register()
    elif choice == "2":
        login_user()
    elif choice == "3":
        check_balance()
    elif choice == "4":
        print("Выход из программы")
        break
    else:
        print("Неверный выбор")