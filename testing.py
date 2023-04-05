import eliza
import tkinter
from tkinter import ttk

import sv_ttk
eliza = eliza.Eliza()
eliza.load('doctor.txt')

print(eliza.initial())

root = tkinter.Tk()
root.title("Eliza the Assitant")
root.geometry('1200x800')


def submit():
    text_box.config(state='normal')
    input_txt=input_box.get()
    if input_txt == '':
        return
    response = eliza.respond(input_txt)
    text_box.insert("end-1c",'You: ','YouNameTag')
    text_box.insert("end-1c",input_txt+'\n')
    text_box.insert("end-1c", 'Eliza: ', 'ElizaNameTag')
    text_box.insert("end-1c", response+'\n')
    text_box.config(state='disabled')
    input_box.delete(0, 'end')

button = ttk.Button(root, text="Click me!", command=submit)
button.grid(row = 0, column = 0)


text_box = tkinter.Text(root, relief='groove', height=50, width = 80, borderwidth=1)
text_box.grid(row = 1, column = 0)
text_box.insert("end-1c",'Eliza: ','ElizaNameTag')
text_box.insert("end-1c",eliza.initial()+'\n')
text_box.tag_config('ElizaNameTag', foreground="cyan")
text_box.tag_config('YouNameTag', foreground="green")
text_box.config(state= 'disabled')

input_box = tkinter.Entry(root, width=200,borderwidth=1,font=(60))
input_box.grid(row=1,column=2)

# This is where the magic happens
sv_ttk.set_theme('dark')


root.mainloop()
'''
while True:
    said = input('> ')
    response = eliza.respond(said)
    if response is None:
        break
    print(response)
print(eliza.final())
'''
