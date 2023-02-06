import cv2
import os.path
from tkinter import *
from tkinter import messagebox as mb
from PIL import Image, ImageTk

capture = cv2.VideoCapture(0)


class App(Tk):
    def __init__(self):
        super().__init__()

        self.title("Фото с камеры")
        self.geometry('335x250')

        self.make_photo = Button(
            self, text="Сделать фото", command=self.make_capture)
        self.make_photo.grid(row=0, column=1)

        self.show_photo = Button(
            self, text="Показать фото", command=self.show_capture)
        self.show_photo.grid(row=0, column=2)
        self.show_photo["state"] = "disabled"

        self.show_negative_photo = Button(
            self, text="Показать негативное фото", command=self.show_negative_capture)
        self.show_negative_photo.grid(row=0, column=3)
        self.show_negative_photo["state"] = "disabled"

    def make_capture(self):
        if not os.path.exists("photo.bmp") or os.path.exists("negative_photo.bmp"):
            ret, frame = capture.read()
            cv2.imwrite("photo.bmp", frame)

            ret, frame = capture.read()
            for string in frame:
                for pixel in string:
                    pixel[0] = 255 - pixel[0]
                    pixel[1] = 255 - pixel[1]
                    pixel[2] = 255 - pixel[2]
            cv2.imwrite("negative_photo.bmp", frame)

            # mb.showinfo(message="Фото сделано!")
            self.show_photo["state"] = "normal"
            self.show_negative_photo["state"] = "normal"
            self.top_level = Top("photo.bmp")
        else:
            os.remove("photo.bmp")
            os.remove("negative_photo.bmp")
            self.make_capture()

    def show_capture(self):
        self.top_level = Top("photo.bmp")

    def show_negative_capture(self):
        self.top_level = Top("negative_photo.bmp")


class Top(Toplevel):
    def __init__(self, name):
        super().__init__()
        self.title('Фото')
        self.geometry('640x480')
        self.img = ImageTk.PhotoImage(Image.open(name))
        self.panel = Label(self, image=self.img)
        self.panel.pack(side="bottom", fill="both", expand="no")


if __name__ == '__main__':
    app = App()
    app.mainloop()
