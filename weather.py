import urllib.request,os,zipfile,gzip,shutil,json,weather_ui, urllib.error as er
from configparser import ConfigParser, NoOptionError
from termcolor import colored
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QSize, Qt
class City:
    def __init__(self,dct):
        self.id = dct['id']
        self.name = dct['name']
        self.country = dct['country']
        self.coord = dict(lon=dct['coord']['lon'],lat=dct['coord']['lat'])

def err_print(string):
    print(colored(string, 'red'))

def ok_print(string):
    print(colored(string, 'green'))

def saveconfig(cfg):
    with open(cfg.get("Settings", "main_path") + '/Settings.ini', "w") as config_file:
        cfg.write(config_file)


##Стартовые проверки настроек и служебных файлов
def install():
    """
Первоначальная установка необходимых файлов
    """
    print('Устанавливаем объекты...')
    mainpath = './kim_weather'
    if not os.path.exists(mainpath):
        print('    Создаю директорию для локальных настроек...')
        os.makedirs(mainpath)
    else:
        print('    Директория {} уже существует...'.format(mainpath))

    cfgpath = mainpath+"/settings.ini"

    if not os.path.exists(cfgpath):
        print("Создаю конфиг-файл...")
        config: ConfigParser = ConfigParser()
        config.add_section("Settings")
        config.set("Settings", "main_path", mainpath)
        config.set("Settings", "city_path", mainpath+'/city')
        config.set("Settings", "city_url", 'http://bulk.openweathermap.org/sample/city.list.json.gz')
        saveconfig(config)
    else:
        print("    Читаю конфигурацию...")
        config = getCfgParam()

    # Создаем директорию для городов
    try:
        citypath = config.get("Settings", "city_path")
    except NoOptionError:
        err_print('    "city_path": значение атрибута в {} не найдено!'.format(cfgpath))
        return False

    if not os.path.exists(citypath):
        print('    Создаю директорию {} для списка городов...'.format(citypath))
        os.makedirs(citypath)
    else:
        print('    Директория {} уже существует...'.format(citypath))

    # Загружаем список городов
    zip_city = citypath+"/city_list"
    if not os.path.exists(zip_city+".json"):
        print("    Загружаю с openweathermap.org список городов...")
        try:
            url = config.get("Settings", "city_url")
            urllib.request.urlretrieve(url,zip_city+".gz")
        except er.URLError:
            err_print('    Указанный в конфигурации URL недоступен! {}'.format(url))
            err_print('    Проверьте валидность URL в файле {}!'.format(cfgpath))
            return False
        except er.HTTPError:
            err_print('    Ошибка загрузки файла city_list! Проверьте интернет-соединение')
            return False
        config.set("Settings", "city_file", zip_city+".json")
        print("    Распаковываю файл...")
        with gzip.open(zip_city+".gz", 'rb') as f_in:
            with open(zip_city+'.json', 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        print("    Удаляю архив...")
        os.remove(zip_city+".gz")
    else:
        print('    Список городов уже загружен...')
    ok_print("kim_weather успешно установлен!")


def check_install(): # Проверяем корректность установки
    """
Проверяем целостность необходимых файлов
    :return: null
    """
    if not os.path.exists("./kim_weather/settings.ini"):
        print('Отсутствует файл settings.ini. Проведите повторную инсталляцию!')
        return False
    if not os.path.exists('./kim_weather/city/city_list.json'):
        print('Отсутствует файл city_list.json. Проведите повторную инсталляцию!')
        return False
    cfg = getCfgParam()
    try:
        cfg.get('Settings', 'main_path')
    except NoOptionError:
        err_print('Не установлено значение атрибута "main_path"!')
        return False

    try:
        cfg.get('Settings', 'city_path')
    except NoOptionError:
        err_print('Не установлено значение атрибута "city_path"!')
        return False
    return True


def getCfgParam():
    cfg = ConfigParser() #Считаем конфиг файл
    cfg.read("./kim_weather/Settings.ini")
    return cfg


class City:
    def __init__(self, id, name, country, coord):
        self.id = id
        self.name = name
        self.country = country
        self.coord = coord

def readCityList(path):
    with open(path, 'r', encoding='utf-8') as read_file:
        datalist = json.load(read_file)
    data = dict()
    for city in datalist:
        data[city['id']] = City(city['id'], city['name'], city['country'], city['coord'])
    return data

def setmydata(self):
    for column, key in enumerate(self.data):
        for row, item in enumerate(self.data[key]):
            newitem = QTableWidgetItem(item)
            self.setItem(row, column, newitem)




# install()
cfg = getCfgParam()
cfg.set('Settings', 'city_file', './kim_weather/city/city_list.json')
saveconfig(cfg)
data = readCityList(cfg.get('Settings','city_file'))

# readCityList('./kim_weather/city/city_list.json')
# in_city = input("Введите интересующий город\n")

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
        table.horizontalHeaderItem(4).setTextAlignment(Qt.AlignHCenter)

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