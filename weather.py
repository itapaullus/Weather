import urllib.request, os, gzip, shutil, json, urllib.error as er
from configparser import ConfigParser, NoOptionError
from termcolor import colored


def err_print(string):
    print(colored(string, 'red'))


def ok_print(string):
    print(colored(string, 'yellow'))


def ask_print(string):
    print(colored(string, 'blue'))


def saveconfig(cfg):
    with open(cfg.get("Settings", "main_path") + '/Settings.ini', "w") as config_file:
        cfg.write(config_file)


# Стартовые проверки настроек и служебных файлов
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
        config.set("Settings", "city_file", mainpath+'/city/' + 'city_list.json')
        saveconfig(config)
    else:
        print("    Читаю конфигурацию...")
        config = getcfgparam()

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
            urllib.request.urlretrieve(url, zip_city+".gz")
        except er.URLError:
            err_print('    Указанный в конфигурации URL недоступен! {}'.format(url))
            err_print('    Проверьте валидность URL в файле {}!'.format(cfgpath))
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
    print('Запускаем повторную проверку установки...')

    if check_install():
        ok_print("kim_weather успешно установлен!")
    else:
        err_print('Не удалось провести корректную установку. Попробуйте установить значений Settings.ini вручную')


def check_install():  # Проверяем корректность установки
    """
Проверяем целостность необходимых файлов
    :return: boolean
    """
    ok_print('Проверяем целостность установки...')
    if not os.path.exists("./kim_weather/Settings.ini"):
        err_print('Отсутствует файл settings.ini. Проведите повторную инсталляцию!')
        return False

    cfg = getcfgparam()
    try:
        main = cfg.get('Settings', 'main_path')
        ok_print('    main_path установлен: {}'.format(main))
    except NoOptionError:
        err_print('    Не установлено значение атрибута "main_path"!')
        return False

    try:
        citypath = cfg.get('Settings', 'city_path')
        ok_print('    city_path установлен: {}'.format(citypath))
    except NoOptionError:
        err_print('    Не установлено значение атрибута "city_path"!')
        return False

    try:
        url = cfg.get('Settings', 'city_url')
        ok_print('    city_url установлен: {}'.format(url))
    except NoOptionError:
        err_print('    Не установлено значение атрибута "city_url"')
        return False

    try:
        file = cfg.get('Settings', 'city_file')
        ok_print('    city_file установлен: {}'.format(file))
    except NoOptionError:
        err_print('    Не установлено значение атрибута "city_file"')
        return False
    ok_print('Проверено успешно')
    return True


def getcfgparam() -> ConfigParser:
    cfg = ConfigParser()  # Считаем конфиг файл
    cfg.read("./kim_weather/Settings.ini")
    return cfg


class City:
    def __init__(self, id, name, country, coord):
        self.id = id
        self.name = name
        self.country = country
        self.coord = coord


def read_city_list(path):
    with open(path, 'r', encoding='utf-8') as read_file:
        datalist = json.load(read_file)
    data = dict()
    for city in datalist:
        data[city['id']] = City(city['id'], city['name'], city['country'], city['coord'])
    return data


def ask_request_city(indata):
    ask_print('Введите интересующий город:')
    ask_resp = input()
    result = list()
    for key, value in indata.items():
        if ask_resp.upper() in value.name.upper():
            result.append(indata[key])
            print(str(len(result)) + ': ' + indata[key].country + ', ' + indata[key].name)
    len_result = len(result)
    if len_result == 0:
        print('Не найдено ни одного города. Попробуйте еще раз...')
        ask_request_city(indata)
    elif len_result == 1:
        print('Подтвердите выбор города: (y/n)')
        ans = input()
        if ans in ['Y', 'y']:
            return result[0]
        else:
            ask_request_city(indata)
    else:
        print('Нашлось дохуя, подумаю завтра')
    #     print(str(num) + ': '+i.name)


if not check_install():
    print('Проверка целостности файлов не пройдена')
    install()
cfg = getcfgparam()
data = read_city_list(cfg.get('Settings', 'city_file'))

ask_request_city(data)

# read_city_list('./kim_weather/city/city_list.json')
# in_city = input("Введите интересующий город\n")

