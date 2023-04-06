import eliza
import tkinter as tk
from tkinter import ttk
from pynput import keyboard

eliza = eliza.Eliza()
eliza.load('doctor.txt')



root = tk.Tk()
root.title("Eliza the Assitant")
root.geometry('630x830')

toolbar_frame = tk.Frame(root, width=630, height=200)
toolbar_frame.grid(row=0,column=0, sticky='ne')

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

def change_theme():
    # NOTE: The theme's real name is azure-<mode>
    if root.tk.call("ttk::style", "theme", "use") == "azure-dark":
        # Set light theme
        root.tk.call("set_theme", "light")
    else:
        # Set dark theme
        root.tk.call("set_theme", "dark")

def on_press(key):
    if key == keyboard.Key.enter:
        submit()

listener = keyboard.Listener(
    on_press=on_press)
listener.start()

button = ttk.Button(input_frame, text="Submit", command=submit)
button.grid(row = 0, column = 0)

button2 = ttk.Button(toolbar_frame, text="Change theme!", command=change_theme)
button2.grid(row = 0, column= 1)


text_box = tk.Text(output_frame, relief='groove', height=30, width = 80, borderwidth=2, pady=5, padx=5)
text_box.grid(row = 1, column = 0, sticky='ne')
text_box.insert("end-1c",'Eliza: ','ElizaNameTag')
text_box.insert("end-1c",eliza.initial()+'\n')
text_box.tag_config('ElizaNameTag', foreground="cyan")
text_box.tag_config('YouNameTag', foreground="green")
text_box.config(state= 'disabled')

input_box = ttk.Entry(input_frame, width=50,font=(40), style='Custom.TEntry')
input_box.grid(row=0,column=1, pady=10, padx =10)

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(1, weight=1)


root.mainloop()