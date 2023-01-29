from tkinter import *
from tkinter import ttk
import tkinter as tk
import math
from ctypes import windll

windll.shcore.SetProcessDpiAwareness(1)

LARGE_FONT_STYLE = ("Comic Sans", 36)
SMALL_FONT_STYLE = ("Comic Sans", 16)
TINY_FONT_STYLE = ('Comic Sans', 12)

RIGHT_BG = "#a8dadc"
LEFT_BG = "#001d3d"
CALC_BG = "#e63946"
ACTIVE_BG = "#457b9d"

LEFT_COLOR = "white"
RIGHT_COLOR = "black"

class Calculator:
    
    def __init__(self):
        
        self.window = tk.Tk()
        self.window.geometry("1000x700")
        self.window.resizable(0,0)
        self.window.title("GPA Calculator")
        
        self.ent_frame , self.res_frame = self.create_main_frames()
        
        self.res_exp = 0
        self.top_label, self.res_label = self.create_right_labels()
        
        self.sub_entry, self.subjects = "0", "0"
        self.credit_list = []
        self.grade_list = []
               
        self.grades = {"O":10, "A+":9, "A":8, "B+":7, "B":6, "C":5}
        self.create_left_labels()
              
    def create_main_frames(self):
        ent_frame = tk.Frame(self.window, bg=LEFT_BG, width=300)
        ent_frame.grid(row=0, column=0,sticky=NSEW)
        ent_frame.rowconfigure(0, weight=1)
        ent_frame.rowconfigure(1, weight=1)
        ent_frame.rowconfigure(2, weight=12)
        ent_frame.columnconfigure(0, weight=1)
        ent_frame.columnconfigure(1, weight=1)
        ent_frame.propagate(FALSE)
        
        res_frame = tk.Frame(self.window, bg=RIGHT_BG, width= 200)
        res_frame.grid(row=0, column=1, sticky=NSEW)
        res_frame.propagate(False)
        
        self.window.grid_columnconfigure(0, weight=2)
        self.window.grid_columnconfigure(1, weight=1)
        self.window.rowconfigure(0, weight=1)
        
        return ent_frame,res_frame
    
    def create_right_labels(self):
        top_label = tk.Label(self.res_frame,
                             text="Your calculated GPA is:",
                             bg=RIGHT_BG,
                             anchor=S,
                             fg=RIGHT_COLOR,
                             font=SMALL_FONT_STYLE)
        top_label.pack(expand=True, fill="both")
        res_label = tk.Label(self.res_frame,
                             text=self.res_exp,
                             anchor=N,
                             bg=RIGHT_BG,
                             fg=RIGHT_COLOR,
                             font=LARGE_FONT_STYLE)
        res_label.pack(expand=True, fill="both")
        
        button = tk.Button(self.res_frame,
                           font=LARGE_FONT_STYLE,
                           text="Calculate",
                           bg=CALC_BG,
                           command= self.evaluate,
                           height=1,
                           borderwidth=0,
                           activebackground=ACTIVE_BG)
        button.pack(expand=True, fill="both")
        
        warning = tk.Label(self.res_frame,
                             text="WARNING: The data will reset \nafter pressing calculate!",
                             bg=CALC_BG,
                             anchor=S,
                             font=TINY_FONT_STYLE)
        warning.pack(fill="both")
        
        return top_label, res_label    
    
    def create_left_labels(self):
        txt_label = tk.Label(self.ent_frame,
                             text="Enter the number of credit subjects (max 15) \n(Press Return after typing):",
                             bg=LEFT_BG,
                             fg=LEFT_COLOR,
                             font=TINY_FONT_STYLE)
        txt_label.grid(row=0, column=0)
        
        self.sub_entry = tk.Entry(self.ent_frame,
                                  font=TINY_FONT_STYLE,
                                  width=5)
        self.sub_entry.grid(row=0, column=1)
        self.sub_entry.bind('<Return>', self.enter_press)
        
        txt_label = tk.Label(self.ent_frame,
                             text="Enter the credits and grade for each subject:",
                             bg=LEFT_BG,
                             fg=LEFT_COLOR,
                             font=TINY_FONT_STYLE)
        txt_label.grid(row=1, columnspan=4)
    
    def create_grade_frame(self):
        self.grade_frame = tk.Frame(self.ent_frame, bg=LEFT_BG)
        self.grade_frame.grid(row=2, columnspan=3, sticky=NSEW)
        self.create_grade_labels()

    def create_grade_labels(self):
        try:
            for i in range(0,4):
                self.grade_frame.columnconfigure(i, weight=1)
            for i in range(0,int(str(self.subjects))):
                self.grade_frame.rowconfigure(i, weight=1)
        except Exception as e:
            pass
        
        for i in range(0, int(self.subjects)):
            txt_label = tk.Label(self.grade_frame, text="Subject "+str(i+1)+": ", bg=LEFT_BG, fg=LEFT_COLOR, font=TINY_FONT_STYLE)
            txt_label.grid(row=i, column=0)
            
            entry_box = tk.Entry(self.grade_frame, font=TINY_FONT_STYLE, width=5)
            entry_box.grid(row=i, column=2)
            self.credit_list.append(entry_box)
            
            combo_box = ttk.Combobox(self.grade_frame, font=TINY_FONT_STYLE, width=3)
            combo_box.grid(row=i, column=3)
            combo_box["values"] = ("O", "A+", "A", "B+", "B", "C")
            combo_box.set("O")
            self.grade_list.append(combo_box)
    
    def enter_press(self, event=None):
        self.subjects = math.floor(float(self.sub_entry.get()))
        self.res_label.config(text=self.res_exp)
        if self.subjects <= 15:
            self.credit_list = []
            self.grade_list = []
            self.create_grade_frame()
      
    def evaluate(self):
        self.res_exp=0
        k=0
        temp = 0
        try:
            for grade in self.grade_list:
                val = self.credit_list[k].get()
                self.res_exp += self.grades.get(grade.get()) * math.floor(float(val))
                temp += math.floor(float(val))
                k+=1
            if temp == 0:
                self.res_exp = 0
            else:
                self.res_exp = int(self.res_exp) / int(temp)
        except Exception as e:
            self.res_exp=0
        finally:
            self.res_label.config(text=str(self.res_exp)[0:5])
        self.res_exp = 0
        self.credit_list = []
        self.grade_list = []
        self.create_grade_labels()
        
    def run(self):
        self.window.mainloop()
    
    
if __name__ == "__main__":
    calc = Calculator()
    calc.run()