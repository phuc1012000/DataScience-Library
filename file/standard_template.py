import os
from phuc import file


def save_data_path(PROJECT_DIR=os.getcwd().split('/src')[0],
                   endswith=['csv', 'pkl'],
                   ignore_dir=['.git', '.ipynb_checkpoints', '.gitignore']):

    DATA_DIR = {'DATA_DIR': PROJECT_DIR + '/data_path.pkl'}

    def _ignore(dirpath):
        for ignore in ignore_dir:
            if ignore in dirpath:
                return True
        return False

    def _check_unwanted(file_path, file_name):
        if os.path.isfile(file_path):
            for end in endswith:
                if file_name.endswith(end):
                    return False
            return True
        else:
            return True

    for dirpath, dirnames, _ in os.walk(PROJECT_DIR + '/data'):
        for dirname in dirnames:
            full_dir = os.path.join(dirpath, dirname)
            if _ignore(full_dir):
                continue

            file_names = os.listdir(full_dir)
            if len(file_names) == 0:
                key = (dirname + '_dir').upper()
                DATA_DIR[key] = full_dir
            elif len(file_names) == 1 and _ignore(file_names[0]):
                key = (dirname + '_dir').upper()
                DATA_DIR[key] = full_dir

            else:
                for file_name in file_names:
                    file_path = os.path.join(full_dir, file_name)
                    if _check_unwanted(file_path, file_name):
                        if os.path.isfile(file_path):
                            key = (dirname + '_dir').upper()
                            DATA_DIR[key] = full_dir
                            break
                        continue

                    key = (file_name + '_path').upper().replace('.', '_')
                    DATA_DIR[key] = file_path

    file.save_pickle(DATA_DIR['DATA_DIR'], DATA_DIR)
