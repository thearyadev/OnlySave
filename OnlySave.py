from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from PIL import Image, ImageTk
import sys
from seleniumwire import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
import uuid

import time
import shutil

import os


def relative_to_assets(path: str):
    return "./assets/" + path


class OnlySave:
    BG_COLOR = "#261C2C"
    BTN_COLOR = "#5C527F"
    TEXT_COLOR = "#6E85B2"
    BOX_COLOR = "#3E2C41"
    CARAT_COLOR = "#FFFFFF"

    def __init__(self, master):
        self.master = master
        self.build()

    def init_browser(self):
        self.ONLYFANS = "https://onlyfans.com/"
        options = webdriver.ChromeOptions()
        options.binary_location = r"CHROME/chrome.exe"
        options.add_argument("--log-level=OFF")
        args = ["hide_console", ]
        self.driver = webdriver.Chrome("CHROME/chromedriver.exe", options=options, service_args=args)
        self.driver.get(self.ONLYFANS)
        self.scrolling = False
        self.current_user = None

    def start_program(self):
        self.current_user = self.entry_1.get()
        if self.current_user:
            self.driver.get(self.ONLYFANS + self.current_user)

    def toggleScroll(self):
        if not self.scrolling:
            # start scrolling, change var to is scrolling
            # loop scrolling; if scrolling changes to False again; break
            self.scrolling = True
            while self.scrolling:
                img = PhotoImage(file=relative_to_assets("scroll-button-active.png"))
                self.button_3.configure(
                    image=img
                )
                self.button_3.image = img
                # start scrolling
                self.driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);")
                # update master
                self.master.update()

            img = PhotoImage(file=relative_to_assets("scroll-button-inactive.png"))
            self.button_3.configure(
                image=img
            )
            self.button_3.image = img
        else:
            self.scrolling = False

    def parse_and_download(self):

        def update_preview(canvas, new_image):
            canvas.delete("preview_image")
            canvas.delete("preview_label")
            i = Image.open(new_image)
            pil_tk = ImageTk.PhotoImage(i)
            width, height = i.size
            basewidth = 400
            wpercent = (basewidth / float(i.size[0]))
            hsize = int((float(i.size[1]) * float(wpercent)))
            i = i.resize((basewidth, hsize), Image.ANTIALIAS)
            pil_tk = ImageTk.PhotoImage(i)

            self.image_1 = canvas.create_image(
                835,
                350,
                image=pil_tk,
                tags="preview_image"
            )
            self.master.update()

        data = self.driver.requests

        if self.current_user:
            try:  # make new dir with the onlyfans account name
                os.mkdir("./" + self.current_user)
            except FileExistsError:
                shutil.rmtree("./" + self.current_user)  # if it exists, delete the existing one.
            finally:
                try:
                    os.mkdir("./" + self.current_user)  # try and make it again
                except FileExistsError:
                    pass
        else:
            return

        for i, request in enumerate(data):
            if request.url.startswith("https://cdn2."):
                try:
                    self.canvas.itemconfigure(self.prompt, text=f"Downloading: {i + 1} of {len(data)}")
                    image_path = "./" + self.current_user + "/" + uuid.uuid4().hex + ".gif"
                    with open(image_path, "wb") as image_file:
                        image_file.write(requests.get(request.url).content)
                        update_preview(self.canvas, image_path)
                except:
                    pass

        for f in os.listdir("./" + self.current_user):
            os.rename("./" + self.current_user + "/" + f, "./" + self.current_user + "/" + f.replace("gif", "jpg"))

        self.build()

    def build(self):
        self.master.title("OnlySave")
        self.master.iconbitmap("assets/logo.ico")
        self.master.geometry("1120x700")
        self.master.configure(bg=self.BG_COLOR)
        self.master.resizable(False, False)
        try:
            del self.driver.requests
            self.current_user = None
        except Exception as e:
            pass
        self.canvas = Canvas(
            self.master,
            bg=self.BG_COLOR,
            height=700,
            width=1120,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        self.canvas.place(x=0, y=0)
        self.image_image_1 = PhotoImage(
            file=relative_to_assets("image_1.png"))
        image_1 = self.canvas.create_image(
            837.0,
            344.0,
            image=self.image_image_1,
            tags="preview_image"
        )

        self.title = self.canvas.create_text(
            110.0,
            137.0,
            anchor="nw",
            text="OnlySave",
            fill=self.TEXT_COLOR,
            font=("Poppins Medium", 30 * -1),
        )

        self.canvas.create_text(
            715.0,
            324.0,
            anchor="nw",
            text="Preview will be displayed here. ",
            fill="#FFFFFF",
            font=("Poppins Regular", 16 * -1),
            tags="preview_label"
        )

        self.prompt = self.canvas.create_text(
            110.0,
            182.0,
            anchor="nw",
            text="Login, then enter an account name. ",
            fill=self.TEXT_COLOR,
            font=("Poppins Regular", 16 * -1)
        )

        self.canvas.create_text(
            110.0,
            236.0,
            anchor="nw",
            text="Enter an OnlyFans account name",
            fill=self.TEXT_COLOR,
            font=("Poppins Medium", 13 * -1)
        )

        self.canvas.create_rectangle(
            110.0,
            298.0,
            456.1128234863281,
            299.5553436279297,
            fill=self.BOX_COLOR,
            outline="")

        button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))
        self.button_1 = Button(
            image=button_image_1,
            bg=self.BTN_COLOR,
            activebackground=self.BG_COLOR,
            disabledforeground=self.BG_COLOR,
            borderwidth=0,
            highlightthickness=1,
            command=self.start_program,
            relief="flat"
        )
        self.button_1.image = button_image_1

        self.button_1.place(
            x=110.0,
            y=315.0,
            width=346.0,
            height=40.0
        )

        button_image_2 = PhotoImage(
            file=relative_to_assets("button_2.png"))
        self.button_2 = Button(
            image=button_image_2,
            activebackground=self.BG_COLOR,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: os.startfile(os.getcwd()),
            relief="flat"
        )
        self.button_2.image = button_image_2
        self.button_2.place(
            x=26.0,
            y=629.0,
            width=50.0,
            height=50.0
        )

        button_image_3 = PhotoImage(
            file=relative_to_assets("scroll-button-inactive.png"))
        self.button_3 = Button(
            image=button_image_3,
            bg=self.BTN_COLOR,
            activebackground=self.BG_COLOR,
            borderwidth=0,
            highlightthickness=0,
            command=self.toggleScroll,
            relief="flat"
        )
        self.button_3.image = button_image_3
        self.button_3.place(
            x=110.0,
            y=365.0,
            width=115.48956298828125,
            height=40.0
        )

        button_image_4 = PhotoImage(
            file=relative_to_assets("button_4.png"))
        self.button_4 = Button(
            image=button_image_4,
            bg=self.BTN_COLOR,
            activebackground=self.BG_COLOR,
            borderwidth=0,
            highlightthickness=0,
            command=self.parse_and_download,
            relief="flat"
        )
        self.button_4.image = button_image_4
        self.button_4.place(
            x=230.0,
            y=365.0,
            width=226.0,
            height=40.0
        )

        entry_image_1 = PhotoImage(
            file=relative_to_assets("entry_1.png"))
        entry_bg_1 = self.canvas.create_image(
            283.0,
            279.5,
            image=entry_image_1
        )
        self.entry_1 = Entry(
            fg="white",
            bd=0,
            bg=self.BG_COLOR,
            disabledbackground=self.BG_COLOR,
            highlightthickness=0,
            insertbackground=self.CARAT_COLOR,
            font=("Poppins Medium", 13 * -1)
        )
        self.entry_1.place(
            x=110.0,
            y=262.0,
            width=346.0,
            height=33.0
        )

        self.canvas.create_rectangle(
            556.0,
            33.0,
            560.0,
            651.0,
            fill="#5C527F",
            outline="")


if __name__ == "__main__":
    root = Tk()
    window = OnlySave(root)
    window.init_browser()
    root.mainloop()
