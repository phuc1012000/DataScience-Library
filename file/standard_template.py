import os
from phuc import file

def save_data_path(PROJECT_DIR= os.getcwd().split('/src')[0],
                   ignore_dir = [],
                   endswith=['csv', 'pkl']):

    def _ignore(dirname):
        if dirname.startswith("."): return True
        if dirname in ignore_dir: return True

        return False

    def _check_unwanted(file_path):
        if os.path.isfile(file_path):
            for end in endswith:
                if file_path.endswith(end): return False
        return True


    if not (isinstance(PROJECT_DIR,str)):
        raise TypeError("Expect path is string")

    elif not (os.path.exists(PROJECT_DIR)):
        raise ValueError("Path not exist")

    data_path = PROJECT_DIR + '/data_path.pkl'

    if os.path.exists(data_path):
        DATA_DIR = file.load_pickle(data_path)

        # remove missing file
        missing_files = []
        for key, value in DATA_DIR.items():
            if not os.path.exists(value):
                missing_files.append(key)

        for missing_file in missing_files:
            del(DATA_DIR[missing_file])

        del(missing_files)

    else:
        print("Missing data_path.pkl")
        print("Generate new data_path.pkl")

        DATA_DIR = {
                    'DIRS':{'PROJECT_DIR': PROJECT_DIR},
                    'FILES':{}
                    }

    for scan_file in ['/data','/outputs'] :
        for dirpath, _ , filenames in os.walk(PROJECT_DIR + scan_file):
            dirname = dirpath.split("/")[-1]

            if _ignore(dirname):
                continue

            key = (dirname + '_dir').upper()

            if key in DATA_DIR['DIRS'].keys(): # check duplicate new name
                if (DATA_DIR['DIRS'][key] != dirpath):
                    print("Duplicate Name", key)
                    print(dirpath)
                    print(DATA_DIR['DIRS'][key])
            else:
                DATA_DIR['DIRS'][key] = dirpath

            for file_name in filenames:
                file_path = os.path.join(dirpath, file_name)
                if not _check_unwanted(file_path):
                    # change the end name . to _
                    key = (file_name + '_path').upper().replace('.', '_')
                    DATA_DIR['FILES'][key] = file_path

    file.save_pickle(data_path, DATA_DIR)
