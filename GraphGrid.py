"""
GraphGrid: Class that manages the grid of graphs.
Used in Page 5 (AllGraphsPage) and Page 6 (SingleGraphsPage)
Functions:
- Ability to manage and display the names of graphs
- Ability to draw the rectangles and write the texts on Page 5
"""

from PagesClass import *
from tkinter import *
from tkinter.font import Font
from tkmacosx import Button

class GraphGrid:

    
    # [graph_id, graph_name, graph_desc]
    all_graphs = [
        [1, "Customers \n acquired p.m.", "No. of customers acquired per month"],
        [2, "Customers \n lost p.m.", "No. of customers lost per month"],
        [3, "Total \n customers p.m.", "Total customers per month"],
        [4, "Avg. Revenue per \n customer p.m.", "Avg. revenue per customer per month"],
        [5, "Cost of goods \n sold p.m.", "Cost of goods sold per month"],
        [6, "Total sales \n costs p.m.", "Total sales costs per month"],
        [7, "Total marketing \n costs p.m.", "Total marketing costs per month"],
        [8, "Total R&D \n costs p.m.", "Total R&D costs per month"],
        [9, "Misc. operational \n costs p.m.", "Miscellaneous operational costs"],
        [10, "Gross profit \n margin p.m.", "Gross profit margin per month"],
        [11, "Net profit \n margin p.m.", "Net profit margin per month"],
        [12, "Annual \n recurring revenue", "Annual recurring revenue"],
        [13, "Customer growth \n rate p.m.", "Customer growth rate per month"],
        [14, "Revenue growth \n rate p.m.", "Revenue growth rate per month"],
        [15, "Generate \n PDF for \n Company", ""]
    ]

    # class attribute
    SELECTED_GRAPH_ID = 0

    def __init__(self, company_id, graph_id):
        self.graph_id = graph_id
        self.company_id = company_id

    @classmethod
    def getGraphInfo(cls):
        return (cls.all_graphs)

    def setGraphId(self, graph_id):
        self.graph_id = graph_id
    
    def setGraphName(self, graph_name):
        self.graph_name = graph_name
    
    def setGraphDesc(self, graph_desc):
        self.graph_desc = graph_desc
    
    def getGraphId(self):
        return (self.graph_id)
    
    def getGraphName(self):
        return (GraphGrid.all_graphs[self.graph_id - 1][1])
    
    def getGraphDesc(self):
        return (GraphGrid.all_graphs[self.graph_id - 1][2])

    # (topleftcorner_x, topleftcorner_y, bottomrightcorner_x, bottomrightcorner_y, canvas)
    def createGraphRect(self, x1, y1, x2, y2, canvas, color, activecolor):
        graph_rect = canvas.create_rectangle(x1, y1, x2, y2, fill = color, activefill = activecolor, width = 0)
        return graph_rect

    def createGraphText(self, x1, y1, x2, y2, canvas, weight):
        graph_text = canvas.create_text(((x1 + x2)/2, (y1 + y2)/2), text = self.getGraphName(),
                                        font = Font(family = "Helvetica Neue", size = 20, weight = weight), justify = CENTER)
        return graph_text
