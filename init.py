import cv2
import numpy as np
import tkinter as tk
from tkinter import Button, Label, Frame
from PIL import Image, ImageTk
from ultralytics import YOLO
import pyautogui


class App:
    def __init__(self, root):
        self.root = root
        self.prepare_screen()
        self.model = YOLO("yolov5s.pt")
        self.start_video()

    def prepare_screen(self):
        self.root.title("Detecção de Bola de Vôlei com YOLOv5")

        self.video_frame = Frame(root)
        self.video_frame.pack()

        self.video_label = Label(self.video_frame)
        self.video_label.pack()

        self.options_frame = Frame(root)
        self.options_frame.pack()

        self.close_button = Button(
            self.options_frame,
            text="Fechar",
            command=self.close_window
        )
        self.close_button.pack(side="left")
        self.running = False

    def start_video(self):
        self.running = True
        self.show_video()

    def show_video(self):
        if self.running:
            screenshot = pyautogui.screenshot()
            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            results = self.model(frame)

            for result in results:
                boxes = result.boxes
                for box in boxes:
                    cls = int(box.cls[0])
                    label = self.model.names[cls]
                    self.highlight_ball(label=label, frame=frame, box=box)

            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)

            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)

            self.root.after(10, self.show_video)

    def highlight_ball(self, label, frame, box):
        if label == "sports ball":
            x1, y1, x2, y2 = box.xyxy[0]
            conf = box.conf[0]
            cv2.rectangle(
                frame,
                (int(x1), int(y1)),
                (int(x2), int(y2)),
                (0, 255, 0),
                2,
            )
            cv2.putText(
                frame,
                f'Bola {conf:.2f}',
                (int(x1), int(y1) - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2,
            )

    def close_window(self):
        self.running = False
        self.root.quit()


root = tk.Tk()
app = App(root)
root.mainloop()
