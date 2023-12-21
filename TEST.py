

# x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
# index = ["Jan'18", "Feb'18", "Mar'18", "Apr'18", "May'18", "Jun'18", "Jul'18", "Aug'18", "Sep'18", "Oct'18", "Nov'18", "Dec'18"]

# df = pd.DataFrame(x, columns = ['cust_acq_pm'], index = index)

# root = Tk()

# figure = plt.Figure(figsize = (6,6), dpi = 100)
# ax1 = figure.add_subplot(111)
# bar = FigureCanvasTkAgg(figure, root)
# bar.get_tk_widget().grid(row = 0, column = 0)
# df.plot(kind = 'bar', xlabel = 'dates', ylabel = 'cust_acq_pm', ax = ax1)
# plt.xticks(x, index, rotation = 'horizontal')
# ax1.set_title('Test')

# test_button = Button(root, bg = "red", fg = "white", text = "Click me!")
# test_button.grid(row = 1, column = 0)

# root.mainloop()

# from tkinter import *
# import pandas as pd
# from GraphClass import *
# import GraphGrid

# root = Tk()

# canvas = Canvas(root)
# canvas.pack()

# Graph.df = pd.DataFrame()

# p6_graph_obj = Graph(canvas)
# column_name = Graph.metrics_column_ids[3][1]
# column_data = p6_graph_obj.getColumnData(column_name)

# p6_xlabels = p6_graph_obj.get_xlabels()
# p6_df = pd.DataFrame(column_data, columns = [column_name], index = p6_xlabels)
# p6_ylabels = GraphGrid.GraphGrid.all_graphs[0][2]
        
# p6_graph_obj.draw_graph(p6_xlabels, p6_ylabels, p6_df)



# import PasswordClass

# password = PasswordClass.Password()
# password.password = "Hello World"

# enc = password.encryptPassword()
# print("\n\n")
# print(enc)
# print("\n\n")

# dec = password.decryptPassword(enc)
# print("\n\n")
# print(dec)
# print("\n\n")

# print("\n\n")

# p1 = "p@123"
# print(str(hash(p1)))

# p2 = "p@123"
# print(str(hash(p2)))

# print("\n\n")



# import hashlib as hash

# msg = "p@123"
# msg_bytes = msg.encode()

# print("\n\n")
# print("Using SHA-3: ")
# print(hash.sha3_256(msg_bytes).hexdigest())
# print("\n\n")

import datetime
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt

# Create the PdfPages object to which we will save the pages:
# The with statement makes sure that the PdfPages object is closed properly at
# the end of the block, even if an Exception occurs.
with PdfPages('multipage_pdf.pdf') as pdf:
    plt.figure(figsize=(3, 3))
    plt.plot(range(7), [3, 1, 4, 1, 5, 9, 2], 'r-o')
    plt.title('Page One')
    pdf.savefig()  # saves the current figure into a pdf page
    plt.close()

    # if LaTeX is not installed or error caught, change to `False`
    plt.figure(figsize=(8, 6))
    x = np.arange(0, 5, 0.1)
    plt.plot(x, np.sin(x), 'b-')
    plt.title('Page Two')
    pdf.attach_note("plot of sin(x)")  # attach metadata (as pdf note) to page
    pdf.savefig()
    plt.close()

    plt.rcParams['text.usetex'] = False
    fig = plt.figure(figsize=(4, 5))
    plt.plot(x, x ** 2, 'ko')
    plt.title('Page Three')
    pdf.savefig(fig)  # or you can pass a Figure object to pdf.savefig
    plt.close()

