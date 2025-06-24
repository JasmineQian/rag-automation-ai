import os

def remove_pycache_dirs(root_dir='.'):
    """
    递归删除指定目录下所有 __pycache__ 文件夹
    :param root_dir: 项目根目录，默认为当前目录
    """
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if '__pycache__' in dirnames:
            pycache_path = os.path.join(dirpath, '__pycache__')
            print(f'正在删除: {pycache_path}')
            shutil.rmtree(pycache_path)

if __name__ == '__main__':
    remove_pycache_dirs('.')