import time

class BankAccount:
    def __init__(self, pin="1234", initial_balance=2000):
        self.__pin = pin
        self.__balance = initial_balance
        self.__history = []

    def verify_pin(self, entered_pin):
        return self.__pin == entered_pin

    def get_balance(self):
        return self.__balance

    def withdraw(self, amount):
        if amount <= 0:
            return False, "Сумма должна быть положительной."
        if amount > self.__balance:
            return False, "Недостаточно средств."
        self.__balance -= amount
        self.__history.append((f"Снятие: {amount:.2f}", time.ctime()))
        return True, f"Выдано: {amount:.2f}"

    def deposit(self, amount):
        if amount <= 0:
            return False, "Сумма должна быть положительной."
        self.__balance += amount
        self.__history.append((f"Пополнение: {amount:.2f}", time.ctime()))
        return True, f"Пополнено на: {amount:.2f}"

    def get_history(self):
        return self.__history.copy()


class ATM:
    def __init__(self, account):
        self.__account = account

    def __verify_pin(self):
        for _ in range(3):
            pin = input("Введите PIN-код: ")
            if self.__account.verify_pin(pin):
                print("Доступ разрешён.")
                return True
            else:
                print("Неверный PIN-код.")
        print("Превышено количество попыток.")
        return False

    def run(self):
        if not self.__verify_pin():
            return

        while True:
            print("\n1. Баланс\n2. Снять\n3. Пополнить\n4. История\n5. Выход")
            choice = input("Выберите: ").strip()

            if choice == "1":
                print(f"Баланс: {self.__account.get_balance():.2f} ")
            elif choice == "2":
                try:
                    amount = float(input("Сумма снятия: "))
                    success, msg = self.__account.withdraw(amount)
                    print(msg)
                except ValueError:
                    print("Введите число!")
            elif choice == "3":
                try:
                    amount = float(input("Сумма пополнения: "))
                    success, msg = self.__account.deposit(amount)
                    print(msg)
                except ValueError:
                    print("Введите число!")
            elif choice == "4":
                history = self.__account.get_history()
                if history:
                    for record in history:
                        print(f"{record[0]} | {record[1]}")
                else:
                    print("История пуста.")
            elif choice == "5":
                print("До свидания!")
                break
            else:
                print("Неверный выбор.")


def main():
    account = BankAccount(pin="1234", initial_balance=2000)
    atm = ATM(account)
    atm.run()


if __name__ == "__main__":
    main()