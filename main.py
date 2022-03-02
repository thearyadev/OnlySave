from OnlySave import OnlySave
from tkinter import Tk

import time


def main():
    root = Tk()
    window = OnlySave(root)
    window.init_browser()
    root.mainloop()


if __name__ == "__main__":
    main()
