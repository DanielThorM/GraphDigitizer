
import tkinter as tk
import tkinter.filedialog
import dill
import DigitizingWindow
import numpy as np



class Curve(object):
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

class DigitizerGUI(object):
    def __init__(self, master):
        self.project=[]
        self.project.append(Curve())
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
        main_frame = tk.Frame(master)
        main_frame.pack(side=tk.TOP, fill=tk.X)

        bottom_frame=tk.Frame(master)
        bottom_frame.pack(side=tk.TOP, fill=tk.X)


        main_frame_top=tk.Frame(main_frame)
        main_frame_top.pack(side=tk.TOP, fill=tk.X, anchor=tk.E)
        main_frame_left = tk.Frame(main_frame)
        main_frame_left.pack(side=tk.LEFT, anchor=tk.N + tk.E)
        main_frame_center = tk.Frame(main_frame)
        main_frame_center.pack(side=tk.LEFT, anchor=tk.N, expand=tk.NO)
        main_frame_right = tk.Frame(main_frame)
        main_frame_right.pack(side=tk.LEFT, anchor=tk.N + tk.W , expand=tk.YES)

        ##################################################
        #Top

        tk.Label(main_frame_left, text='List of curves').pack()
        self.curve_list=tk.Listbox(main_frame_left, exportselection=False)
        self.curve_list.pack()
        self.print_curve_list()
        #self.listVar.trace('w', self.print_article_list)
        self.curve_list.bind('<<ListboxSelect>>', self.selected_curve)





        #################################################################
        #Digitizer
        button_add_from_graph = tk.Button(main_frame_center, text='New overlay', bg='Yellow', command=self.open_new_transparent_window)
        button_add_from_graph.grid(row=1, column=1, sticky=tk.W + tk.E)
        button_add_from_graph = tk.Button(main_frame_center, text='New curve', command=self.new_curve)
        button_add_from_graph.grid(row=2, column=1, sticky=tk.W + tk.E)
        button_add_from_graph = tk.Button(main_frame_center, text='Clear points', command=self.clear_points)
        button_add_from_graph.grid(row=3, column=1, sticky=tk.W + tk.E)
        button_set_origo = tk.Button(main_frame_center, text='Set origo', command=self.set_origo)
        button_set_origo.grid(row=4, column=1, sticky=tk.W + tk.E)
        button_set_x = tk.Button(main_frame_center, text='Set point on X', command=self.set_x_reference)
        button_set_x.grid(row=5, column=1, sticky=tk.W + tk.E)
        button_set_y = tk.Button(main_frame_center, text='Set point on Y', command=self.set_y_reference)
        button_set_y.grid(row=6, column=1, sticky=tk.W + tk.E)
        button_add_points = tk.Button(main_frame_center, text='Add graph points', bg='violet', command=self.add_points)
        button_add_points.grid(row=7, column=1, sticky=tk.W + tk.E)
        button_assign_data = tk.Button(main_frame_center, text='Assign data to curve', bg='green',
                                       command=self.assign_to_curve)
        button_assign_data.grid(row=8, column=1, sticky=tk.W + tk.E)



        ###################################
        #LogAxis
        self.log_axis_x = tk.IntVar()
        self.log_axis_y = tk.IntVar()
        self.start_in_origo = tk.IntVar()
        cButton_logX = tk.Checkbutton(
            main_frame_center, text="log axis X", variable=self.log_axis_x,
            onvalue=1, offvalue=0)
        cButton_logY = tk.Checkbutton(
            main_frame_center, text="log axis Y", variable=self.log_axis_y,
            onvalue=1, offvalue=0)
        cButton_logX.grid(row=5, column=2, sticky=tk.W + tk.E)
        cButton_logY.grid(row=6, column=2, sticky=tk.W + tk.E)

        cButton_incl_origo= tk.Checkbutton(
            main_frame_center, text="Start in 0", variable=self.start_in_origo,
            onvalue=1, offvalue=0)
        cButton_incl_origo.grid(row=7, column=2, sticky=tk.W + tk.E)

        ############################################################
        #Curve data
        tk.Label(main_frame_right, text = 'Curve data', bg = 'gray').grid(row=0, columnspan=2, sticky= tk.E + tk.W)

        main_frame_right.columnconfigure(1, weight=5)
        main_frame_right.columnconfigure(1, weight=1)

        tk.Label(main_frame_right, text = 'ID').grid(row=1, sticky=tk.W)
        self.entry_ID=tk.Entry(main_frame_right)
        self.entry_ID.grid(row=1, column=1, sticky = tk.E+tk.W)
        self.entry_ID.bind('<Return>', self.update_ID)
        tk.Label(main_frame_right, text='Comment').grid(row=2, sticky=tk.W)
        self.entry_comment = tk.Entry(main_frame_right)
        self.entry_comment.grid(row=2, column=1, sticky = tk.E+tk.W)
        self.entry_comment.bind('<Return>', self.update_comment)


        ####################################################
        #Bottom
        tk.Label(bottom_frame, text='Data, [x,...][y, ...]').pack(anchor=tk.N+tk.W)
        self.dataText = tk.Text(bottom_frame, exportselection=False)
        self.dataText.pack(side=tk.LEFT, anchor=tk.N)
        scrollbar=tk.Scrollbar(bottom_frame)
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
        self.transparent_window = DigitizingWindow.DrawOnWindow(self.slave)

    def set_origo(self):
        try:
            self.transparent_window.axes.promt_origo(self.log_axis_x.get(), self.log_axis_y.get())
        except:
            self.transparent_window.axes = DigitizingWindow.DefineAxes(self.transparent_window)
            self.transparent_window.axes.promt_origo(self.log_axis_x.get(), self.log_axis_y.get())
            print (str(self.log_axis_x.get()))

    def set_x_reference(self):
        try:
            self.transparent_window.axes.promt_x_axis()
        except:
            self.transparent_window.axes = DigitizingWindow.DefineAxes(self.transparent_window)
            self.transparent_window.axes.promt_x_axis()

    def set_y_reference(self):
        try:
            self.transparent_window.axes.promt_y_axis()
        except:
            self.transparent_window.axes = DigitizingWindow.DefineAxes(self.transparent_window)
            self.transparent_window.axes.promt_y_axis()

    def add_points(self):
        try:
            self.transparent_window.points.promt_points()
        except:
            self.transparent_window.points = DigitizingWindow.Point(self.transparent_window)
            self.transparent_window.points.promt_points()

    def assign_to_curve(self):
        x,y = self.transparent_window.axes.interpolate_data(self.transparent_window.points.point_list)
        if self.start_in_origo.get() == 1:
            x = np.insert(x, 0, 0.0)
            y = np.insert(y, 0, 0.0)
        self.project[self.current_index].set_xy(x,y)
        self.print_data_data()


    def clear_points(self):
        try:
            self.transparent_window.points.clear_points()
        except:
            self.transparent_window.points = DigitizingWindow.Point(self.transparent_window)
            self.transparent_window.points.clear_points()

    def select_regression_area(self):
        try:
            self.transparent_window.draw_rectangle.calculate_line()
        except:
            self.transparent_window.draw_rectangle = DigitizingWindow.DrawRectangle(self.transparent_window)
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
        self.curve_list.delete(0, tk.END)
        for item in self.project:
            self.curve_list.insert(tk.END, item.ID)
        self.curve_list.select_set(self.current_index)  # This only sets focus on the first item.
        self.curve_list.event_generate("<<ListboxSelect>>")

    def print_curve_data(self):
        self.entry_ID.delete(0, tk.END)
        self.entry_ID.insert(0, str(self.project[self.current_index].ID))
        self.entry_comment.delete(0, tk.END)
        self.entry_comment.insert(0, str(self.project[self.current_index].comment))

    def print_data_data(self):
        self.dataText.delete(1.0, tk.END)
        self.dataText.insert(1.0, 'np.'+repr(np.array([self.project[self.current_index].x, self.project[self.current_index].y])))


    def update_ID(self, event):
        self.project[self.current_index].set_ID(str(event.widget.get()))
        self.print_curve_list()

    def update_comment(self, event):
        self.project[self.current_index].set_comment(str(event.widget.get()))
        print (self.project[self.current_index].comment)

    def selected_curve(self, event):
        self.current_index=event.widget.curselection()[0]
        self.print_curve_data()
        self.print_data_data()
        #print ('{}'.format(self.current_index))


    def new_curve(self):
        self.project.append(Curve())
        self.print_curve_list()

    #### File dropdown################################################
    def new_project(self):

        self.project = []
        self.project.append(Curve())
        self.print_curve_list()
        self.saveAs_fileName=None
        #elf.listVar = tk.StringVar()

    def saveAs_project(self):
        self.saveAs_fileName = tk.filedialog.asksaveasfilename(defaultextension=".pkl")
        with open(self.saveAs_fileName, 'wb') as output:
            dill.dump(self.project, output)
            print ('Saved as {}'.format(self.saveAs_fileName))

    def save_project(self):
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
    my_gui = DigitizerGUI(root)
    root.mainloop()