from tkinter import *
from tkinter import messagebox
import socket
import os
import bcrypt
import json
import requests
import request

# initiate for window GUI
window = Tk()
window.title('Account Login')
window.geometry('300x300')


def connect_menu():
    window.title('Connect Menu')
    window.geometry('300x300')

    global top_screen
    top_screen = Frame(window)
    top_screen.pack()
    Label(top_screen, text="").pack()
    Button(top_screen, text = "Connect", width = 30, height = 2, command = connect_btn).pack()
    Label(top_screen, text = "").pack()

def connect_btn():
    try:
        res = requests.get('http://127.0.0.1:5000/')

        if res.status_code == 200 :
            # Get notification that client connected to the server
            Label(top_screen, text = "Welcome", font=("Calibri", 13)).pack()
            Label(top_screen, text="").pack()
            messagebox.showinfo('connect', 'connected to server')
            back_frame(top_screen, login)
    except:
        back_connectmenu(top_screen)

        # def back_frame(frame1, to_frameFunc2):
        #     # in this back func, frame will bi hide and new frame will be po up
        #     frame1.pack_forget()
        #     to_frameFunc2()

def back_connectmenu(frame1):
    messagebox.showerror("Connection Error", "Can't Connect to the server")

    # frame will be hide, and connect menu will show-up
    frame1.pack_forget()
    connect_menu()


def back_frame(frame1, to_frameFunc2):
    # in this back func, frame will bi hide and new frame will be po up
    frame1.pack_forget()
    to_frameFunc2()


# define login function
def login():
    window.title("Login menu")
    window.geometry('300x300')
    # top_frame.pack_forget()
    global login_screen
    login_screen = Frame()
    login_screen.pack()
    Label(login_screen, text="Please enter details below to login").pack()
    Label(login_screen, text="").pack()

    global username_verify
    global password_verify
    global username_login_entry
    global password_login_entry

    username_verify = StringVar()
    password_verify = StringVar()

    Label(login_screen, text="IDCard * ").pack()
    username_login_entry = Entry(login_screen, textvariable=username_verify)
    username_login_entry.pack()
    Label(login_screen, text="").pack()

    Label(login_screen, text="PIN * ").pack()
    password_login_entry = Entry(login_screen, textvariable=password_verify, show='*')
    password_login_entry.pack()
    Label(login_screen, text="").pack()

    Button(login_screen, text="Login", width=10, height=1, bg="blue", command=login_verify).pack()
    Label(login_screen, text="").pack()

    Button(login_screen, text="Back", width=5, height=1, bg="green",
           command=lambda: back_frame(login_screen,connect_menu)).pack()

def login_verify():
	try :
		global nama_nasabah
		global no_rek

		no_rek = None

		#get username and password
		username1 = username_verify.get()
		password1 = password_verify.get()

		# this will delete the entry after login button is pressed
		username_login_entry.delete(0, END)
		password_login_entry.delete(0, END)

		# make a hashed data for pass
		salt = b'$2b$12$O4GGyQXRald97MZwuhurL.'
		hashed = bcrypt.hashpw(password1.encode(), salt)
		# make a python object
		kirim_p = {
			"user_id" : int(username1),
			"pass" : hashed.decode()
		}

		# Send JSON
		res = requests.post('http://127.0.0.1:5000/login', json=kirim_p)
		json = res.json()

		if res.status_code == 200 and json.get('status'):
			nama_nasabah = json.get('nama_nasabah')
			no_rek = int(username1)
			messagebox.showinfo("Login Success", "Selamat Datang Sdr. "+nama_nasabah)
			main_menu()
		else:
			messagebox.showerror("Login Failed", "Wrong Username/Password")
	except:
		back_connectmenu(login_screen)
	
    
def main_menu() :
    # Hide frame before (login)
    login_screen.pack_forget()

    # set window geometry and title for user menu
    window.title("Main Menu")
    window.geometry('600x400')

    # make a new frame that contain menu for user
    global menu_1
    menu_1 = Frame(window)
    menu_1.pack()


    # widget menu_1
    Label(menu_1, text = "").pack()
    Button(menu_1, text="User Information", heigh="2", width="30", command = user_info).pack()
    Label(menu_1, text="").pack()

    Button(menu_1, text="Transfer Money", heigh="2", width="30", command = transfer_money).pack()
    Label(menu_1, text="").pack()

    Button(menu_1, text= "Transaction History", heigh="2", width="30", command = transaction_history).pack()
    Label(menu_1, text="").pack()

    Button(menu_1, text = "Exit", heigh = "2", width = "30",
           command = lambda: back_frame(menu_1,login)).pack()
    Label(menu_1, text = "").pack()

