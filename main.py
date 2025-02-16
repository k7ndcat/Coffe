import sys
import sqlite3
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMainWindow, QTableWidget, QPushButton, QVBoxLayout, QWidget, QTableWidgetItem
import re

conn = sqlite3.connect('coffee.sqlite')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS coffee (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    roast_level TEXT NOT NULL,
    ground BOOLEAN NOT NULL,
    taste_description TEXT NOT NULL,
    price REAL NOT NULL,
    package_volume TEXT NOT NULL
)
''')

# cursor.execute('''
# INSERT INTO coffee (name, roast_level, ground, taste_description, price, package_volume)
# VALUES
# ('Espresso', 'Dark', 0, 'Rich and bold flavor', 5.99, '250g'),
# ('Arabica', 'Medium', 1, 'Smooth and sweet with hints of chocolate', 6.99, '500g'),
# ('Robusta', 'Light', 0, 'Strong and bitter with a nutty finish', 4.99, '200g')
# ''') - сделал базовое содержание таблицы

conn.commit()
conn.close()


class CoffeeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.pushButton.clicked.connect(self.load_coffee_data)
        self.coffee_table.setColumnCount(6)
        self.coffee_table.setHorizontalHeaderLabels(
            ["Название", "Обжарка", "Молотый/Зерно", "Описание вкуса", "Цена", "Объем упаковки"
             ])
        self.pushButton1.clicked.connect(self.create_coffe)
        self.pushButton_3.clicked.connect(self.update_coffe)

    def load_coffee_data(self):
        conn = sqlite3.connect('coffee.sqlite')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM coffee")
        rows = cursor.fetchall()
        if not rows:
            return

        self.coffee_table.setRowCount(0)

        for row in rows:
            row = row[1:]
            row_position = self.coffee_table.rowCount()
            self.coffee_table.insertRow(row_position)  # Добавляем новую строку
            for column in range(len(row)):
                item_data = str(row[column])
                if column == 2:
                    if item_data == '0':
                        item_data = 'Зерновой'
                    elif item_data == '1':
                        item_data = 'Молотый'
                item = QTableWidgetItem(item_data)
                self.coffee_table.setItem(row_position, column, item)

        conn.close()

    def create_coffe(self):
        self.add_coffee_window = AddWidget("create")
        self.add_coffee_window.show()

    def update_coffe(self):
        self.add_coffee_window = AddWidget('update')
        self.add_coffee_window.show()


class AddWidget(QMainWindow):
    def __init__(self, mode):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.comboBox.addItems(["В зернах", "Молотый"])
        if mode == 'update':
            self.pushButton.clicked.connect(self.update_coffee)
        else:

            self.pushButton.clicked.connect(self.add_coffee)

        '''a = self.plainTextEdit_3.toPlainText()
        b = self.plainTextEdit_4.toPlainText()
        print(a)'''

    def check(self):
        if self.plainTextEdit.toPlainText() and self.plainTextEdit_2.toPlainText() and self.plainTextEdit_5.toPlainText():
            a = self.plainTextEdit_3.toPlainText()
            b = self.plainTextEdit_4.toPlainText()
            pattern = r"^[-+]?\d+(\.\d+)?$"
            if a.isdigit() and bool(re.match(pattern, b)):
                return True
        return False

    def add_coffee(self):
        if self.check():
            try:
                name = self.plainTextEdit.toPlainText()
                roast_level = self.plainTextEdit_2.toPlainText()
                ground = 1 if self.comboBox.currentText() == 'Молотый' else 0  # Определяем тип кофе
                taste_description = self.plainTextEdit_5.toPlainText()
                price = float(self.plainTextEdit_3.toPlainText())
                package_volume = self.plainTextEdit_4.toPlainText()

                conn = sqlite3.connect('coffee.sqlite')
                cursor = conn.cursor()

                cursor.execute('''
                       INSERT INTO coffee (name, roast_level, ground, taste_description, price, package_volume)
                       VALUES (?, ?, ?, ?, ?, ?)
                   ''', (name, roast_level, ground, taste_description, price, package_volume))

                conn.commit()
                conn.close()
                self.statusBar().showMessage('успешный успех')

            except Exception as e:
                print(f"Произошла ошибка: {e}")
        else:
            self.statusBar().showMessage('Неверно заполнена форма')

    def update_coffee(self):
        if self.check():
            try:
                conn = sqlite3.connect('coffee.sqlite')
                cursor = conn.cursor()

                name = self.plainTextEdit.toPlainText()
                roast_level = self.plainTextEdit_2.toPlainText()
                ground = 1 if self.comboBox.currentText() == 'Молотый' else 0
                taste_description = self.plainTextEdit_5.toPlainText()
                price = float(self.plainTextEdit_3.toPlainText())
                package_volume = self.plainTextEdit_4.toPlainText()
                cursor.execute("SELECT id FROM coffee WHERE name = ?", (name,))
                idi = cursor.fetchone()
                cursor.execute('''
                       UPDATE coffee 
                       SET name=?, roast_level=?, ground=?, taste_description=?, price=?, package_volume=?
                       WHERE id=?
                   ''', (name, roast_level, ground, taste_description, price, package_volume, idi[0]))

                conn.commit()
                conn.close()
                self.statusBar().showMessage("Информация о кофе успешно обновлена.")
            except Exception as e:
                print(f"Ошибка при обновлении данных: {e}")
        else:
            self.statusBar().showMessage('Неверно заполнена форма')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec())
