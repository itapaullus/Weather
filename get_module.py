import importlib.util, os, pip
from urllib.request import urlretrieve
def checkmodule(module):
    module_spec = importlib.util.find_spec(module)
    if module_spec is None:
        print("Module " + module + " not found")
        return None
    else:
        print("Module {} can be imported".format(module))
        return module_spec


def import_module_from_spec(module_spec):
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module


def get_module_from_web(module):#asd
    if not os.path.exists('./tmpmodule'):
        os.mkdir("./tmpmodule")
    destination = "./tmpmodule/SQLAlchemy.tar.gz"
    url = "https://files.pythonhosted.org/packages/25/c9/b0552098cee325425a61efdf380c51b5c721e459081c85bbb860f501c091" \
          "/SQLAlchemy-1.2.12.tar.gz "
    urlretrieve(url, destination)
    # os.system('mkdir tmp')
    os.system('pip install {}'.format('SQLAlchemy'))
    # pip.main(['install', 'SQLAlchemy'])
    # module_spec = checkmodule('fake_module')
    # module_spec = checkmodule('collections')
    # if module_spec:
    #     module = import_module_from_spec(module_spec)
    #     print(dir(module))


# get_module_from_web('sde')

os.system('cmd')
os.error
