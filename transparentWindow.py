# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 23:12:46 2017

@author: danieltm
"""
import tkinter as tk
import tkinter.simpledialog
import numpy as np
import matplotlib.figure as mplfig
import matplotlib.backends.backend_tkagg as tkagg
import re


class draw_on_window(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title("Lines")
        self.pack(fill=tk.BOTH, expand=1)

        self.canvas = tk.Canvas(self)
        self.cursor_vert = tk.PhotoImage(master=self.canvas, width=1, height=2280)
        self.cursor_hor = tk.PhotoImage(master=self.canvas, width=2280, height=1)

        dat_vert = ('red',) * 2280
        self.cursor_vert.put(dat_vert, to=(0, 0))
        self.cursor_vert_box = self.canvas.create_image(0, 0, image=self.cursor_vert, anchor='nw')
        for i in range(2280):
            self.cursor_hor.put(('red',), to=(i, 0))
        self.cursor_hor_box = self.canvas.create_image(0, 0, image=self.cursor_hor, anchor='nw')

        #        self.canvas.create_line(15, 25, 200, 25, fill='red')
        #        self.canvas.create_line(300, 35, 300, 200, dash=(4, 2))
        #        self.canvas.create_line(55, 85, 155, 85, 105, 180, 55, 85)

        self.canvas.pack(fill=tk.BOTH, expand=1)

        self.canvas.bind('<Motion>', self.on_motion)

    def on_motion(self, event):
        vert_left, vert_top = self.canvas.coords(self.cursor_vert_box)
        hor_left, hor_top = self.canvas.coords(self.cursor_hor_box)
        dx = event.x - (vert_left)
        dy = event.y - (hor_top)
        self.canvas.move(self.cursor_vert_box, dx, 0)
        self.canvas.move(self.cursor_hor_box, 0, dy)


class points:
    def __init__(self, window):
        self.canvas = window.canvas

    def promt_points(self):
        if hasattr(self, 'point_list') != True:
            self.point_list = []
        self.canvas.bind('<Button-1>', self.on_l_click)
        self.canvas.bind('<Button-3>', self.on_r_click)

    def on_l_click(self, event):
        self.point_list.append([event.x, event.y])

        self.datapoints_plot = self.xcross(self.point_list[-1], 'red', str(len(self.point_list)))

    def on_r_click(self, event):
        del self.point_list[-1]
        self.canvas.delete(self.canvas.find_withtag('v' + str(len(self.point_list) + 1)))
        self.canvas.delete(self.canvas.find_withtag('h' + str(len(self.point_list) + 1)))

    #    def dot(self, location, color):
    #        x1, y1 = (location[0] - 2), (location[1] - 2)
    #        x2, y2 = (location[0]+2), (location[1] + 2)
    #        return self.canvas.create_oval(x1, y1, x2, y2, fill=color)

    def xcross(self, location, color, tag):
        return [self.canvas.create_line(location[0] + 4, location[1] - 4, location[0] - 4, location[1] + 4, fill=color,
                                        tags='v' + tag),
                self.canvas.create_line(location[0] - 4, location[1] - 4, location[0] + 4, location[1] + 4, fill=color,
                                        tags='h' + tag)]
    def clear_points(self):
        for i in range(len(self.point_list)):

            self.canvas.delete(self.canvas.find_withtag('v{}'.format(i+1)))
            self.canvas.delete(self.canvas.find_withtag('h{}'.format(i+1)))
        self.point_list=[]
class define_axes:
    def __init__(self, window):
        self.canvas = window.canvas

    def promt_origo(self, logAxisX, logAxisY):
        try:
            self.canvas.delete('origo_dot')
        except:
            pass
        self.canvas.bind('<Button-1>', lambda event: self.on_l_click(event, 'origo'))
        self.origo_value=[0,0]
        self.logAxisX=logAxisX
        self.logAxisY=logAxisY

    # def set_origo(self, event):
    #     self.origo_loc = [event.x, event.y]
    #     try:
    #         self.canvas.delete(self.origo_dot)
    #     except:
    #         pass
    #     self.origo_dot = self.dot(self.origo_loc, 'red')


        #print[event.x, event.y]

    def promt_x_axis(self):
        self.canvas.bind('<Button-1>', lambda event: self.on_l_click(event, 'x_axis'))

    def promt_y_axis(self):
        self.canvas.bind('<Button-1>', lambda event: self.on_l_click(event, 'y_axis'))

    def on_l_click(self, event, attrstring):
        setattr(self, attrstring + '_loc', [event.x, event.y])
        try:
            self.canvas.delete(getattr(self, attrstring + '_line'))
            self.canvas.delete(getattr(self, attrstring + '_dot'))
        except:
            pass
        try:
            setattr(self, attrstring + '_line', self.canvas.create_line(self.origo_loc[0], self.origo_loc[1],
                                                                        getattr(self, attrstring + '_loc')[0],
                                                                        getattr(self, attrstring + '_loc')[1],
                                                                        width=1.0, fill='red'))
        except:
            pass
        setattr(self, attrstring + '_dot', self.dot(getattr(self, attrstring + '_loc'), 'red'))
        if attrstring!='origo':
            setattr(self, attrstring + '_value',
                    float(tk.simpledialog.askstring('Value', 'enter value of ' + attrstring.split('_')[0] + ' axis point',
                                                   parent=self.canvas)))

        else:
            if self.logAxisX == 1:
                self.origo_value[0] = float(tk.simpledialog.askstring('Value', 'enter X value of origo',
                                                                      parent=self.canvas))
            if self.logAxisY == 1:
                self.origo_value[1] = float(tk.simpledialog.askstring('Value', 'enter Y value of origo',
                                                                      parent=self.canvas))
        #print([event.x, event.y])

    def dot(self, location, color='red'):
        x1, y1 = (location[0] - 2), (location[1] - 2)
        x2, y2 = (location[0] + 2), (location[1] + 2)
        return self.canvas.create_oval(x1, y1, x2, y2, fill=color)

    def interp_value(self, pix):
        origo = np.array(self.origo_loc, dtype=np.float)
        x_axis = np.array(self.x_axis_loc, dtype=np.float)
        y_axis = np.array(self.y_axis_loc, dtype=np.float)


        alpha=(x_axis - origo)/(self.x_axis_value)
        beta=(y_axis - origo)/(self.y_axis_value)

        values=np.dot(np.matrix([alpha, beta]).T.I, pix-origo)
        x = values[0,0]
        y = values[0,1]

        if self.logAxisX == 1:
            decades=int(np.log10(self.x_axis_value)-np.log10(self.origo_value[0]))
            x=10**(x*decades/ self.x_axis_value)

        if self.logAxisY == 1:
            decades = int(np.log10(self.y_axis_value) - np.log10(self.origo_value[1]))
            y = 10 ** (y * decades / self.y_axis_value)

        return [x, y]

    def interpolate_data(self, points):
        pix_list = np.array(points, dtype=np.float)
        TempList = np.array([self.interp_value(loc) for loc in pix_list])
        y, x = TempList[:, 0], TempList[:, 1]
        return y, x


class draw_rectangle:
    def __init__(self, window):
        self.canvas = window.canvas
        self.points = np.array(window.points.points)
        self.item = None

        # self.canvas.create_line(0,0,100,100, width=3.0, fill='red')

    def draw(self, start, end, **opts):
        return self.canvas.create_rectangle(*(list(start) + list(end)), **opts)

    def autodraw(self, **opts):
        self.start = None
        self.canvas.bind('<Button-1>', self.__update)
        self.canvas.bind('<B1-Motion>', self.__update)
        self.canvas.bind('<ButtonRelease-1>', self.__stop)  # '+'# adds callback to list

    def __update(self, event):
        if not self.start:
            self.start = [event.x, event.y]
            return
        if self.item is not None:
            self.canvas.delete(self.item)
        self.item = self.draw(self.start, [event.x, event.y])
        self.rectangle = list(self.start) + [event.x, event.y]

    def __stop(self, event):
        self.start = None
        self.canvas.delete(self.item)
        self.item = None
        self.rectangle_set = True

        setattr(self, self.varName, self.regression_in_rectangle())
        # except:
        #   print 'Failed to regress line'

    def regression_in_rectangle(self):
        # print self.points.points
        points_in_window = np.array([point for point in self.points if point[0] >= self.rectangle[0]
                                     and point[0] <= self.rectangle[2] and point[1] >= self.rectangle[1] and point[1] <=
                                     self.rectangle[3]])
        print
        points_in_window
        pixel_line_coeff = np.polyfit(points_in_window[:, 0], points_in_window[:, 1], 1)

        try:
            self.canvas.delete(self.rectangle_line)
        except:
            pass
        self.rectangle_line = self.canvas.create_line(0, int(pixel_line_coeff[1]),
                                                      1280, int(pixel_line_coeff[1] + 1280 * pixel_line_coeff[0]),
                                                      fill='red')
        return np.polyfit(points_in_window[:, 0], points_in_window[:, 1], 1)

    def calculate_line(self):
        self.varName = 'line'
        self.autodraw()
        # print 'Failed to calculate youngs'


class show_plot(tk.Frame):
    def __init__(self, parent, data):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.data = data
        self.plot_plot()

    def plot_plot(self):
        self.parent.title('Plot of data')
        self.pack(fill=tk.BOTH, expand=1)

        self.canvas = tk.Canvas(self)

        self.fig = mplfig.Figure(figsize=(4, 4))
        self.subplot = self.fig.add_subplot(111)
        self.subplot.set_ylabel('Y')
        self.subplot.set_xlabel('X')
        self.subplot.plot(self.data[1], self.data[0])
        self.canvas = tkagg.FigureCanvasTkAgg(self.fig, master=self.parent)
        self.subplot.grid(True)

        # self.ax.set_xticklabels([])
        # self.ax.set_yticklabels([])
        self.canvas.get_tk_widget().pack()
        self.canvas.draw()


if __name__ == '__main__':
    root = tk.Tk()

    root_thing = show_plot(root, [[0, 1], [0, 2]])

    root.mainloop()
