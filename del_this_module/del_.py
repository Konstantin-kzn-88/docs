from tkinter import *


def year():
    print(ent)  # условно во первых надо посмотреть что пришло
    print(ent.get())  # потом у entery надо что-то получить (значение методом get)
    print(type(ent.get()))  # понять какого типа значение мы получили (тут строка)
    # ... понять, что нам дальше делать
    # помня что для математических действий строка не подходит
    ent_num = int(ent.get())
    k = ent_num % 10
    l = (ent_num - 1900) % 12 + 1
    # ...
    x = f'{ent_num}, y. - year under the patronage, {k}, {l},'
    label["text"] = x


window = Tk()
window.title('Hello World!')
window.geometry('700x500')
window.resizable(False, False)
label = Label(window, text='Enter any year (from 1900):\n |\nV', fg='red', font='Times')
label.pack()
ent = Entry(window, width=20, bd=3)
ent.pack()
button = Button(text='input', fg='red', width=10, bd=5, command=year)
button.pack()
window.mainloop()