def user_info():
    try:
        # hide menu1 frame and show the user info frame.
        menu_1.pack_forget()

        # make a frame for user information
        global user_info_screen
        user_info_screen = Frame(window)
        user_info_screen.pack()

        # Get Saldo data
        # Send JSON
        kirim_p = {
            "no_rek": no_rek
        }
        res = requests.get('http://127.0.0.1:5000/cek_saldo', json=kirim_p)
        #print(res)
        json = res.json()
        #print(json)
        saldo = json.get('saldo')

        # for label in the top frame
        Label(user_info_screen, text = "User Information", font = ("Calibri", 20, "bold")).\
            grid(column = 0, row = 0, columnspan = 2, rowspan = 2)
        Label(user_info_screen, text = "").grid(column = 0, row = 1)

        # name
        Label(user_info_screen, text="Nama: ").grid(column = 0, row = 2)
        name = nama_nasabah
        Label(user_info_screen, text = name, borderwidth = 2, relief = "sunken").grid(column = 1, row = 2)
        Label(user_info_screen, text = "").grid(column = 0, row = 3)

        # account number
        Label(user_info_screen, text="Nomor Rekening: ").grid(column = 0, row = 4)
        rekening = no_rek
        Label(user_info_screen, text = rekening, borderwidth = 2, relief = "sunken").grid(column = 1, row = 4)
        Label(user_info_screen, text = "").grid(column = 0, row = 5)

        #label for user money information
        Label(user_info_screen, text= "Informasi Saldo: ").grid(column = 0, row = 6)
        info_saldo = saldo
        Label(user_info_screen, text= info_saldo, borderwidth = 2, relief = "sunken").grid(column = 1, row = 6)
        Label(user_info_screen,text = "").grid(column = 0, row = 7)

        # Back Button
        Button(user_info_screen, text = "Kembali", width = 30, height = 2,
               command = lambda: back_frame(user_info_screen, main_menu)).grid(column = 0, row = 8, columnspan = 2)
    except:
        # back to connect menu
        back_connectmenu(user_info_screen)

def transfer_money():
    try:
        # hide menu1 frame and show the user info frame.
        menu_1.pack_forget()

        # make a frame for transfer money
        global transfer_money_screen
        transfer_money_screen = Frame(window)
        transfer_money_screen.pack()

        # set to gobal variable
        global user_id
        global money_transfer
        global user_entry
        global money_entry

        # make a title label for this frame
        Label(transfer_money_screen, text = "Transfer Menu", font = ("Calibri", 20, "bold")).\
            grid(column = 0, row = 0, columnspan = 2, rowspan = 2)
        Label(transfer_money_screen, text = "").grid(column = 0, row = 1)

        # User Id
        user_id = StringVar()
        Label(transfer_money_screen, text = "User Id/ No. Rekening: ").grid(column = 0, row = 2)
        user_entry = Entry(transfer_money_screen, textvariable = user_id).grid(column = 1, row = 2)
        Label(transfer_money_screen, text = "").grid(column = 0, row = 3)

        #money that transfer
        money_transfer = IntVar()
        Label(transfer_money_screen, text = "Jumlah uang yang ditransfer: ").grid(column = 0, row = 4)
        money_entry = Entry(transfer_money_screen, textvariable = money_transfer).grid(column = 1, row = 4)
        Label(transfer_money_screen, text = "").grid(column = 0, row = 5)

        #Ok button
        Button(transfer_money_screen, text = "Enter", height = "2", width = "30",
               command = transfer_verify).grid(column = 0, row = 6, columnspan = 2)
        Label(transfer_money_screen, text = "").grid(column = 0, row = 7)

        # Back button
        Button(transfer_money_screen, text="Kembali", width=30, height=2,
               command=lambda: back_frame(transfer_money_screen, main_menu)).grid(column = 0, row = 8, columnspan = 2)
    except:
        back_connectmenu(transfer_money_screen)

def transfer_verify():
    #try:
        # get a value from transfer variable
        send_user = user_id.get()
        send_money = money_transfer.get()

        if send_user == "" or send_money == 0:
            # check  for entry. if not input at entry send an error
            messagebox.showerror("Error tramsfer money", "Please insert a money and user Id")
            user_entry.delete(0, END)
            money_entry.delete(0, END)
        else:
            # hide a frame before
            transfer_money_screen.pack_forget()

            # initiate for a new frame
            global transfer_verify_screen
            transfer_verify_screen = Frame(window)
            transfer_verify_screen.pack()

            #make a title Label
            Label(transfer_verify_screen, text = "Transfer Menu", font = ("Calibri", 18, "bold")).\
                grid(column = 0, row = 0, columnspan =2, rowspan = 2)
            Label(transfer_verify_screen,text = "").grid(column = 0, row = 1)

            # Memastikan informasi yang dikirim
            # User Id
            Label(transfer_verify_screen, text = "User Id: ").grid(column = 0, row = 2)
            Label(transfer_verify_screen, text = send_user, borderwidth = 2, relief = "sunken").grid(column = 1, row = 2)
            Label(transfer_verify_screen, text = "").grid(column = 0, row = 3)

            # Ambil Variabel User
            no_rek_tujuan = send_user

            # Money transfer
            Label(transfer_verify_screen, text="Money Transfer: ").grid(column = 0, row = 4)
            Label(transfer_verify_screen, text=send_money, borderwidth=2, relief = "sunken").grid(column = 1, row = 4)
            Label(transfer_verify_screen, text="").grid(column = 0, row = 5)

            # Ambil Variabel Nominal
            nominal_trans = send_money

            # Send Button
            Button(transfer_verify_screen, text = "Kirim", bg = "green", height = 2, width = 30,
                   command = lambda : execute_transfer(no_rek_tujuan, nominal_trans)).grid(column = 0, row = 6, columnspan = 2)
            Label(transfer_verify_screen, text = "").grid(column = 0, row = 7)

            # Cancel Button
            Button(transfer_verify_screen, text = "Kembali", bg = "yellow", height = 2, width =30,
                   command = lambda : back_frame(transfer_verify_screen,transfer_money)).\
                grid(column = 0, row = 8, columnspan = 2)

    #except:
        #back_connectmenu(transfer_verify_screen)

