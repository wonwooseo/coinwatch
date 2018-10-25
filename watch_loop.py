import requests
import threading
import queue
from datetime import datetime
import time
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext


api_url = "https://api.coinone.co.kr/ticker/"
# Options
target_currency = 'btc'
cool_down = 5
# Exit when true
exit_flag = False
# Queue for thread communication
q = queue.Queue()


# monitoring loop at new thread
class MonitorLoop(threading.Thread):
    def run(self):
        while not exit_flag:
            res = requests.get(api_url, params={'currency': target_currency})
            price = res.json()['last']
            timestamp = int(res.json()['timestamp'])
            q.put((price, timestamp)) # Bind as tuple and send to queue
            time.sleep(cool_down)  # halt for preset seconds


# Console update function
def console_update():
    if not q.empty():
        data_tup = q.get()
        price = data_tup[0]
        update_time = str(datetime.fromtimestamp(data_tup[1]))
        outline = "[" + update_time + "] " + "Price for " + \
                  target_currency + ": " + str(price) + '\n'
        console_text['state'] = 'normal'
        console_text.insert(END, outline)
        console_text['state'] = 'disabled'
        console_text.see(END)
        window.after(5000, console_update)
    else:
        window.after(1000, console_update)


# GUI exit function
def sys_exit():
    exit_check = messagebox.askyesno("Exit", "Shutdown Coinwatch?")
    if exit_check:
        global exit_flag
        exit_flag = True
        monitor_thread.join()
        sys.exit(0)
    else:
        pass


# Start monitor loop thread
monitor_thread = MonitorLoop()
monitor_thread.start()
# GUI on main thread
window = Tk()
window.title("Coinwatch")
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
console_text = scrolledtext.ScrolledText(console_page, state="disabled", wrap="none", bg="black", fg="lawn green")
console_text.pack(fill=BOTH, expand=True, padx=5, pady=5)
console_page.pack(side=TOP, fill=BOTH, expand=True)
# Start text update function
window.after(0, console_update)
window.mainloop()
