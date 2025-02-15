import sys
import sqlite3
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMainWindow, QTableWidget, QPushButton, QVBoxLayout, QWidget, QTableWidgetItem

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

    def load_coffee_data(self):
        """Загружает данные о кофе из базы данных и отображает их в QTableWidget."""
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
                item = QTableWidgetItem(str(row[column]))
                self.coffee_table.setItem(row_position, column, item)  # Устанавливаем значение в ячейку

        conn.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec())
