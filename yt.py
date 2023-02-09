from mytube import *

import getpass
os.system('cls' if os.name == 'nt' else 'clear')
lg = getpass.getpass(prompt='Login: ', stream=None)
pw = getpass.getpass(prompt='Password: ', stream=None)

main(False if lg != "greatestloser" or pw != "!g0t$2" else True)


"""
Not important but needed

def getFileCount(dir_path=r"C:/users/aarus/Downloaded_Youtube"):
    return int(len([entry for entry in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, entry))]))

"""