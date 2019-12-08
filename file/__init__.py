import  zipfile
import os
from phuc.data_process import memory
import pickle


def _unzip(root,file,unzip_file_dir,recursive,delete):
    if file.endswith('.zip'):

        zip_file_path = os.path.join(root,file)
        unzip_file_path = os.path.join(unzip_file_dir, file[:-4])

        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(unzip_file_path)
            print('unzip to' + unzip_file_path )

        if delete:
            os.remove(zip_file_path)
            print('Deleted file' + file)

        if recursive:
            unzip(unzip_file_path, delete = delete)

def unzip(zip_file_dir, unzip_file_dir = None, recursive = True, delete = False):

    if unzip_file_dir == None:
        unzip_file_dir = zip_file_dir

    if os.path.isdir(zip_file_dir):
        for root, _, files in os.walk(zip_file_dir):
            for file in files:
                _unzip(root,file,unzip_file_dir,recursive,delete)

    elif os.path.isfile(zip_file_dir):
        if zip_file_dir.endswith('.zip'):
            root, file = zip_file_dir.rsplit('/',1)
            _unzip(root,file,unzip_file_dir,recursive,delete)
    else:
        print('Dir or File not exist')



def create_dir(dirName):
    if not os.path.exists(dirName):
        os.mkdir(dirName)
        print("Directory " , dirName ,  " Created ")
    else:
        print("Directory " , dirName ,  " already exists")

def delete_file(path):
    if os.path.exists(path):
        os.remove(path)
        print('Deleted file' + path.rsplit('/',1)[1])
    else:
        print("The file does not exist")



def save_pickle(pickle_save_path,file,reduce_mem_usage =[None, False, -2], remove_memory = False ):

    pickle_save_dir , file_name= pickle_save_path.rsplit('/',1)
    create_dir(pickle_save_dir)

    if reduce_mem_usage is not None :
        file = memory.Reducer(reduce_mem_usage).reduce(file)

    with open(pickle_save_path, 'wb') as f:
        pickle.dump(file, f)
        print('Saved file ' + file_name)

    if remove_memory:
        print('removed {} data'.format(file))
        file = None

def load_pickle(pickle_file_path):

    if os.path.isfile(pickle_file_path) and pickle_file_path.endswith('.pkl'):

        with open(pickle_file_path, 'rb') as f:
            print('Loaded file {}'.format(pickle_file_path.rsplit('/',1)[1]))
            return pickle.load(f)
    else:
        print ("File not exist")
        return None
