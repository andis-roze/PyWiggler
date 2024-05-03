import threading
import time
import tkinter
import tkinter.messagebox
import tkinter.ttk
from pynput.mouse import Controller as MouseController


class Wiggler:
    def __init__(self, delta=1, interval=1):
        self.mouse = MouseController()
        self.running = False
        self.stop_event= threading.Event()
        self.toggle_text = ["Start", "Stop"]

        self.root = tkinter.Tk()
        self.root.title("Wiggler")
        self.delta = delta
        self.interval = interval
        
        mainframe = tkinter.ttk.Frame(self.root, padding="0 0 0 0")
        mainframe.grid(column=0, row=0)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.button = tkinter.ttk.Button(mainframe, text=self.toggle_text[int(self.running)], command=self.toggle)
        self.button.grid(column=0, row=0)

        for child in mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

        self.root.bind("<Return>", self.toggle)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def wiggle(self):
        while not self.stop_event.is_set():
            self.mouse.move(self.delta, self.delta)
            time.sleep(self.interval)
            self.delta *= -1

    def start(self):
        self.stop_event.clear()
        self.thread = threading.Thread(target=self.wiggle)
        self.thread.start()

    def stop(self):
        self.stop_event.set()
        self.thread.join()

    def toggle(self):
        self.running = not self.running
        self.button.config(text=self.toggle_text[int(self.running)])

        if self.running:
            self.start()
        else:
            self.stop()

    def on_closing(self):
        if tkinter.messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.stop_event.set()
            self.root.destroy()

    def mainloop(self):
        self.root.mainloop()


if __name__ == "__main__":
    wiggler = Wiggler()
    wiggler.mainloop()
