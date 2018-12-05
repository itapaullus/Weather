import configparser,urllib.request,os,zipfile,gzip,shutil,json,weather_ui
from configparser import ConfigParser
class City:
    def __init__(self,dct):
        self.id = dct['id']
        self.name = dct['name']
        self.country = dct['country']
        self.coord = dict(lon=dct['coord']['lon'],lat=dct['coord']['lat'])
def createConfig(path,dct):
    config = configparser.ConfigParser()
    config.add_section("Settings")
    config.set("Settings","main_path",dct["main_path"])
    config.set("Settings","city_path",dct["city_path"])
    config.add_section("My Cities")
    config.set("My Cities","city_list","")
    with open(path,"w") as config_file:
        config.write(config_file)
##Стартовые проверки настроек и служебных файлов
def install():
    """
Первоначальная установка необходиых файлов
    """
    mainpath = './kim_weather'
    if not os.path.exists(mainpath):
        print('Создаю директорию для локальных настроек...')
        os.makedirs(mainpath)
    citypath = mainpath+'/city'
    if not os.path.exists(citypath):
        print('Создаю директорию для списка городов...')
        os.makedirs(citypath)
    zip_city = mainpath+"/city/city_list"
    if not os.path.exists(zip_city+".json"):
        print("Загружаю с openweathermap.org список городов...")
        url = 'http://bulk.openweathermap.org/sample/city.list.json.gz'
        urllib.request.urlretrieve(url,zip_city+".gz")
        print("Распаковываю файл...")
        with gzip.open(zip_city+".gz", 'rb') as f_in:
            with open(zip_city+'.json', 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        print("Удаляю архив...")
        os.remove(zip_city+".gz")
        print("Успешно!")
    cfgpath = mainpath+"/settings.ini"
    if not os.path.exists(cfgpath):
        print("Создаю конфиг-файл...")
        createConfig(cfgpath,{"main_path": mainpath,"city_path": zip_city+'.json'})

def check_install(): # Проверяем корректность установки
    """
Проверяем целостность необходимых файлов
    :return: null
    """
    if not os.path.exists("./kim_weather/settings.ini"):
        print('Отсутствует файл settings.ini. Проведите повторную инсталляцию')
        return False
    if not os.path.exists('./kim_weather/city/city_list.json'):
        print('Отсутствует файл city_list.json. Проведите повторную инсталляцию')
        return False
    return True


def getCfgParam():
    cfg = ConfigParser() #Считаем конфиг файл
    cfg.read("./kim_weather/settings.ini")
    return cfg


def readCityList(path):
    with open(path, 'r', encoding='utf-8') as read_file:
        data = json.load(read_file)
    print(data[1])


if not check_install():
    install()
cfg = getCfgParam()
readCityList(cfg.get('Settings','city_path'))
# in_city = input("Введите интересующий город\n")


# with open(parser.get('Settings','city_path'), "r",encoding='utf-8') as read_file:
#     data = json.load(read_file)  # Уложили в data полный файл


# data2 = [item for item in data if item["name"].upper().find(in_city.upper()) != -1]
# if len(data2) == 1:
#     c = City(data2[0])
#     print('Город: '+c.name+'\n'+"Страна:" + c.country)
#     # c.savetocfg()
#     print(c.name)
# elif len(data2) > 1:
#     print("Много городов")
#     c = city_select(data2)
#     print('Город: '+c.name+'\n'+"Страна:" + c.country)
#     # c.savetocfg()
# elif len(data2) == 0:
#     print("По вашему запросу на найдено ни одного города")
