import requests
import threading
import queue
import configparser
from datetime import datetime
import time
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext


api_url = "https://api.coinone.co.kr/ticker/"
# Options from config
config = configparser.ConfigParser()
config.read("monitor_config.ini")
targets = config['TARGET']['currency'].split('\n')[1:]
cool_down = int(config['SETTINGS']['cooldown'])


class MonitorLoop(threading.Thread):
    """
    Thread for price monitor. Loops until flag turns and signals exit.
    Interval between each loop can be adjusted from config file.
    Fetches latest data of given currency via Coinone API and passes price
    value to GUI Thread via queue.
    """
    def __init__(self, tid, target, q):
        """
        Overriden function to add arguments on thread initialization.
        :param tid: (int) Thread ID
        :param target: (string) Currency ticker
        :param q: (queue.Queue) Queue object for thread communication
        """
        threading.Thread.__init__(self)
        self.id = tid
        self.currency = target
        self.q = q

    def run(self):
        """
        Execution part of thread. Fetches latest data and pass it to GUI.
        :return: no return value
        """
        while not flag_arr[self.id]:
            res = requests.get(api_url, params={'currency': self.currency})
            price = res.json()['last']
            timestamp = int(res.json()['timestamp'])
            self.q.put((price, timestamp))  # Bind as tuple and send to queue
            time.sleep(cool_down)  # halt for preset seconds


class GUILoop(threading.Thread):
    """
    Thread for GUI. Picks up data sent from monitor thread through queue and
    updates the textbox. tkinter main loop runs on this thread.
    """
    def __init__(self, tid, target, q):
        """
        Overriden function to add arguments on thread initialization.
        :param tid: (int) Thread ID
        :param target: (string) Currency ticker
        :param q: (queue.Queue) Queue object for thread communication
        """
        threading.Thread.__init__(self)
        self.id = tid
        self.currency = target
        self.q = q

    def run(self):
        """
        Execution part of this thread. Sets up GUI and starts GUI main loop.
        :return: no return value
        """
        def console_update():
            """
            Fetches latest price data from the queue and updates the textbox
            of GUI. This function should be explicitly called using after
            method of tkinter window.
            :return: no return value
            """
            if not self.q.empty():
                data_tup = self.q.get()
                price = data_tup[0]
                update_time = str(datetime.fromtimestamp(data_tup[1]))
                outline = "[" + update_time + "] " + "Price for " + \
                          self.currency + ": " + str(price) + '\n'
                console_text['state'] = 'normal'
                console_text.insert(END, outline)
                console_text['state'] = 'disabled'
                console_text.see(END)
                window.after(5000, console_update)  # reserve next call
            else:  # if queue was empty, wait for short time and check again
                window.after(1000, console_update)

        def sys_exit():
            """
            Callback function initiated when window closes or user exits from
            menu. Joins monitor thread and exits current thread.
            :return: no return value
            """
            exit_check = messagebox.askyesno("Exit", "Shutdown this monitor?")
            if exit_check:
                flag_arr[self.id] = True
                # TODO: find other options for joining (delay before joining)
                monitor_thread.join()  # to exit gracefully
                sys.exit(0)  # quit current thread
            else:
                pass

        # Start monitor loop thread
        monitor_thread = MonitorLoop(self.id, self.currency, self.q)
        monitor_thread.start()
        # GUI on current thread
        window = Tk()
        window.title("Coinwatch: " + self.currency)
        window.minsize(800, 450)
        window.maxsize(800, 450)
        # Menu bar settings
        menu_bar = Menu(window)
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Exit..", command=sys_exit)
        menu_bar.add_cascade(label="File", menu=file_menu)
        # Add options here
        window.config(menu=menu_bar)
        # Console tab
        console_page = ttk.Frame(window)
        console_text = scrolledtext.ScrolledText(console_page,
                                                 state="disabled", wrap="none",
                                                 bg="black", fg="lawn green")
        console_text.pack(fill=BOTH, expand=True, padx=5, pady=5)
        console_page.pack(side=TOP, fill=BOTH, expand=True)
        # Start text update function
        window.after(0, console_update)
        # Show message box when closing window
        window.protocol("WM_DELETE_WINDOW", sys_exit)
        window.mainloop()


flag_arr = []  # global list to store flags
for i in range(0, len(targets)):
    new_flag = False
    flag_arr.append(new_flag)
    new_q = queue.Queue()
    new_thread = GUILoop(i, targets[i], new_q)
    new_thread.start()
    time.sleep(0.5)  # error prevention
