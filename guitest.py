import tkinter

def when_pressed(event=None):
    print(e.get())

# def get(event):
#     print(event.widget.get())

gui = tkinter.Tk()
#gui.geometry("500x500")
t = tkinter.Text(gui)
t.insert('1.0', "HELLO")
l = tkinter.Label(gui, text="Enter the ticker symbol:")
b = tkinter.Button(gui, text="Enter", command=when_pressed, height = 1, width = 10)
e = tkinter.Entry(gui, width = 25)
e.bind('<Return>', when_pressed)
l.pack()
t.pack(side='bottom')
e.pack(side="left")
b.pack(side="left")

gui.mainloop()


