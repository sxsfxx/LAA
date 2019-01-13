import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from fractions import Fraction
from pprint import pprint
from Point import Point
import json
import copy
import Algorithms
import gettext

gettext.install("lang", "./locale")
#gettext.translation("lang", "./locale", languages=["cn"]).install(True)

PAD_SIZE = 10
WIDGET_WIDTH = 20

class Application:
    def __init__(self, master):
        self.master = master
        self.create_widgets()
        self.deserialize()

    def create_widgets(self):
        # left panel, for control
        panel = tk.Frame(self.master, width=WIDGET_WIDTH)
        panel.pack(side="left", padx=PAD_SIZE, pady=PAD_SIZE)
        
        # controls in the left panel
        btn = tk.Button(panel, text=_("Normalize"), width=WIDGET_WIDTH)
        btn.grid(row=0, column=0, padx=PAD_SIZE, pady=PAD_SIZE)
        btn["command"] = self.btn_normalize
        
        btn = tk.Button(panel, text=_("Dot product"), width=WIDGET_WIDTH)
        btn.grid(row=1, column=0, padx=PAD_SIZE, pady=PAD_SIZE)
        btn["command"] = self.btn_dot_product
        
        btn = tk.Button(panel, text=_("Cross product"), width=WIDGET_WIDTH)
        btn.grid(row=2, column=0, padx=PAD_SIZE, pady=PAD_SIZE)
        btn["command"] = self.btn_cross_product
        
        btn = tk.Button(panel, text=_("Mix product"), width=WIDGET_WIDTH)
        btn.grid(row=3, column=0, padx=PAD_SIZE, pady=PAD_SIZE)
        btn["command"] = self.btn_mix_product
        
        btn = tk.Button(panel, text=_("Determinant"), width=WIDGET_WIDTH)
        btn.grid(row=4, column=0, padx=PAD_SIZE, pady=PAD_SIZE)
        btn["command"] = self.btn_determinant
        
        # right panel for input data
        panel = tk.Frame(self.master, width=WIDGET_WIDTH)
        panel.pack(side="left", padx=PAD_SIZE, pady=PAD_SIZE)
        # at the first row, there are 3 labels i,j,k
        lab = tk.Label(panel, text="i", width=WIDGET_WIDTH)
        lab.grid(row=0, column=1, padx=PAD_SIZE, pady=PAD_SIZE)
        lab = tk.Label(panel, text="j", width=WIDGET_WIDTH)
        lab.grid(row=0, column=2, padx=PAD_SIZE, pady=PAD_SIZE)
        lab = tk.Label(panel, text="k", width=WIDGET_WIDTH)
        lab.grid(row=0, column=3, padx=PAD_SIZE, pady=PAD_SIZE)
        # at the first column, there are 3 labels for A,B,C
        lab = tk.Label(panel, text="A", anchor="e", width=WIDGET_WIDTH)
        lab.grid(row=1, column=0, padx=PAD_SIZE, pady=PAD_SIZE)
        lab = tk.Label(panel, text="B", anchor="e", width=WIDGET_WIDTH)
        lab.grid(row=2, column=0, padx=PAD_SIZE, pady=PAD_SIZE)
        lab = tk.Label(panel, text="C", anchor="e", width=WIDGET_WIDTH)
        lab.grid(row=3, column=0, padx=PAD_SIZE, pady=PAD_SIZE)
        # input entry for A,B,C
        self.Ai = tk.Entry(panel, justify="center", width=WIDGET_WIDTH)
        self.Ai.grid(row=1, column=1, padx=PAD_SIZE, pady=PAD_SIZE)
        self.Aj = tk.Entry(panel, justify="center", width=WIDGET_WIDTH)
        self.Aj.grid(row=1, column=2, padx=PAD_SIZE, pady=PAD_SIZE)
        self.Ak = tk.Entry(panel, justify="center", width=WIDGET_WIDTH)
        self.Ak.grid(row=1, column=3, padx=PAD_SIZE, pady=PAD_SIZE)
        self.Bi = tk.Entry(panel, justify="center", width=WIDGET_WIDTH)
        self.Bi.grid(row=2, column=1, padx=PAD_SIZE, pady=PAD_SIZE)
        self.Bj = tk.Entry(panel, justify="center", width=WIDGET_WIDTH)
        self.Bj.grid(row=2, column=2, padx=PAD_SIZE, pady=PAD_SIZE)
        self.Bk = tk.Entry(panel, justify="center", width=WIDGET_WIDTH)
        self.Bk.grid(row=2, column=3, padx=PAD_SIZE, pady=PAD_SIZE)
        self.Ci = tk.Entry(panel, justify="center", width=WIDGET_WIDTH)
        self.Ci.grid(row=3, column=1, padx=PAD_SIZE, pady=PAD_SIZE)
        self.Cj = tk.Entry(panel, justify="center", width=WIDGET_WIDTH)
        self.Cj.grid(row=3, column=2, padx=PAD_SIZE, pady=PAD_SIZE)
        self.Ck = tk.Entry(panel, justify="center", width=WIDGET_WIDTH)
        self.Ck.grid(row=3, column=3, padx=PAD_SIZE, pady=PAD_SIZE)
        # a row for result
        lab = tk.Label(panel, text="Result", anchor="e", width=WIDGET_WIDTH)
        lab.grid(row=4, column=0, padx=PAD_SIZE, pady=PAD_SIZE)
        self.Ri = tk.Label(panel, text="", relief="ridge", width=WIDGET_WIDTH)
        self.Ri.grid(row=4, column=1, padx=PAD_SIZE, pady=PAD_SIZE)
        self.Rj = tk.Label(panel, text="", relief="ridge", width=WIDGET_WIDTH)
        self.Rj.grid(row=4, column=2, padx=PAD_SIZE, pady=PAD_SIZE)
        self.Rk = tk.Label(panel, text="", relief="ridge", width=WIDGET_WIDTH)
        self.Rk.grid(row=4, column=3, padx=PAD_SIZE, pady=PAD_SIZE)

    def btn_normalize(self):
        self.clearResult()
        v = self.getVectorA()
        if v:
            m = v.mod()
            if m[0]:
                self.setVectorResult(v=v.normalize())
            else:
                a = "{0}/sqrt({1})".format(v.x, m[1])
                b = "{0}/sqrt({1})".format(v.y, m[1])
                c = "{0}/sqrt({1})".format(v.z, m[1])
                self.setVectorResult(a=a, b=b, c=c)

    def btn_dot_product(self):
        self.clearResult()
        a = self.getVectorA()
        b = self.getVectorB()
        if a and b:
            x = a * b
            self.setScalarResult(x)

    def btn_cross_product(self):
        self.clearResult()
        a = self.getVectorA()
        b = self.getVectorB()
        if a and b:
            x = a @ b
            self.setVectorResult(v=x)

    def btn_mix_product(self):
        self.clearResult()
        a = self.getVectorA()
        b = self.getVectorB()
        c = self.getVectorC()
        if a and b and c:
            x = a @ b
            y = x * c
            self.setScalarResult(y)

    def btn_determinant(self):
        self.clearResult()
        a = self.getVectorA()
        b = self.getVectorB()
        c = self.getVectorC()
        if a and b and c:
            data = [[a.x, a.y, a.z], [b.x, b.y, b.z], [c.x, c.y, c.z]]
            self.setScalarResult(Algorithms.calcDet(data))

    def getVectorA(self):
        try:
            return Point(self.Ai.get(), self.Aj.get(), self.Ak.get())
        except:
            return None

    def getVectorB(self):
        try:
            return Point(self.Bi.get(), self.Bj.get(), self.Bk.get())
        except:
            return None

    def getVectorC(self):
        try:
            return Point(self.Ci.get(), self.Cj.get(), self.Ck.get())
        except:
            return None

    def clearResult(self):
        self.Ri.config(text="")
        self.Rj.config(text="")
        self.Rk.config(text="")

    def setVectorResult(self, v=None, a=None, b=None, c=None):
        if v:
            self.Ri.config(text=v.x)
            self.Rj.config(text=v.y)
            self.Rk.config(text=v.z)
        else:
            self.Ri.config(text=a)
            self.Rj.config(text=b)
            self.Rk.config(text=b)

    def setScalarResult(self, v):
        self.Ri.config(text=v)

    def serialize(self): 
        try:
            try:
                data = json.load(open(r"data.json"))
            except:
                data = {}
            content = []
            content.append(self.Ai.get())
            content.append(self.Aj.get())
            content.append(self.Ak.get())
            content.append(self.Bi.get())
            content.append(self.Bj.get())
            content.append(self.Bk.get())
            content.append(self.Ci.get())
            content.append(self.Cj.get())
            content.append(self.Ck.get())
            data["geometry"] = content
            json.dump(data, open(r"data.json", "w"), indent=4)
        except Exception as exp:
            pprint(exp)

    def deserialize(self):
        try:
            data = json.load(open(r"data.json"))
            content = data.get("geometry", None)
            if content:
                self.Ai.insert(0, content[0])
                self.Aj.insert(0, content[1])
                self.Ak.insert(0, content[2])
                self.Bi.insert(0, content[3])
                self.Bj.insert(0, content[4])
                self.Bk.insert(0, content[5])
                self.Ci.insert(0, content[6])
                self.Cj.insert(0, content[7])
                self.Ck.insert(0, content[8])
        except Exception as exp:
            pprint(exp)

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    root.title(_("Geometry Assistant"))
    root.mainloop()