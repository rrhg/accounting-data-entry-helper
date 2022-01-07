from pathlib import Path


def create_dir_w_parents(path):
    # If parents is true, any missing parents of this path are created as needed;
    p = Path(path)
    try:
        p.mkdir(parents=True, exist_ok=True)
    except FileExistsError:
        pass
    return p