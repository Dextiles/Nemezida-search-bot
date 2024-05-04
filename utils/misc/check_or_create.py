import os


def check_or_create_file(path):
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path, 'w'):
        pass
