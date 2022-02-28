from tkinter import Tk, Label, Button, Canvas, PhotoImage, NW, Text, DISABLED, NORMAL
from PIL import Image, ImageTk
import sys
from seleniumwire import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
import uuid

from rich import print
import time
import shutil

import os


class OnlySave:
    def __init__(self, master):
        # window setup
        self.master = master
        self.master.geometry("500x500")
        master.title("OnlySave")
        self.title_label = Label(master, text="OnlySave")
        self.title_label.pack()
        self.prompt = Label(master, text="Log into OnlyFans using the web browser, then press start.", fg="#eb4034")
        self.textarea = Text(master, height=1, width=30)
        self.textarea.pack()
        self.prompt.pack()
        self.startBtn = Button(master, text='Start', width=50, height=3, command=self.get_page)  # starts program
        self.startBtn.pack()
        self.preview_label = Label(master, text="Currently downloading:")
        self.preview_label.pack()

        self.preview = Label(master)
        # self.preview.image = pil_tk_image
        self.preview.pack()

        self.ONLYFANS = "https://onlyfans.com/"
        options = webdriver.ChromeOptions()
        options.binary_location = r"CHROME/chrome.exe"
        self.driver = webdriver.Chrome("CHROME/chromedriver.exe", options=options)
        self.driver.get(self.ONLYFANS)

    def capture_and_parse(self):
        data = self.driver.requests  # gets all requests from the browser
        links = []  # stores all urls
        for request in data:
            if request.url.startswith("https://cdn2."):  # checks if it is a Onlyfans image.
                links.append(request.url)
        self.download(links)  # starts downloading all the links

    def download(self, links):
        try:  # make new dir with the onlyfans account name
            os.mkdir("./" + self.textarea.get("1.0", "end-1c"))
        except FileExistsError:
            shutil.rmtree("./" + self.textarea.get("1.0", "end-1c"))  # if it exists, delete the existing one.
        finally:
            try:
                os.mkdir("./" + self.textarea.get("1.0", "end-1c"))  # try and make it again
            except FileExistsError:
                pass

        self.startBtn['state'] = DISABLED  # disable button

        for link in links:
            try:
                time.sleep(0.5)  # avoid getting request timeout
                # save it as a gif to display in GUI
                path = "./" + self.textarea.get("1.0", "end-1c") + "/" + uuid.uuid4().hex + ".gif"
                with open(path, "wb") as file:  # open file
                    file.write(requests.get(link).content)  # request for the content and write
                    # download, write, show image
                    pil_image = Image.open(path)  # show image in gui
                    pil_image.thumbnail((400, 400))
                    pil_tk_image = ImageTk.PhotoImage(pil_image)
                    self.preview.configure(image=pil_tk_image)
                    self.preview.image = pil_tk_image
                    self.master.update()  # update screen
            except:
                pass  # skip if any errors. Output doesnt matter too much

        for f in os.listdir("./" + self.textarea.get("1.0", "end-1c")):  # renames all the files to .jpg
            os.rename("./" + self.textarea.get("1.0", "end-1c") + "/" + f,
                      "./" + self.textarea.get("1.0", "end-1c") + "/" + f.replace("gif", "jpg"))
        self.driver.close()  # ends the program. Didnt want to figure out resetting the screen lol
        self.master.destory()

        sys.exit(0)

    def get_page(self):
        self.driver.get(self.ONLYFANS + self.textarea.get("1.0", "end-1c"))  # gets page from submitted input
        self.textarea.pack_forget()  # hides textarea
        self.startBtn.configure(text="Begin Downloading")  # updates button
        self.prompt.configure(text="Currently listening for image data.. Press the button to capture and download.")
        self.startBtn.configure(command=self.capture_and_parse)  # next step with button press
