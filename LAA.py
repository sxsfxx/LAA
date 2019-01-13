# pyinstaller -w -F LAA.py

import tkinter as tk
from tkinter import ttk
import xMatrix
import xGeometry
import xMenu
import gettext

curlang = "cn"
gettext.install("lang", "./locale")
try:
    gettext.translation("lang", "./locale", languages=[curlang]).install(True)
except Exception as exp:
    print(exp)

def close_window(root, mat, geo):
    mat.serialize()
    geo.serialize()
    root.destroy()

def main(curlang="en"):
    root = tk.Tk()
    note = ttk.Notebook(root)

    tabMat = tk.Frame(note)
    mat = xMatrix.Application(master=tabMat)
    note.add(tabMat, text=" "+_("Matrix")+" ")
    
    tabGeo = tk.Frame(note)
    geo = xGeometry.Application(master=tabGeo)
    note.add(tabGeo, text=" "+_("Geometry")+" ")

    note.pack()

    # menu
    xMenu.makeMenu(root)
    root.reload = main
    root.curlang = curlang

    root.title(_("Linear Algebra Assistant"))
    root.callback_closewindow = lambda: close_window(root, mat, geo)
    root.protocol("WM_DELETE_WINDOW", root.callback_closewindow)
    root.mainloop()

main("cn")
