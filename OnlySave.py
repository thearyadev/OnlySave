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

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str):
    return "./assets/" + path


class OnlySave:
    def __init__(self, master):
        self.master = master
        self.master.title("OnlySave")
        self.master.iconbitmap("assets/logo.ico")
        self.master.resizable(False, False)
        self.master.geometry("1440x900")
        self.master.configure(bg="#FFFFFF")
        self.canvas = Canvas(
            master,
            bg="#FFFFFF",
            height=900,
            width=1440,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        self.canvas.place(x=0, y=0)
        self.image_image_1 = PhotoImage(
            file=relative_to_assets("image_1.png"))

        image_1 = self.canvas.create_image(
            1045.0,
            449.0,
            image=self.image_image_1,
            tags="preview_image"
        )

        self.canvas.create_text(
            124.0,
            150.0,
            anchor="nw",
            text="OnlySave",
            fill="#000000",
            font=("Poppins Medium", 30 * -1)

        )

        self.canvas.create_text(
            923.0,
            437.0,
            anchor="nw",
            text="Preview will be displayed here. ",
            fill="#FFFFFF",
            font=("Poppins Regular", 16 * -1),
            tags="preview_label"
        )

        self.canvas.create_text(
            124.0,
            195.0,
            anchor="nw",
            text="Login using the web browser.\nOnce logged in, enter an account name and press the start button.",
            fill="#000000",
            font=("Poppins Regular", 16 * -1)
        )

        self.canvas.create_text(
            124.0,
            256.0,
            anchor="nw",
            text="Enter the OnlyFans account name you would like to download from",
            fill="#999999",
            font=("Poppins Medium", 13 * -1)
        )

        self.canvas.create_rectangle(
            124.0,
            318.0,
            569.0,
            320.0,
            fill="#000741",
            outline="")

        button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))
        self.button_1 = Button(
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.start_program,
            relief="flat"
        )

        self.button_1.image = button_image_1

        self.button_1.place(
            x=124.0,
            y=362.0,
            width=429.0,
            height=53.0
        )

        button_image_2 = PhotoImage(
            file=relative_to_assets("SCROLL_ENABLED.png"))
        self.button_2 = Button(
            image=button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.toggleScroll,
            relief="flat"
        )
        self.button_2.image = button_image_2
        self.button_2.place(
            x=122.0,
            y=430.0,
            width=183.0,
            height=53.0
        )

        button_image_3 = PhotoImage(
            file=relative_to_assets("button_3.png"))
        self.button_3 = Button(
            image=button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=self.parse_and_download,
            relief="flat"
        )
        self.button_3.image = button_image_3
        self.button_3.place(
            x=316.0,
            y=430.0,
            width=237.0,
            height=53.0
        )

        entry_image_1 = PhotoImage(
            file=relative_to_assets("entry_1.png"))
        self.entry_bg_1 = self.canvas.create_image(
            346.5,
            298.5,
            image=entry_image_1
        )
        self.entry_1 = Entry(
            bd=0,
            bg="#FFFFFF",
            highlightthickness=0
        )
        self.entry_1.place(
            x=124.0,
            y=281.0,
            width=445.0,
            height=33.0
        )

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
            self.entry_1.config(state="disabled")
            self.button_1.config(state="disabled")
            self.driver.get(self.ONLYFANS + self.current_user)

    def toggleScroll(self):
        if not self.scrolling:
            # start scrolling, change var to is scrolling
            # loop scrolling; if scrolling changes to False again; break
            self.scrolling = True
            while self.scrolling:
                img = PhotoImage(file=relative_to_assets("SCROLL_DISABLED.png"))
                self.button_2.configure(
                    image=img
                )
                self.button_2.image = img
                # start scrolling
                self.button_2.after(1000, lambda: self.driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);"))
                # update master
                self.master.update()

            img = PhotoImage(file=relative_to_assets("SCROLL_ENABLED.png"))
            self.button_2.configure(
                image=img
            )
            self.button_2.image = img
        else:
            self.scrolling = False

    def parse_and_download(self):

        def update_preview(canvas, new_image):
            canvas.delete("preview_image")
            canvas.delete("preview_label")
            i = Image.open(new_image)
            pil_tk = ImageTk.PhotoImage(i)
            width, height = i.size
            basewidth = 800
            wpercent = (basewidth / float(i.size[0]))
            hsize = int((float(i.size[1]) * float(wpercent)))
            i = i.resize((basewidth, hsize), Image.ANTIALIAS)
            pil_tk = ImageTk.PhotoImage(i)

            self.image_1 = canvas.create_image(
                1045.0,
                449.0,
                image=pil_tk,
                tags="preview_image"
            )
            self.master.update()

        data = self.driver.requests

        try:  # make new dir with the onlyfans account name
            os.mkdir("./" + self.current_user)
        except FileExistsError:
            shutil.rmtree("./" + self.current_user)  # if it exists, delete the existing one.
        finally:
            try:
                os.mkdir("./" + self.current_user)  # try and make it again
            except FileExistsError:
                pass

        for request in data:
            if request.url.startswith("https://cdn2."):
                try:
                    image_path = "./" + self.current_user + "/" + uuid.uuid4().hex + ".gif"
                    with open(image_path, "wb") as image_file:
                        image_file.write(requests.get(request.url).content)
                        update_preview(self.canvas, image_path)
                except:
                    pass

        for f in os.listdir("./" + self.current_user):
            os.rename("./" + self.current_user + "/" + f, "./" + self.current_user + "/" + f.replace("gif", "jpg"))

        self.master.destroy()
        self.driver.quit()
        os.startfile("OnlySave.exe")


if __name__ == "__main__":
    root = Tk()
    window = OnlySave(root)
    root.mainloop()
