import os

def create_database(dir_path):
    if('posted.csv' in os.listdir(dir_path)):
        return
    with open('posted.csv', 'w') as fp:
        pass
    with open('serialized_database.txt', 'w') as fp:
        pass

def create_folder(path):
    CHECK_FOLDER = os.path.isdir(path)
    # If folder doesn't exist, then create it.
    if not CHECK_FOLDER:
        os.makedirs(path)
