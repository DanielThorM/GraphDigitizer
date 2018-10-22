@@ -0,0 +1,301 @@
import tkinter as tk
import tkinter.filedialog
import dill
import transparentDigitizer
import numpy as np



class curve(object):
    def __init__(self):
        self.ID = 'None'
        self.comment = ''
        self.y=None
        self.x=None

    def set_ID(self, ID):
        self.ID = ID

    def set_comment(self, comment):
        self.comment = comment

    def set_xy(self, x, y):
        self.x=x
        self.y=y

class digitizerGUI(object):
    def __init__(self, master):
        self.project=[]
        self.project.append(curve())
        self.current_index=0

        self.master=master

        master.title('Digitizer')
        menu=tk.Menu(master)
        master.config(menu=menu)
        ######## subMenu #########################
        subMenu=tk.Menu(menu)
        menu.add_cascade(label='File', menu=subMenu)
        subMenu.add_command(label='New project', command=self.new_project)
        subMenu.add_command(label='Save as... project', command=self.saveAs_project)
        subMenu.add_command(label='Save project', command=self.save_project)
        subMenu.add_command(label='Load project', command=self.load_project)
        subMenu.add_separator()
        subMenu.add_command(label='Exit', command=self.exit_func)

        ###################################################################
        ###### Frames #######################################
        mainFrame = tk.Frame(master)
        mainFrame.pack(side=tk.TOP, fill=tk.X)

        bottomFrame=tk.Frame(master)
        bottomFrame.pack(side=tk.TOP, fill=tk.X)


        mainFrameTop=tk.Frame(mainFrame)
        mainFrameTop.pack(side=tk.TOP, fill=tk.X, anchor=tk.E)
        mainFrameLeft = tk.Frame(mainFrame)
        mainFrameLeft.pack(side=tk.LEFT, anchor=tk.N + tk.E)
        mainFrameCenter = tk.Frame(mainFrame)
        mainFrameCenter.pack(side=tk.LEFT, anchor=tk.N, expand=tk.NO)
        mainFrameRight = tk.Frame(mainFrame)
        mainFrameRight.pack(side=tk.LEFT, anchor=tk.N + tk.W , expand=tk.YES)

        ##################################################
        #Top

        tk.Label(mainFrameLeft, text='List of curves').pack()
        self.curveList=tk.Listbox(mainFrameLeft, exportselection=False)
        self.curveList.pack()
        self.print_curve_list()
        #self.listVar.trace('w', self.print_article_list)
        self.curveList.bind('<<ListboxSelect>>', self.selected_curve)





        #################################################################
        #Digitizer
        button_add_from_graph = tk.Button(mainFrameCenter, text='New overlay', bg='Yellow', command=self.open_new_transparent_window)
        button_add_from_graph.grid(row=1, column=1, sticky=tk.W + tk.E)
        button_add_from_graph = tk.Button(mainFrameCenter, text='New curve', command=self.new_curve)
        button_add_from_graph.grid(row=2, column=1, sticky=tk.W + tk.E)
        button_add_from_graph = tk.Button(mainFrameCenter, text='Clear points', command=self.clear_points)
        button_add_from_graph.grid(row=3, column=1, sticky=tk.W + tk.E)
        button_set_origo = tk.Button(mainFrameCenter, text='Set origo', command=self.set_origo)
        button_set_origo.grid(row=4, column=1, sticky=tk.W + tk.E)
        button_set_x = tk.Button(mainFrameCenter, text='Set point on X', command=self.set_x_point)
        button_set_x.grid(row=5, column=1, sticky=tk.W + tk.E)
        button_set_y = tk.Button(mainFrameCenter, text='Set point on Y', command=self.set_y_point)
        button_set_y.grid(row=6, column=1, sticky=tk.W + tk.E)
        button_add_points = tk.Button(mainFrameCenter, text='Add graph points', command=self.set_points)
        button_add_points.grid(row=7, column=1, sticky=tk.W + tk.E)
        button_assign_data = tk.Button(mainFrameCenter, text='Assign data to curve', bg='green',
                                       command=self.assign_to_curve)
        button_assign_data.grid(row=8, column=1, sticky=tk.W + tk.E)




        ############################################################
        #Curve data
        tk.Label(mainFrameRight, text = 'Curve data', bg = 'gray').grid(row=0, columnspan=2, sticky= tk.E + tk.W)

        mainFrameRight.columnconfigure(1, weight=5)
        mainFrameRight.columnconfigure(1, weight=1)

        tk.Label(mainFrameRight, text = 'ID').grid(row=1, sticky=tk.W)
        self.entry_ID=tk.Entry(mainFrameRight)
        self.entry_ID.grid(row=1, column=1, sticky = tk.E+tk.W)
        self.entry_ID.bind('<Return>', self.update_ID)
        tk.Label(mainFrameRight, text='Comment').grid(row=2, sticky=tk.W)
        self.entry_comment = tk.Entry(mainFrameRight)
        self.entry_comment.grid(row=2, column=1, sticky = tk.E+tk.W)
        self.entry_comment.bind('<Return>', self.update_comment)


        ####################################################
        #Bottom
        tk.Label(bottomFrame, text='Data, [x,...][y, ...]').pack(anchor=tk.N+tk.W)
        self.dataText = tk.Text(bottomFrame, exportselection=False)
        self.dataText.pack(side=tk.LEFT, anchor=tk.N)
        scrollbar=tk.Scrollbar(bottomFrame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.dataText.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.dataText.yview)




    ################################################################
    #Transparent window
    def open_new_transparent_window(self):
        try:
            self.slave.destroy()
            del self.transparent_window
        except:
            pass
        self.slave = tk.Toplevel()
        self.slave.attributes('-alpha', 0.4)
        self.slave.geometry('600x600')
        self.slave.wm_attributes("-topmost", 1)
        self.transparent_window = transparentDigitizer.draw_on_window(self.slave)

    def set_origo(self):
        try:
            self.transparent_window.axes.promt_origo()
        except:
            self.transparent_window.axes = transparentDigitizer.define_axes(self.transparent_window)
            self.transparent_window.axes.promt_origo()

    def set_x_point(self):
        try:
            self.transparent_window.axes.promt_x_axis()
        except:
            self.transparent_window.axes = transparentDigitizer.define_axes(self.transparent_window)
            self.transparent_window.axes.promt_x_axis()

    def set_y_point(self):
        try:
            self.transparent_window.axes.promt_y_axis()
        except:
            self.transparent_window.axes = transparentDigitizer.define_axes(self.transparent_window)
            self.transparent_window.axes.promt_y_axis()

    def set_points(self):
        try:
            self.transparent_window.points.promt_points()
        except:
            self.transparent_window.points = transparentDigitizer.points(self.transparent_window)
            self.transparent_window.points.promt_points()

    def assign_to_curve(self):
        x,y = self.transparent_window.axes.interpolate_data(self.transparent_window.points.point_list)
        self.project[self.current_index].set_xy(x,y)
        self.print_data_data()


    def clear_points(self):
        try:
            self.transparent_window.points.clear_points()
        except:
            self.transparent_window.points = transparentDigitizer.points(self.transparent_window)
            self.transparent_window.points.clear_points()

    def select_regression_area(self):
        try:
            self.transparent_window.draw_rectangle.calculate_line()
        except:
            self.transparent_window.draw_rectangle = Digitizer.draw_rectangle(self.transparent_window)
            self.transparent_window.draw_rectangle.calculate_line()

    def calculate_slope(self):
        p0 = self.transparent_window.axes.interp_value([self.transparent_window.axes.origo_loc[0],
                                                        self.transparent_window.draw_rectangle.line[1] + (
                                                        self.transparent_window.axes.origo_loc[0]) *
                                                        self.transparent_window.draw_rectangle.line[0]])
        p1 = self.transparent_window.axes.interp_value([self.transparent_window.axes.origo_loc[0] + 20,
                                                        self.transparent_window.draw_rectangle.line[1] + (
                                                                    self.transparent_window.axes.origo_loc[0] + 20) *
                                                        self.transparent_window.draw_rectangle.line[0]])

        slope = (p1[0] - p0[0]) / (p1[1] - p0[1])
        print
        p1, p0
        return slope
    ##################################################################

    def print_curve_list(self):
        self.curveList.delete(0, tk.END)
        for item in self.project:
            self.curveList.insert(tk.END, item.ID)
        self.curveList.select_set(self.current_index)  # This only sets focus on the first item.
        self.curveList.event_generate("<<ListboxSelect>>")

    def print_curve_data(self):
        self.entry_ID.delete(0, tk.END)
        self.entry_ID.insert(0, str(self.project[self.current_index].ID))
        self.entry_comment.delete(0, tk.END)
        self.entry_comment.insert(0, str(self.project[self.current_index].comment))

    def print_data_data(self):
        self.dataText.delete(1.0, tk.END)
        self.dataText.insert(1.0, repr(np.array([self.project[self.current_index].x, self.project[self.current_index].y])))


    def update_ID(self, event):
        self.project[self.current_index].set_ID(str(event.widget.get()))
        self.print_curve_list()

    def update_comment(self, event):
        #print ('LOLL')
        self.project[self.current_index].set_comment(str(event.widget.get()))
        print (self.project[self.current_index].comment)

    def selected_curve(self, event):
        self.current_index=event.widget.curselection()[0]
        self.print_curve_data()
        self.print_data_data()
        #print ('{}'.format(self.current_index))


    def new_curve(self):
        self.project.append(curve())
        self.print_curve_list()

    #### File dropdown################################################
    def new_project(self):

        self.project = []
        self.project.append(curve())
        self.print_curve_list()
        self.saveAs_fileName=None
        #elf.listVar = tk.StringVar()

    def saveAs_project(self):
        # try:
        #     self.delete(self.transparent_window)
        # except:
        #     pass
        self.saveAs_fileName = tk.filedialog.asksaveasfilename(defaultextension=".pkl")
        with open(self.saveAs_fileName, 'wb') as output:
            dill.dump(self.project, output)
            print ('Saved as {}'.format(self.saveAs_fileName))

    def save_project(self):
        # try:
        #     self.delete(self.transparent_window)
        # except:
        #     pass
        try:
            with open(self.saveAs_fileName, 'wb') as output:
                dill.dump(self.project, output)
                print('Saved {}'.format(self.saveAs_fileName))
        except:
            self.saveAs_project()

    def load_project(self):
        load_fileName = tk.filedialog.askopenfilename()
        self.saveAs_fileName = load_fileName
        try:
            with open(load_fileName, 'rb') as input_file:
                self.project = dill.load(input_file)
            #Reload curve list
            print ('Loaded {}'.format(self.saveAs_fileName))
            self.print_curve_list()
        except:
            print ('Failed to load {}'.format(self.saveAs_fileName))

    def exit_func(self):
        self.master.destroy()





if __name__ == '__main__':
    root = tk.Tk()
    my_gui = digitizerGUI(root)
    root.mainloop()