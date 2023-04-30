import tkinter
import datetime
import eliza
import tkinter as tk
import customtkinter as ctk #pip install customtkinter

from tkinter import ttk
from pynput import keyboard #pip install pynput

# initialize an Eliza instance
eliza = eliza.Eliza()
# loads doctor.txt for response filtering
eliza.load('doctor.txt')

# initializes a window with title and geometry
root = tk.Tk()
root.title("Eliza the Assitant")
root.geometry('630x830')

# tkinter grid layout
toolbar_frame = tk.Frame(root, width=630, height=200)
toolbar_frame.grid(row=0,column=0, sticky='ne',pady=5)

output_frame = tk.Frame(root, width=630, height=600)
output_frame.grid(row=1,column=0,pady=5,padx=5)
tk.Label(output_frame, text="Eliza",font=('Small Fonts',60)).grid(row=0, column=0)

input_frame = tk.Frame(root, width=630, height=200)
input_frame.grid(row=2, column=0,padx=10,pady=10)

style = ttk.Style()
style.configure('Custom.TEntry', borderwidth=0, relief='flat',
                background='white', foreground='black',
                padding=(10, 5),
                bordercolor='gray',
                focusthickness=2,
                focuscolor='#0078d7',
                borderradius=10)

# Set the initial theme
root.tk.call("source", "azure.tcl")
root.tk.call("set_theme", "dark")


# submit function, includes state of textbox as well as Eliza responses and datetime feature 
def submit():
    # turns the tkinter text widget interactive
    text_box.config(state='normal')
    input_txt=input_box.get()
    if input_txt == '':
        return
    response = eliza.respond(input_txt)
    now = datetime.datetime.now()
    text_box.insert("end-1c",now.strftime('\n'+"%I:%M%p |")+' You: ','YouNameTag')
    text_box.insert("end-1c",input_txt+'\n')
    now = datetime.datetime.now()
    text_box.insert("end-1c",now.strftime('%I:%M%p |')+' Eliza: ', 'ElizaNameTag')
    text_box.insert("end-1c", response)
    text_box.see(tkinter.END)
    # turns the tkinter text widget to 'readonly'
    text_box.config(state='disabled')
    input_box.delete(0,"end")
    
# on_press method where if input key is 'enter' calls submit function
def on_press(key):
    if key == keyboard.Key.enter:
        submit()

listener = keyboard.Listener(
    on_press=on_press)
listener.start()


# close window function
def closeWindow():
    root.quit()

# clear input text function
def clearInputField():
    input_box.delete("0","end")


# change_theme function 
def change_theme():
    # NOTE: The theme's real name is azure-<mode>
    if root.tk.call("ttk::style", "theme", "use") == "azure-dark":
        # Set light theme
        root.tk.call("set_theme", "light")
        text_box.config(bg="#FFFFFF")
    else:
        # Set dark theme
        root.tk.call("set_theme", "dark")
        text_box.config(bg="#A2A2A2")

# creates Submit button
button = ttk.Button(input_frame, text="Submit", command=submit)
button.grid(row = 0, column = 0)

# creates Change theme button
button2 = ttk.Button(toolbar_frame, text="Change theme!", command=change_theme)
button2.grid(row = 0, column= 1)

# creates text box (chat log)
text_box = tk.Text(output_frame, relief='groove', height=30, width = 80, borderwidth=2, pady=5, padx=5, bg='#A2A2A2')
text_box.grid(row = 1, column = 0, sticky='ne')

# text box beginning content parameters
now = datetime.datetime.now()
text_box.insert("end-1c",now.strftime('%I:%M%p |')+' Eliza: ','ElizaNameTag')
text_box.insert("end-1c",eliza.initial())
text_box.tag_config('ElizaNameTag', foreground="black")
text_box.tag_config('YouNameTag', foreground="green")
text_box.config(state= 'disabled')

# create input box
input_box = ttk.Entry(input_frame, width=50,font=(40), style='Custom.TEntry')
input_box.grid(row=0,column=1, pady=10, padx =10)


# tkinter grid configuration
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(1, weight=1)


root.mainloop()