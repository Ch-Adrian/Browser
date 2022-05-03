from os import link
from tkinter import *
import tkinter.font as tkFont
import webbrowser
from search import read_sparse
from tkinter.messagebox import showinfo

frame = Tk()

frame.geometry("800x800")
frame.resizable(False, False)

font = tkFont.Font(family='Courier New Baltic', size=100, weight="bold")
search_string = StringVar(frame)
is_IDF = BooleanVar(frame)
is_Norm = BooleanVar(frame)

search_label = Label(frame, text="Search", font=font)
search_label.place(x=180, y=60)

search_entry = Entry(frame, textvariable=search_string,width=120)
search_entry.place(x=30, y=250)
search_entry.focus()

def linkClickEvent(event):
    webbrowser.open_new(event.widget.cget("text"))

link_list = []
link_labels = []

def run_search():
    showinfo("Searching", "Please wait. Searching process takes a while.")
    for lab in link_labels:
        lab.place_forget()
    
    link_list = read_sparse(search_string.get(), isNorm=is_Norm.get(), isIDF=is_IDF.get())

    tmp_lab = Label(frame, text="Results: ")
    tmp_lab.place(x=30, y=340)
    link_labels.append(tmp_lab)
    for i in range(min(20,len(link_list))):
        link = link_list[i]
        link_tmp = Label(frame, text=link, fg="blue", cursor="hand2")
        link_tmp.place(x=30, y=340+(i+1)*20)
        link_tmp.bind("<Button-1>", lambda e: linkClickEvent(e))
        link_labels.append(link_tmp)

idf_check = Checkbutton(frame,text='use IDF', variable=is_IDF, onvalue=True, offvalue=False)
idf_check.place(x=30, y=300)

norm_check = Checkbutton(frame,text='use Norm', variable=is_Norm, onvalue=True, offvalue=False)
norm_check.place(x=100, y=300)

b1 = Button(frame, text = "Search", command=run_search)
b1.place(x = 350, y = 300)

mainloop()