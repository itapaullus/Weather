# Наследуемся от QMainWindow
class MainWindow(QMainWindow):
    def setmydata(self):
        for column, key in enumerate(self.data):
            for row, item in enumerate(self.data[key]):
                newitem = QTableWidgetItem(item)
                self.setItem(row, column, newitem)
    # Переопределяем конструктор класса
    def __init__(self):
        # Обязательно нужно вызвать метод супер класса
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(640, 120))  # Устанавливаем размеры
        self.setWindowTitle("Работа с QTableWidget")  # Устанавливаем заголовок окна
        central_widget = QWidget(self)  # Создаём центральный виджет
        self.setCentralWidget(central_widget)  # Устанавливаем центральный виджет

        grid_layout = QGridLayout()  # Создаём QGridLayout
        central_widget.setLayout(grid_layout)  # Устанавливаем данное размещение в центральный виджет

        table = QTableWidget(self)  # Создаём таблицу
        table.setColumnCount(5)  # Устанавливаем три колонки
        table.setRowCount(len(data))  # и одну строку в таблице

        # Устанавливаем заголовки таблицы
        table.setHorizontalHeaderLabels(["Город", "Страна", "Ширина","Долгота","???"])

        # Устанавливаем всплывающие подсказки на заголовки
        table.horizontalHeaderItem(0).setToolTip("Город")
        table.horizontalHeaderItem(1).setToolTip("Страна")
        table.horizontalHeaderItem(2).setToolTip("Ширина")
        table.horizontalHeaderItem(3).setToolTip("Ширина")
        table.horizontalHeaderItem(4).setToolTip("Ширина")

        # Устанавливаем выравнивание на заголовки
        table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignHCenter)
        table.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)
        table.horizontalHeaderItem(2).setTextAlignment(Qt.AlignHCenter)
        table.horizontalHeaderItem(3).setTextAlignment(Qt.AlignHCenter)
        table.horizontalHeaderItem(4).setTextAlignment(Qt.AlignHCenter) #

        # заполняем первую строку
        i = 0
        for index, city in data.items():
            table.setItem(i, 0, QTableWidgetItem(city.name))
            table.setItem(i, 1, QTableWidgetItem(city.country))
            table.setItem(i, 2, QTableWidgetItem(city.coord.get('lon')))
            table.setItem(i, 3, QTableWidgetItem(city.coord.get('lat')))
            i += 1

        # делаем ресайз колонок по содержимому
        table.resizeColumnsToContents()

        grid_layout.addWidget(table, 0, 0)  # Добавляем таблицу в сетку

import sys
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())