def execute_transfer(no_rek_tujuan, nominal_trans):
    # Send JSON
    kirim_p = {
        "no_rek": no_rek,
        "no_rek_tujuan": int(no_rek_tujuan),
        "nominal_trans": int(nominal_trans)
    }
    res = requests.post('http://127.0.0.1:5000/exec_transfer', json=kirim_p)
    json = res.json()
    status = json.get('status')
    message = json.get('message')

    if status == 1:
        messagebox.showinfo("Transfer Success", message)
        back_frame(transfer_verify_screen,login)

    else:
        messagebox.showerror("Transfer Failed", message)
        back_frame(transfer_verify_screen, transfer_money)

def transaction_history():
    #try:
        #hide menu_1 frame
        menu_1.pack_forget()

        # iniatiate for a new frame for transaction history
        global transaction_history_screen
        transaction_history_screen = Frame(window)
        transaction_history_screen.pack()

        # Send JSON
        kirim_p = {
            "no_rek": no_rek,
        }
        res = requests.get('http://127.0.0.1:5000/history', json=kirim_p)
        json = res.json()
        status = json.get('status')
        history = json.get('history')

        if status == 1:
            # labe for title in this frame
            Label(transaction_history_screen, text="Transaction History", font=("calibri", 20, "bold")).pack()
            Label(transaction_history_screen, text="").pack()

            # make a table for transaction history
            history_table = Frame(transaction_history_screen)
            history_table.pack()
            list_isi = []
            row_table = len(history)
            column_table = 4

            # coba isi list
            for i in range(row_table):
                for j in range(column_table):
                    list_isi.append([row_table, column_table])
            Label(history_table, text="tanggal", borderwidth=2, relief="sunken").grid(column=0, row=2)
            Label(history_table, text="K/D", borderwidth=2, relief="sunken").grid(column=1, row=2)
            Label(history_table, text="Nominal (Rp)", borderwidth=2, relief="sunken").grid(column=2, row=2)
            Label(history_table, text="rek. asal/tujuan", borderwidth=2, relief="sunken").grid(column=3, row=2)
            for i in range(column_table):
                if i == 0:
                    for j in range(row_table):
                        isi = history[j].get('timestamp')
                        Label(history_table, text=isi, borderwidth=2, relief="sunken").grid(column=i, row=j + 3)

                elif i == 1:
                    for j in range(row_table):
                        nama = history[j].get('nama')
                        if nama == 'ISI SALDO' or nama == 'TRANSFER MASUK':
                            isi = 'D'
                        elif nama == 'TRANSFER KELUAR':
                            isi = 'K'
                        else:
                            isi = 'N/A'
                        Label(history_table, text=isi, borderwidth=2, relief="sunken").grid(column=i, row=j + 3)

                elif i == 2:
                    for j in range(row_table):
                        isi = history[j].get('jumlah_transaksi')
                        Label(history_table, text=isi, borderwidth=2, relief="sunken").grid(column=i, row=j + 3)

                elif i == 3:
                    for j in range(row_table):
                        isi = history[j].get('rek_asal_atau_tujuan')
                        if isi == None:
                            isi = '-'
                        Label(history_table, text=isi, borderwidth=2, relief="sunken").grid(column=i, row=j + 3)
                else:
                    for j in range(row_table):
                        isi = 'Kosong'
                        Label(history_table, text=isi, borderwidth=2, relief="sunken").grid(column=i, row=j + 3)


            # back button
            Label(transaction_history_screen, text="").pack()
            Button(transaction_history_screen, text="Kembali", height=2, width=30, bg="green",
            command=lambda: back_frame(transaction_history_screen, main_menu)).pack()

        else:
            back_connectmenu(transaction_history_screen)
    #except:
        #back_connectmenu(transaction_history_screen)

def back_2frame(frame1, frame2, to_frame3):
    frame2.pack_forget()
    frame1.pack_forget()
    to_frame3()

connect_menu()
window.mainloop()  # start the GUI































