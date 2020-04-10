from sys import argv

from utils import check_update


def cmd_init():
    check_update()


if __name__ == "__main__":
    if "init" in argv:
        cmd_init()
