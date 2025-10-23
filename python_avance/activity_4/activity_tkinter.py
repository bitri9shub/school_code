from tkinter import *

fenetre=Tk()
fenetre.title=("title")
fenetre.geometry("300x300")

name_labelA=Label(fenetre, text="Enter num 1: ")
name_labelA.grid(column=0, row=0, sticky="w")

v1=StringVar()
v2=StringVar()
v3=StringVar()

entry_value_1=Entry(fenetre, textvariable=v1, width=31)
entry_value_1.focus_set()
entry_value_1.grid(column=1, row=0, sticky="sw", columnspan=1)

name_labelB=Label(fenetre, text="Enter num2: ")
name_labelB.grid(column=0, row=1, sticky="w")

entry_value_2=Entry(fenetre, textvariable=v2, width=31)
entry_value_2.focus_set()
entry_value_2.grid(column=1, row=1, sticky="sw", columnspan=1)

name_labelC=Label(fenetre, text="The sum is: ")
name_labelC.grid(column=0, row=2, sticky="w")

entry_value_3=Entry(fenetre, textvariable=v3, width=31)
entry_value_3.focus_set()
entry_value_3.grid(column=1, row=2, sticky="sw", columnspan=1)

def show_sum():
	v3.set(int(v1.get())+int(v2.get()))

quit_button=Button(fenetre, text="Quit", command=fenetre.quit)
quit_button.grid(column=0, row=3, sticky="sw")

send_button=Button(fenetre, text="Show", command=show_sum)
send_button.grid(column=1, row=3, sticky="sw")

fenetre.mainloop()
