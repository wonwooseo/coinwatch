from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext


# available currency:
curr_btc = 0  # bitcoin
curr_eth = 0  # ethereum
curr_etc = 0  # ethereum classic
curr_xrp = 0  # ripple
curr_qtum = 0  # qtum
curr_bch = 0  # bitcoin cash
curr_ltc = 0  # litecoin
curr_iota = 0  # iota
curr_eos = 0  # eos
curr_btg = 0  # bitcoin gold
curr_omg = 0  # omisego
curr_data = 0  # streamr
curr_zil = 0  # zilliqa
curr_knc = 0  # kyber network coin
curr_zrx = 0  # 0x
curr_xtz = 0  # tezos


def open_setting():
    setting_window = Toplevel()
    setting_window.title("Currency Monitor Selection")
    setting_window.minsize(480, 270)
    setting_window.maxsize(480, 270)
    # Main window not focusable while in settings
    setting_window.grab_set()
    # Checkboxes for supported currency
    check_frame = ttk.Frame(setting_window)
    chk_btc = ttk.Checkbutton(check_frame, text='Bitcoin', variable=curr_btc)
    chk_btc.pack()
    chk_eth = ttk.Checkbutton(check_frame, text='Ethereum', variable=curr_eth)
    chk_eth.pack()
    chk_etc = ttk.Checkbutton(check_frame, text='Ethereum Classic',
                              variable=curr_etc)
    chk_etc.pack()
    chk_xrp = ttk.Checkbutton(check_frame, text='Ripple', variable=curr_xrp)
    chk_xrp.pack()
    chk_qtum = ttk.Checkbutton(check_frame, text='Qtum', variable=curr_qtum)
    chk_qtum.pack()
    check_frame.pack(side=TOP, fill=BOTH, expand=True)


# GUI exit function
def sys_exit():
    exit_check = messagebox.askyesno("Exit", "Shutdown Coinwatch?")
    if exit_check:
        sys.exit(0)
    else:
        pass


# GUI on main thread
window = Tk()
window.title("Coinwatch")
window.minsize(800, 450)
window.maxsize(800, 450)
# Menu bar settings
menu_bar = Menu(window)
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Monitor..", command=open_setting)
file_menu.add_separator()
file_menu.add_command(label="Exit..", command=sys_exit)
menu_bar.add_cascade(label="File", menu=file_menu)
# Add options here
window.config(menu=menu_bar)
# Notebook (tabs) settings
notebook = ttk.Notebook(window)
notebook.pack(side=TOP, fill=BOTH, expand=True)
# Start text update function
window.mainloop()
