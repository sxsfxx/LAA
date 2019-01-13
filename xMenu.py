import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import gettext

def menu_click_language(lang, master):
    if lang != master.curlang:
        try:
            gettext.translation("lang", "./locale", languages=[lang]).install(True)
        except:
            return
        master.callback_closewindow()
        master.reload(lang)

def menu_click_about():
     messagebox.showerror(title=_("Matrix Assistant"), message=_("This software is free and open source, help to reduce students' hand/brain labor in LinearAlgebra exam.\n\n\t\t\tAuthor: XuYuan @Mooc."))

def menu_click_exit(master):
    master.callback_closewindow()

def makeMenu(master):
    menu = tk.Menu(master)
    fMenu = tk.Menu(menu, tearoff=0)
    langMenu = tk.Menu(fMenu, tearoff=0)
    langMenu.add_command(label="English", command=lambda: menu_click_language("en", master))
    langMenu.add_command(label="中文", command=lambda: menu_click_language("cn", master))
    fMenu.add_cascade(label=_("Language"), menu=langMenu)
    fMenu.add_command(label=_("About"), command=menu_click_about)
    fMenu.add_command(label=_("Exit"), command=lambda: menu_click_exit(master))
    menu.add_cascade(label=_("Menu"), menu=fMenu)
    master.config(menu=menu)
