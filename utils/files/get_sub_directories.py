from pathlib import Path


def get_sub_directories(dir_path):
    subs = []
    # rootdir = 'path/to/dir'
    for path in Path(dir_path).iterdir():
        if path.is_dir():
            # print(path)
            subs.append( path.name )

    return subs
 