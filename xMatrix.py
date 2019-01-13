import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from fractions import Fraction
from pprint import pprint
import json
import copy
import Algorithms
import gettext
try:
    import numpy
except:
    numpy = None

gettext.install("lang", "./locale")
#gettext.translation("lang", "./locale", languages=["cn"]).install(True)

MATRIX_SIZE = 6
PAD_SIZE = 10
WIDGET_WIDTH = 20

class Application:
    def __init__(self, master):
        self.master = master
        self.leftMatSize = (2, 2)
        self.rightMatSize = (2, 2)
        self.create_widgets()
        self.deserialize()

    def create_widgets(self):
        # panel for left Matrix
        panel = tk.Frame(self.master, padx=PAD_SIZE, pady=PAD_SIZE)
        panel.grid(row=0, column=0)
        ctrls = tk.Frame(panel)
        ctrls.pack(side="top", anchor="w")
        lab = tk.Label(ctrls, text=_("Matrix A"))
        lab.pack(side="left", padx=PAD_SIZE, pady=PAD_SIZE)
        lab = tk.Label(ctrls, text=_("Row"))
        lab.pack(side="left", padx=PAD_SIZE, pady=PAD_SIZE)
        self.leftRow = ttk.Combobox(ctrls, values=[i+1 for i in range(MATRIX_SIZE)], width=WIDGET_WIDTH//5, state="readonly")
        self.leftRow.pack(side="left", padx=PAD_SIZE, pady=PAD_SIZE)
        self.leftRow.set(self.leftMatSize[0])
        self.leftRow.bind("<<ComboboxSelected>>", self.updateMatrixSize)
        lab = tk.Label(ctrls, text=_("Column"))
        lab.pack(side="left", padx=PAD_SIZE, pady=PAD_SIZE)
        self.leftCol = ttk.Combobox(ctrls, values=[i+1 for i in range(MATRIX_SIZE)], width=WIDGET_WIDTH//5, state="readonly")
        self.leftCol.pack(side="left", padx=PAD_SIZE, pady=PAD_SIZE)
        self.leftCol.set(self.leftMatSize[1])
        self.leftCol.bind("<<ComboboxSelected>>", self.updateMatrixSize)
        btn = tk.Button(ctrls, text=_("Transpose"))
        btn.pack(side="left", padx=PAD_SIZE, pady=PAD_SIZE)
        btn["command"] = self.btn_transpose_left_matrix
        btn = tk.Button(ctrls, text=_("Fill 0"))
        btn.pack(side="left", padx=PAD_SIZE, pady=PAD_SIZE)
        btn["command"] = self.btn_left_fill_zero
        btn = tk.Button(ctrls, text=_("Clear"))
        btn.pack(side="left", padx=PAD_SIZE, pady=PAD_SIZE)
        btn["command"] = self.btn_clear_left_matrix
        btn = tk.Button(ctrls, text=_("Swap A/B"))
        btn.pack(side="left", padx=PAD_SIZE, pady=PAD_SIZE)
        btn["command"] = self.btn_swap_a_b_matrixs
        ctrls = tk.Frame(panel)
        ctrls.pack(side="top")
        self.leftMatrix = []
        for i in range(MATRIX_SIZE):
            for j in range(MATRIX_SIZE):
                entry = tk.Entry(ctrls, width=WIDGET_WIDTH//2, justify="center")
                entry.grid(row=i, column=j, padx=PAD_SIZE, pady=PAD_SIZE)
                self.leftMatrix.append(entry)

        # panel for right Matrix
        panel = tk.Frame(self.master, padx=PAD_SIZE, pady=PAD_SIZE)
        panel.grid(row=0, column=1)
        ctrls = tk.Frame(panel)
        ctrls.pack(side="top", anchor="w")
        lab = tk.Label(ctrls, text=_("Matrix B"))
        lab.pack(side="left", padx=PAD_SIZE, pady=PAD_SIZE)
        lab = tk.Label(ctrls, text=_("Row"))
        lab.pack(side="left", padx=PAD_SIZE, pady=PAD_SIZE)
        self.rightRow = ttk.Combobox(ctrls, values=[i+1 for i in range(MATRIX_SIZE)], width=WIDGET_WIDTH//5, state="readonly")
        self.rightRow.pack(side="left", padx=PAD_SIZE, pady=PAD_SIZE)
        self.rightRow.set(self.rightMatSize[0])
        self.rightRow.bind("<<ComboboxSelected>>", self.updateMatrixSize)
        lab = tk.Label(ctrls, text=_("Column"))
        lab.pack(side="left", padx=PAD_SIZE, pady=PAD_SIZE)
        self.rightCol = ttk.Combobox(ctrls, values=[i+1 for i in range(MATRIX_SIZE)], width=WIDGET_WIDTH//5, state="readonly")
        self.rightCol.pack(side="left", padx=PAD_SIZE, pady=PAD_SIZE)
        self.rightCol.set(self.rightMatSize[1])
        self.rightCol.bind("<<ComboboxSelected>>", self.updateMatrixSize)
        btn = tk.Button(ctrls, text=_("Transpose"))
        btn.pack(side="left", padx=PAD_SIZE, pady=PAD_SIZE)
        btn["command"] = self.btn_transpose_right_matrix
        btn = tk.Button(ctrls, text=_("Fill 0"))
        btn.pack(side="left", padx=PAD_SIZE, pady=PAD_SIZE)
        btn["command"] = self.btn_right_fill_zero
        btn = tk.Button(ctrls, text=_("Clear"))
        btn.pack(side="left", padx=PAD_SIZE, pady=PAD_SIZE)
        btn["command"] = self.btn_clear_right_matrix
        ctrls = tk.Frame(panel)
        ctrls.pack(side="top")
        self.rightMatrix = []
        for i in range(MATRIX_SIZE):
            for j in range(MATRIX_SIZE):
                entry = tk.Entry(ctrls, width=WIDGET_WIDTH//2, justify="center")
                entry.grid(row=i, column=j, padx=PAD_SIZE, pady=PAD_SIZE)
                self.rightMatrix.append(entry)

        # panel for result Matrix
        panel = tk.Frame(self.master, padx=PAD_SIZE, pady=PAD_SIZE)
        panel.grid(row=1, column=1)
        ctrls = tk.Frame(panel)
        ctrls.pack(side="top", anchor="w")
        # Result => matrix A
        btn = tk.Button(ctrls, text=_("Swap Result/A"))
        btn.pack(side="left", padx=PAD_SIZE, pady=PAD_SIZE)
        btn["command"] = self.btn_swap_a_result_matrixs
        btn = tk.Button(ctrls, text=_("Clear"))
        btn.pack(side="left", padx=PAD_SIZE, pady=PAD_SIZE)
        btn["command"] = self.btn_clear_result_matrix
        ctrls = tk.Frame(panel)
        ctrls.pack(side="top")
        self.resultMatrix = []
        for i in range(MATRIX_SIZE):
            for j in range(MATRIX_SIZE):
                entry = tk.Entry(ctrls, width=WIDGET_WIDTH//2, justify="center")
                entry.grid(row=i, column=j, padx=PAD_SIZE, pady=PAD_SIZE)
                self.resultMatrix.append(entry)

        # functionality panel
        panel = tk.Frame(self.master, padx=PAD_SIZE, pady=PAD_SIZE)
        panel.grid(row=1, column=0)
        # determinant
        btn = tk.Button(panel, text=_("A Determinant"), width=WIDGET_WIDTH)
        btn.grid(row=0, column=0, padx=PAD_SIZE, pady=PAD_SIZE)
        btn["command"] = self.btn_calc_determinant
        # determinant's algebra cofactor
        btn = tk.Button(panel, text=_("A Algebra cofactor"), width=WIDGET_WIDTH)
        btn.grid(row=0, column=1, padx=PAD_SIZE, pady=PAD_SIZE)
        btn["command"] = self.btn_calc_algebra_cofactor
        # A*B
        btn = tk.Button(panel, text=_("A*B"), width=WIDGET_WIDTH)
        btn.grid(row=1, column=0, padx=PAD_SIZE, pady=PAD_SIZE)
        btn["command"] = self.btn_matrix_multiply_matrix
        # A^-1
        btn = tk.Button(panel, text=_("A^-1"), width=WIDGET_WIDTH)
        btn.grid(row=1, column=1, padx=PAD_SIZE, pady=PAD_SIZE)
        btn["command"] = self.btn_calc_inverse_matrix
        # simplify ladder
        btn = tk.Button(panel, text=_("A Simplify ladder"), width=WIDGET_WIDTH)
        btn.grid(row=2, column=0, padx=PAD_SIZE, pady=PAD_SIZE)
        btn["command"] = self.btn_simplify_ladder
        # is the matrix orthogonal?
        btn = tk.Button(panel, text=_("is A orthogonal?"), width=WIDGET_WIDTH)
        btn.grid(row=2, column=1, padx=PAD_SIZE, pady=PAD_SIZE)
        btn["command"] = self.btn_is_matrix_a_orthogonal
        # power
        btn = tk.Button(panel, text=_("A Power"), width=WIDGET_WIDTH)
        btn.grid(row=3, column=0, padx=PAD_SIZE, pady=PAD_SIZE)
        btn["command"] = self.btn_calc_power_matrix
        self.powExp = tk.Entry(panel, width=WIDGET_WIDTH//2, justify="center")
        self.powExp.grid(row=3, column=1, padx=PAD_SIZE, pady=PAD_SIZE)
        # calc the orthogonal basis by Gram-Schmidt
        btn = tk.Button(panel, text=_("Gram-Schmidt"), width=WIDGET_WIDTH)
        btn.grid(row=4, column=0, padx=PAD_SIZE, pady=PAD_SIZE)
        btn["command"] = self.btn_calc_gram_schmidt
        # eig
        btn = tk.Button(panel, text=_("Eig"), width=WIDGET_WIDTH)
        btn.grid(row=4, column=1, padx=PAD_SIZE, pady=PAD_SIZE)
        btn["command"] = self.btn_calc_eig
        # clear all
        btn = tk.Button(panel, text=_("Clear all"), width=WIDGET_WIDTH)
        btn.grid(row=5, column=0, padx=PAD_SIZE, pady=PAD_SIZE)
        btn["command"] = self.btn_clear_all

        # update state for all entry controls
        self.updateMatrixSize(None)

    @staticmethod
    def updateEntryState(ctrls, sizes):
        for i in range(MATRIX_SIZE):
            for j in range(MATRIX_SIZE):
                if i>sizes[0]-1 or j>sizes[1]-1:
                    ctrls[i*MATRIX_SIZE+j].config(state="disabled")
                else:
                    ctrls[i*MATRIX_SIZE+j].config(state="normal")

    @staticmethod
    def clearControls(ctrls):
        for ctrl in ctrls:
            disabled = ctrl.config()["state"][-1] ==  "disabled"
            if disabled:
                ctrl.config(state="normal")
            ctrl.delete(0, tk.END)
            if disabled:
                ctrl.config(state="disabled")

    def updateMatrixSize(self, x):
        self.leftMatSize = (int(self.leftRow.get()), int(self.leftCol.get()))
        Application.updateEntryState(self.leftMatrix, self.leftMatSize)
        self.rightMatSize = (int(self.rightRow.get()), int(self.rightCol.get()))
        Application.updateEntryState(self.rightMatrix, self.rightMatSize)

    @staticmethod
    def getDataFromEntries(ctrls, sizes):
        try:
            data = []
            for i in range(sizes[0]):
                row = []
                for j in range(sizes[1]):
                    row.append(Fraction(ctrls[i*MATRIX_SIZE+j].get()))
                data.append(row)
            #pprint(data)
            return data
        except Exception as exp:
            print(exp)
            return None

    def btn_swap_a_b_matrixs(self):
        for i in range(MATRIX_SIZE):
            for j in range(MATRIX_SIZE):
                pos = i*MATRIX_SIZE+j
                self.leftMatrix[pos].config(state="normal")
                self.rightMatrix[pos].config(state="normal")
                a = self.leftMatrix[pos].get()
                b = self.rightMatrix[pos].get()
                self.leftMatrix[pos].delete(0, tk.END)
                self.rightMatrix[pos].delete(0, tk.END)
                self.leftMatrix[pos].insert(0, b)
                self.rightMatrix[pos].insert(0, a)
        self.leftMatSize, self.rightMatSize = self.rightMatSize, self.leftMatSize
        self.leftRow.set(self.leftMatSize[0])
        self.leftCol.set(self.leftMatSize[1])
        self.rightRow.set(self.rightMatSize[0])
        self.rightCol.set(self.rightMatSize[1])
        Application.updateEntryState(self.leftMatrix, self.leftMatSize)
        Application.updateEntryState(self.rightMatrix, self.rightMatSize)

    def btn_swap_a_result_matrixs(self):
        for i in range(MATRIX_SIZE):
            for j in range(MATRIX_SIZE):
                pos = i*MATRIX_SIZE+j
                self.leftMatrix[pos].config(state="normal")
                self.resultMatrix[pos].config(state="normal")
                a = self.leftMatrix[pos].get()
                b = self.resultMatrix[pos].get()
                self.leftMatrix[pos].delete(0, tk.END)
                self.resultMatrix[pos].delete(0, tk.END)
                self.leftMatrix[pos].insert(0, b)
                self.resultMatrix[pos].insert(0, a)
        Application.updateEntryState(self.leftMatrix, self.leftMatSize)

    def btn_clear_all(self):
        Application.clearControls(self.leftMatrix)
        Application.clearControls(self.rightMatrix)
        Application.clearControls(self.resultMatrix)

    def btn_clear_left_matrix(self):
        Application.clearControls(self.leftMatrix)

    def btn_clear_right_matrix(self):
        Application.clearControls(self.rightMatrix)

    def btn_clear_result_matrix(self):
        Application.clearControls(self.resultMatrix)

    def btn_left_fill_zero(self):
        for i in range(self.leftMatSize[0]):
            for j in range(self.leftMatSize[1]):
                if not self.leftMatrix[i*MATRIX_SIZE+j].get():
                    self.leftMatrix[i*MATRIX_SIZE+j].insert(0, 0)
                    
    def btn_right_fill_zero(self):
        for i in range(self.rightMatSize[0]):
            for j in range(self.rightMatSize[1]):
                if not self.rightMatrix[i*MATRIX_SIZE+j].get():
                    self.rightMatrix[i*MATRIX_SIZE+j].insert(0, 0)

    def btn_matrix_multiply_matrix(self):
        if self.leftMatSize[1] != self.rightMatSize[0]:
            messagebox.showerror(title=_("Matrix Assistant"), message=_("the left column and right row are not equal!"))
            return
        Application.clearControls(self.resultMatrix)
        leftMat = Application.getDataFromEntries(self.leftMatrix, self.leftMatSize)
        rightMat = Application.getDataFromEntries(self.rightMatrix, self.rightMatSize)
        if leftMat and rightMat:
            res = Algorithms.multiplyMatrix(leftMat, rightMat)
            for i in range(self.leftMatSize[0]):
                for j in range(self.rightMatSize[1]):
                    self.resultMatrix[i*MATRIX_SIZE+j].insert(0, res[i][j])

    def btn_calc_inverse_matrix(self):
        leftMat = Application.getDataFromEntries(self.leftMatrix, self.leftMatSize)
        if not leftMat or len(leftMat)<2 or len(leftMat)!=len(leftMat[0]):
            messagebox.showerror(title=_("Matrix Assistant"), message=_("the matrix is not square, so that doesn't have inverse matrix."))
            return
        if Algorithms.calcDet(leftMat) == 0:
            messagebox.showerror(title=_("Matrix Assistant"), message=_("det() is 0, the matrix doesn't have inverse matrix."))
            return
        Application.clearControls(self.resultMatrix)
        inv = Algorithms.inverseMatrix(leftMat)
        for i in range(len(inv)):
            for j in range(len(inv)):
                self.resultMatrix[i*MATRIX_SIZE+j].insert(0, inv[i][j])

    def btn_calc_power_matrix(self):
        if self.leftMatSize[0] != self.leftMatSize[1]:
            messagebox.showerror(title=_("Matrix Assistant"), message=_("the matrix must be square!"))
            return
        try:
            n = int(self.powExp.get())
            if n==0 or n==1 or n<-1:
                raise Exception()
        except:
            messagebox.showerror(title=_("Matrix Assistant"), message=_("the power exponent must be one of {-1, 2, 3, and bigger}!"))
            return
        Application.clearControls(self.resultMatrix)
        leftMat = Application.getDataFromEntries(self.leftMatrix, self.leftMatSize)
        if leftMat:
            if n == -1:
                self.btn_calc_inverse_matrix()
                return
            else:
                res = copy.deepcopy(leftMat)
                for i in range(n-1):
                    res = Algorithms.multiplyMatrix(res, leftMat)
                for i in range(self.leftMatSize[0]):
                    for j in range(self.leftMatSize[0]):
                        self.resultMatrix[i*MATRIX_SIZE+j].insert(0, res[i][j])

    def btn_simplify_ladder(self):
        leftMat = Application.getDataFromEntries(self.leftMatrix, self.leftMatSize)
        if not leftMat:
            messagebox.showerror(title=_("Matrix Assistant"), message=_("the matrix is incomplete or invalid, please check it."))
            return
        Application.clearControls(self.resultMatrix)
        res = Algorithms.simplifyLadder(leftMat)
        for i in range(len(res)):
            for j in range(len(res[i])):
                self.resultMatrix[i*MATRIX_SIZE+j].insert(0, res[i][j])

    def btn_transpose_left_matrix(self):
        for i in range(MATRIX_SIZE):
            for j in range(MATRIX_SIZE):
                if j>i:
                    p = i*MATRIX_SIZE+j
                    q = j*MATRIX_SIZE+i
                    self.leftMatrix[p].config(state="normal")
                    self.leftMatrix[q].config(state="normal")
                    a = self.leftMatrix[p].get()
                    b = self.leftMatrix[q].get()
                    self.leftMatrix[p].delete(0, tk.END)
                    self.leftMatrix[q].delete(0, tk.END)
                    self.leftMatrix[p].insert(0, b)
                    self.leftMatrix[q].insert(0, a)
        self.leftMatSize = (self.leftMatSize[1], self.leftMatSize[0])
        self.leftRow.set(self.leftMatSize[0])
        self.leftCol.set(self.leftMatSize[1])
        Application.updateEntryState(self.leftMatrix, self.leftMatSize)

    def btn_transpose_right_matrix(self):
        for i in range(MATRIX_SIZE):
            for j in range(MATRIX_SIZE):
                if j>i:
                    p = i*MATRIX_SIZE+j
                    q = j*MATRIX_SIZE+i
                    self.rightMatrix[p].config(state="normal")
                    self.rightMatrix[q].config(state="normal")
                    a = self.rightMatrix[p].get()
                    b = self.rightMatrix[q].get()
                    self.rightMatrix[p].delete(0, tk.END)
                    self.rightMatrix[q].delete(0, tk.END)
                    self.rightMatrix[p].insert(0, b)
                    self.rightMatrix[q].insert(0, a)
        self.rightMatSize = (self.rightMatSize[1], self.rightMatSize[0])
        self.rightRow.set(self.rightMatSize[0])
        self.rightCol.set(self.rightMatSize[1])
        Application.updateEntryState(self.rightMatrix, self.rightMatSize)

    def btn_calc_determinant(self):
        leftMat = Application.getDataFromEntries(self.leftMatrix, self.leftMatSize)
        if not leftMat or len(leftMat)<2 or len(leftMat)!=len(leftMat[0]):
            messagebox.showerror(title=_("Matrix Assistant"), message=_("the row/column must be equal for the determinant."))
            return
        Application.clearControls(self.resultMatrix)
        self.resultMatrix[0].insert(0, Algorithms.calcDet(leftMat))

    def btn_calc_algebra_cofactor(self):
        leftMat = Application.getDataFromEntries(self.leftMatrix, self.leftMatSize)
        if not leftMat or len(leftMat)<2 or len(leftMat)!=len(leftMat[0]):
            messagebox.showerror(title=_("Matrix Assistant"), message=_("the row/column must be equal for the determinant."))
            return
        Application.clearControls(self.resultMatrix)
        res = Algorithms.calcAlgCofactor(leftMat)
        for i in range(len(res)):
            for j in range(len(res[i])):
                self.resultMatrix[i*MATRIX_SIZE+j].insert(0, res[i][j])

    def btn_is_matrix_a_orthogonal(self):
        pass

    def btn_calc_gram_schmidt(self):
        pass

    def btn_calc_eig(self):
        if not numpy:
            messagebox.showerror(title=_("Matrix Assistant"), message=_("numpy has not been installed, please install it firstly."))
            return
        leftMat = Application.getDataFromEntries(self.leftMatrix, self.leftMatSize)
        if not leftMat or len(leftMat)<2 or len(leftMat)!=len(leftMat[0]):
            messagebox.showerror(title=_("Matrix Assistant"), message=_("Eig is only available to a square matrix."))
            return
        Application.clearControls(self.resultMatrix)
        f = [[float(x) for x in row] for row in leftMat]
        #pprint(f)
        e,v = numpy.linalg.eig(f)
        print(e)
        print(v)
        [self.resultMatrix[i].insert(0, round(e[i], 2)) for i in range(len(e))]
        for i in range(len(v)):
            for j in range(len(v[i])):
                self.resultMatrix[MATRIX_SIZE*(i+1)+j].insert(0, round(v[i][j], 2))
            

    def serialize(self):
        try:
            try:
                data = json.load(open(r"data.json"))
            except:
                data = {}
            content = {}
            content["left_size"] = self.leftMatSize
            content["left_matrix"] = [ctrl.get() for ctrl in self.leftMatrix]
            content["right_size"] = self.leftMatSize
            content["right_matrix"] = [ctrl.get() for ctrl in self.rightMatrix]
            data["matrix"] = content
            json.dump(data, open(r"data.json", "w"), indent=4)
        except Exception as exp:
            pprint(exp)

    def deserialize(self):
        try:
            data = json.load(open(r"data.json"))
            content = data.get("matrix", None)
            if content:
                leftSize = content.get("left_size", None)
                if leftSize and len(leftSize)==2:
                    self.leftRow.set(leftSize[0])
                    self.leftCol.set(leftSize[1])
                leftMat = content.get("left_matrix", None)
                if leftMat and len(leftMat)==MATRIX_SIZE**2:
                    for i in range(len(leftMat)):
                        self.leftMatrix[i].config(state="normal")
                        self.leftMatrix[i].insert(0, leftMat[i])
                rightSize = content.get("right_size", None)
                if rightSize and len(rightSize)==2:
                    self.rightRow.set(rightSize[0])
                    self.rightCol.set(rightSize[1])
                rightMat = content.get("right_matrix", None)
                if rightMat and len(rightMat)==MATRIX_SIZE**2:
                    for i in range(len(rightMat)):
                        self.rightMatrix[i].config(state="normal")
                        self.rightMatrix[i].insert(0, rightMat[i])
                self.updateMatrixSize(None)
        except Exception as exp:
            pprint(exp)

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    root.title(_("Matrix Assistant"))
    root.mainloop()
