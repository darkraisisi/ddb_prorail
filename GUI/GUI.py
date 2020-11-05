import sys
from Model import Model

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

import GUIsupport

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()
    GUIsupport.set_Tk_var()
    top = Toplevel1 (root)
    GUIsupport.init(root, top)
    root.mainloop()


w = None
def create_Toplevel1(rt, *args, **kwargs):
    '''Starting point when module is imported by another module.
       Correct form of call: 'create_Toplevel1(root, *args, **kwargs)' .'''
    global w, w_win, root
    #rt = root
    root = rt
    w = tk.Toplevel (root)
    GUIsupport.set_Tk_var()
    top = Toplevel1 (w)
    GUIsupport.init(w, top, *args, **kwargs)
    return (w, top)


def destroy_Toplevel1():
    global w
    w.destroy()
    w = None


class Toplevel1:
    def getValues(self):
        prio = int(self.Entry1.get())
        oorz_code = int(self.Entry2.get())
        oorz_group = str(self.Entry3.get())
        equip_type = str(self.Entry5.get())
        geo_code = int(self.Entry6.get())

        # prio = 1
        # oorz_code = 1
        # oorz_group = 'WEER'
        # equip_type = 'WISSEL'
        # geo_code = 1

        oorz_group, equip_type = self.model.enc_lab(oorz_group, equip_type)
        print(prio, oorz_code, oorz_group, equip_type, geo_code)
        return prio, oorz_code, oorz_group, equip_type, geo_code


    def predict(self):
        prio, oorz_code, oorz_group, equip_type, geo_code = self.getValues()
        prediction = self.model.predict(prio,oorz_code, oorz_group, equip_type, geo_code)
        prediction_prob = self.model.predict_prob(prio,oorz_code, oorz_group, equip_type, geo_code)
        if self.showDetails.get():
            details = self.model.getDetails(prio,oorz_code, oorz_group, equip_type, geo_code)
            self.Prediction.configure(text=f'Verwachte Duur: {int(prediction)} minuten.\n{prediction_prob.to_string(index=False)}')
        else:
            self.Prediction.configure(text=f'Verwachte Duur: {int(prediction)} minuten.')


    def __init__(self, top=None):
        self.model = Model()
        self.showDetails = tk.BooleanVar()
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'

        top.geometry("791x589+443+108")
        top.minsize(72, 15)
        top.maxsize(1920, 1080)
        top.resizable(1,  1)
        top.title("New Toplevel")
        top.configure(background="#d9d9d9")

        self.Frame1 = tk.Frame(top)
        self.Frame1.place(relx=0.025, rely=0.017, relheight=0.360, relwidth=0.601)
        self.Frame1.configure(relief='groove')
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief="groove")
        self.Frame1.configure(background="#d9d9d9")

        self.Button1 = tk.Button(self.Frame1)
        self.Button1.place(relx=0.779, rely=0.757, height=28, width=77)
        self.Button1.configure(activebackground="#ececec")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(text='''Voorspel''')
        self.Button1.configure(command=self.predict)

        self.wantDetails = tk.Checkbutton(self.Frame1, text='Show details', variable=self.showDetails, onvalue=True, offvalue=False)
        self.wantDetails.configure(background="#d9d9d9")
        self.wantDetails.configure(activebackground="#d9d9d9")
        self.wantDetails.configure(highlightbackground="#d9d9d9")
        self.wantDetails.grid(row=7,column=1)

        self.Entry1 = tk.Entry(self.Frame1)
        self.Entry1.grid(row=1,column=2)
        self.Entry1.configure(background="white")
        self.Entry1.configure(font="TkFixedFont")
        self.Entry1.configure(foreground="#000000")
        self.Entry1.configure(insertbackground="black")

        self.Entry2 = tk.Entry(self.Frame1)
        self.Entry2.grid(row=2,column=2)
        self.Entry2.configure(background="white")
        self.Entry2.configure(font="TkFixedFont")
        self.Entry2.configure(foreground="#000000")
        self.Entry2.configure(insertbackground="black")

        self.Entry3 = tk.Entry(self.Frame1)
        self.Entry3.grid(row=3,column=2)
        self.Entry3.configure(background="white")
        self.Entry3.configure(font="TkFixedFont")
        self.Entry3.configure(foreground="#000000")
        self.Entry3.configure(insertbackground="black")

        self.Entry5 = tk.Entry(self.Frame1)
        self.Entry5.grid(row=4,column=2)
        self.Entry5.configure(background="white")
        self.Entry5.configure(font="TkFixedFont")
        self.Entry5.configure(foreground="#000000")
        self.Entry5.configure(insertbackground="black")

        self.Entry6 = tk.Entry(self.Frame1)
        self.Entry6.grid(row=5,column=2)
        self.Entry6.configure(background="white")
        self.Entry6.configure(font="TkFixedFont")
        self.Entry6.configure(foreground="#000000")
        self.Entry6.configure(insertbackground="black")

        self.Text1 = tk.Text(self.Frame1)
        self.Text1.place(relx=1.095, rely=0.216, relheight=0.389, relwidth=0.368)

        self.Text1.configure(background="white")
        self.Text1.configure(font="TkTextFont")
        self.Text1.configure(foreground="black")
        self.Text1.configure(highlightbackground="#d9d9d9")
        self.Text1.configure(highlightcolor="black")
        self.Text1.configure(insertbackground="black")
        self.Text1.configure(selectbackground="blue")
        self.Text1.configure(selectforeground="white")
        self.Text1.configure(wrap="word")

        self.Label1 = tk.Label(self.Frame1)
        self.Label1.grid(row=1,column=1)
        self.Label1.configure(background="#d9d9d9")
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(text='''Prioriteit''')

        self.Label2 = tk.Label(self.Frame1)
        self.Label2.grid(row=2,column=1)
        self.Label2.configure(background="#d9d9d9")
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(text='''Oorzaakcode''')

        self.Label3 = tk.Label(self.Frame1)
        self.Label3.grid(row=3,column=1)
        self.Label3.configure(background="#d9d9d9")
        self.Label3.configure(foreground="#000000")
        self.Label3.configure(text='''Oorzaakgroep''')
        
        self.Label5 = tk.Label(self.Frame1)
        self.Label5.grid(row=4,column=1)
        self.Label5.configure(background="#d9d9d9")
        self.Label5.configure(foreground="#000000")
        self.Label5.configure(text='''Equipment soort''')

        self.Label6 = tk.Label(self.Frame1)
        self.Label6.grid(row=5,column=1)
        self.Label6.configure(background="#d9d9d9")
        self.Label6.configure(foreground="#000000")
        self.Label6.configure(text='''Geo code''')

        self.Frame2 = tk.Frame(top)
        self.Frame2.place(relx=0.025, rely=0.4, relheight=0.57
                , relwidth=0.953)
        self.Frame2.configure(relief='groove')
        self.Frame2.configure(borderwidth="2")
        self.Frame2.configure(relief="groove")
        self.Frame2.configure(background="#d9d9d9")

        self.Prediction = tk.Label(self.Frame2)
        self.Prediction.grid(row=0,column=1)
        self.Prediction.configure(background="#d9d9d9")
        self.Prediction.configure(foreground="#000000")
        self.Prediction.configure(text='')

        self.menubar = tk.Menu(top,font="TkMenuFont",bg=_bgcolor,fg=_fgcolor)
        top.configure(menu = self.menubar)

if __name__ == '__main__':
    vp_start_gui()




