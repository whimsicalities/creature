from tkinter import Tk, Canvas, PhotoImage, Frame, Button, Label, Entry
import os

def pet(event):
    global modifier
    canvas.itemconfig(creature, image=creature_squish)
    modifier=3

def unpet(event):
    global modifier
    canvas.itemconfig(creature, image=creature_idle)
    modifier=1

def move_window(event):
    window.geometry(
        '%dx%d+%d+%d' % (window_width,window_height,event.x_root-50,event.y_root-10))

def create_window():  # create window and define size + position
    window = Tk()
    ws = window.winfo_screenwidth()  # computers screen size
    hs = window.winfo_screenheight()
    x = (ws / 2) - (window_width / 2)  # calculate centre
    y = (hs / 2) - (window_height / 2)
    window.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))
    window.resizable(False, False)
    return window

def count():
    global heart_count
    canvas.pack()
    heart_count=heart_count+1
    canvas.itemconfig(count_lbl,text=(str(heart_count)))
    window.after(int(1000/modifier),count)

def close():
    global name
    file = open('save', 'wb')
    file.write(heart_count.to_bytes(10, 'big'))
    file.close()
    file=open('pet_name.txt','w')
    file.write(name)
    file.close()
    window.destroy()

def close_popup():
    global popup, entry_box, name
    name=entry_box.get()
    popup.destroy()

def namepopup():
    global popup, entry_box
    popup = Tk()
    popup.configure(bg='#EECCAA')
    label = Label(popup, text='Name your creature!', bg='#EECCAA', fg='#ff8c78', font='System 10 bold')
    label.pack(side='top', fill='x', pady=10)
    entry_box=Entry(popup, width=15,relief='flat')
    entry_box.pack(side='top', pady=10)
    enter_btn = Button(popup, text="GO", relief='flat', bg='white', fg='#ff8c78', command = close_popup)
    enter_btn.pack(side='top', pady=10)
    ws = popup.winfo_screenwidth()  # computers screen size
    hs = popup.winfo_screenheight()
    x = (ws / 2) - (200 / 2)  # calculate centre
    y = (hs / 2) - (130 / 2)
    popup.geometry('%dx%d+%d+%d' % (200, 130, x, y))
    popup.overrideredirect(True)
    popup.mainloop()

name=''
if os.path.exists('pet_name.txt'):
    file = open('pet_name.txt','r')
    name=file.read()
    file.close()
else:
    namepopup()

window_width = 150
window_height = 180
window = create_window()
# window.title(name)
canvas = Canvas(window, highlightthickness=0, width=window_width, height=window_height, background='#EECCAA')
# replace title bar
window.overrideredirect(True)
title_bar = Frame(window, bg='#EECCAA', relief='flat')
name_lbl=Label(title_bar, text=name, font='System 10 bold', background='#EECCAA', fg='#ff8c78')
close_btn = Button(title_bar, text='x', relief='flat', command=close, background='#EECCAA', foreground='white')
title_bar.pack(expand=True, fill='x')
close_btn.pack(side='right')
name_lbl.pack(side='left', fill='x', padx=10)
canvas.pack()
title_bar.bind('<B1-Motion>', move_window)

creature_height=100
creature_width=130
creature_idle=PhotoImage(file='creature_idle.png')
creature_squish=PhotoImage(file='creature_squish.png')
creature = canvas.create_image(window_width/2,10,anchor='n',image=creature_idle)
canvas.tag_bind(creature,'<Enter>',pet)
canvas.tag_bind(creature,'<Leave>',unpet)
heart_img = PhotoImage(file='heart.png')
heart=canvas.create_image(10,140,anchor='sw',image=heart_img)
count_lbl=canvas.create_text(40, 140,anchor='sw',text="0",font='System 10 bold',fill='#ff8c78')
heart_count=0
modifier=1


if os.path.exists('save'):
    file = open('save', 'rb')
    heart_count = int.from_bytes(file.read(), 'big')
    file.close()
    canvas.itemconfig(count_lbl, text=(str(heart_count)))



canvas.pack()

canvas.focus_set()

count()

window.mainloop()