import pyautogui
import tkinter as tk
from tkinter import Entry, Label, Button, messagebox
import threading
from pynput import mouse, keyboard


class ClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Clicker")

        self.num_iterations_label = Label(root, text="Number of Iterations:")
        self.num_iterations_label.pack()

        self.num_iterations_entry = Entry(root)
        self.num_iterations_entry.pack()

        self.set_coordinates_label = Label(root, text="Click 'Set Coordinates' then click on the screen.")
        self.set_coordinates_label.pack()

        self.set_coordinates_button = Button(root, text="Set Coordinates", command=self.start_tracking)
        self.set_coordinates_button.pack()

        self.start_button = Button(root, text="Start Clicking", command=self.start_clicking)
        self.start_button.pack()

        self.quit_button = Button(root, text="Quit", command=self.quit_app)
        self.quit_button.pack()

        self.click_coordinates = None
        self.num_iterations = None
        self.clicking = False
        self.tracking = False
        self.quit_requested = False

    def start_tracking(self):
        self.set_coordinates_label.config(text="Tracking mouse coordinates. Click on the screen to lock.")
        self.tracking = True

    def set_coordinates(self, x, y):
        if self.tracking:
            self.click_coordinates = (x, y)
            self.set_coordinates_label.config(text=f"Coordinates Locked: ({x}, {y})")
            self.tracking = False

    def start_clicking(self):
        if self.click_coordinates is None:
            messagebox.showwarning("Warning", "Please set click coordinates first.")
            return

        try:
            self.num_iterations = int(self.num_iterations_entry.get())
        except ValueError:
            messagebox.showwarning("Warning", "Invalid input for iterations.")
            return

        self.clicking = True
        self.start_button.config(state=tk.DISABLED)
        self.quit_button.config(state=tk.DISABLED)

        def click_thread():
            number = 1

            for _ in range(self.num_iterations):
                if not self.clicking:
                    break

                pyautogui.click(self.click_coordinates[0], self.click_coordinates[1])
                pyautogui.typewrite(str(number))
                pyautogui.press('enter')
                print(
                    f"Clicked and typed {number} at {self.click_coordinates[0]}, {self.click_coordinates[1]} and clicked Enter.")
                number += 1

            self.clicking = False
            self.start_button.config(state=tk.NORMAL)
            self.quit_button.config(state=tk.NORMAL)

        threading.Thread(target=click_thread).start()

    def quit_app(self):
        self.quit_requested = True
        self.clicking = False
        self.root.quit()
        self.root.destroy()


def on_click(x, y, button, pressed):
    if pressed:
        app.set_coordinates(x, y)


def on_key_release(key):
    if key == keyboard.Key.f2:
        app.quit_app()


if __name__ == "__main__":
    root = tk.Tk()
    app = ClickerApp(root)

    # Start monitoring mouse clicks
    listener_mouse = mouse.Listener(on_click=on_click)
    listener_mouse.start()

    # Start monitoring keyboard events
    listener_keyboard = keyboard.Listener(on_release=on_key_release)
    listener_keyboard.start()

    root.mainloop()
