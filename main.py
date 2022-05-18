import networkx as nx
from tkinter import *
from tkinter import ttk
import matplotlib.patches
import matplotlib.pyplot as plt
import matplotlib.style
import tkinter as tk
from matplotlib import animation
from queue import Queue
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from queue import PriorityQueue
from networkx.drawing.nx_pydot import pydot_layout, graphviz_layout
from collections import defaultdict
#####################################################################################################
#                                         N O T E S                                                #
####################################################################################################
''''
Inputs

a 0 b
a 1 b
b 1 b
b 0 a

q0 1 q1
q0 0 q2
q1 0 q3
q1 1 q0
q2 0 q1
q2 1 q1
q3 0 q2
q3 1 q0
'''

class Node:
    def __init__(self, value, cost = 0):
        self.value = value
        self.cost = cost

#####################################################################################################
#                                        START OF GRAPH                                             #
####################################################################################################
class Graph:
    def __init__(self, formatted_input):

        self.graph = defaultdict(list)
        self.isAccepted = False

        for lst in formatted_input:
            self.graph[lst[0]].append(Node(value=lst[2], cost=lst[1]))
            self.graph[lst[1]]

        self._Gr = nx.DiGraph()

        for line in formatted_input:
            self._Gr.add_node(line[0])
            self._Gr.add_node(line[2])


            if self._Gr.has_edge(line[0],line[2]):
                oldWeight = nx.get_edge_attributes(self._Gr,"label")
                weightLabel = line[1]+","+oldWeight[(line[0],line[2])]
                self._Gr.add_edge(line[0], line[2], label= weightLabel)

            else:
                if line[0] == line[2]:
                    self._Gr.add_edge(line[0], line[2], label="               "+line[1])

                else:
                    self._Gr.add_edge(line[0], line[2], label=line[1])

        self.labels = nx.get_edge_attributes(self._Gr, 'label')

        self._l = []
        self.solution = ""
        self._colors = ['blue'] * self._Gr.number_of_nodes()
        self._layout = nx.spring_layout(self._Gr)


    def trace(self, initialState,finalStates,inputSequence,formatted_input):
        self._l.append(Node(initialState))
        for item in inputSequence:
            for line in formatted_input:
                if line[0] == self._l[-1].value:
                    if line[1] == item:
                        self._l.append(Node(line[2]))
                        break

        for item in self._l:
            print("Sequence", item.value)

        self.solution="Not Accepted"
        for item in finalStates:
            if item == self._l[-1].value:
                self.isAccepted = True
                self.solution="Accepted"


    def update(self, frames, a):
        a.clear()
        self._colors = ['blue'] * self._Gr.number_of_nodes()

        if frames <len(self._l):
            i = 0
            for node in self._Gr.nodes:
                if node == self._l[frames].value:
                    break
                i += 1

            if self.isAccepted:
                self._colors[i] = 'orange'
            else:
                self._colors[i] = 'red'

            pos_attrs = {}
            for node, coords in self._layout.items():
                pos_attrs[node] = (coords[0], coords[1] + 4)

            nx.draw_networkx(self._Gr, pos=self._layout, with_labels=True, node_color=self._colors,
                             ax=a,connectionstyle="Arc3, rad=0.1")


            nx.draw_networkx_edge_labels(self._Gr, pos=self._layout, edge_labels=self.labels, ax=a,label_pos=0.15,bbox=dict(facecolor="skyblue", edgecolor='black', boxstyle='round,pad=0.2'))
            a.set_title("Frame {}".format(frames))

        if frames == len(self._l) -1:
            self._colors = ['blue'] * self._Gr.number_of_nodes()




    def anim(self):
        fig = plt.Figure(figsize=(7, 5))
        ax = fig.add_subplot(111)
        plt.axis('off')
        canvas = FigureCanvasTkAgg(fig, frm_left)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0)
        ani = animation.FuncAnimation(fig, self.update, frames=len(self._l), interval=700,fargs={ax})
        canvas = FigureCanvasTkAgg(fig, frm_left)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0)
#####################################################################################################
#                                         END OF GRAPH                                              #
####################################################################################################

#####################################################################################################
#                               START OF BUTTON EVENT LISTENER                                      #
####################################################################################################

def onClickRun(user_initialState,user_finalState, user_transitionTable,user_alphabet,user_states,user_sequence):
  inputTransitionTable = user_transitionTable.get("1.0", "end-1c").split('\n')
  inputInitialState = user_initialState.get("1.0", "end-1c")
  inputFinalStates= user_finalState.get("1.0", "end-1c").split(' ')
  inputAlphabet = user_alphabet.get("1.0", "end-1c").split(' ')
  inputStates = user_states.get("1.0", "end-1c").split(' ')
  inputSequence = user_sequence.get("1.0", "end-1c").split(' ')

  formatted_input = []
  for x in inputTransitionTable:
      formatted_input.append((x.split(' ')))

  initialState = False
  finalState = False
  transitionErrorFree= True
  transitionDict={}

  for item in inputStates:
      transitionDict[item] = []
      if item == inputInitialState:
          initialState = True

      for x in inputFinalStates:
          if item == x:
              finalState = True

  if finalState == False:
      tk.messagebox.showinfo("Error", "Check that the final state exists in the state set")
  if initialState == False:
      tk.messagebox.showinfo("Error", "Check that the initial state exists in the state set")

  for line in formatted_input:
      if line[0] not in inputStates or line[2] not in inputStates:
          transitionErrorFree = False
          tk.messagebox.showinfo("Error", "The states in the transition table don't match with the states set")
          break

      if line[1] not in inputAlphabet:
         transitionErrorFree = False
         tk.messagebox.showinfo("Error", "The alphabet in the transition table don't match with the alphabet set")
         break

      transitionDict[line[0]] += line[1]
      print("transition dictionary",transitionDict)

  for x in inputSequence:
      if x not in inputAlphabet:
          transitionErrorFree = False
          tk.messagebox.showinfo("Error", "The alphabet in the sequence don't match with the alphabet set")
          break

  for item in transitionDict:
     if len(transitionDict[item]) != len(inputAlphabet):
         transitionErrorFree = False
         tk.messagebox.showinfo("Error","State " + str(item) + " doesn't have right transitions ")
         break

     element = transitionDict[item][0]
     for x in range(1,len(transitionDict[item])):
         if element == transitionDict[item][x]:
             transitionErrorFree = False
             tk.messagebox.showinfo("Error", "Alphabet " + str(element) + " is repeated more than once from state " + str(item))
             break;
             element = transitionDict[item][x]


  if initialState == True and finalState == True and transitionErrorFree == True:
          dfs_inst = Graph(formatted_input)
          dfs_inst.trace(inputInitialState,inputFinalStates,inputSequence,formatted_input)
          dfs_inst.anim()
          lbl_bottom['text'] = dfs_inst.solution

#####################################################################################################
#                              END OF OF BUTTON EVENT LISTENER                                     #
####################################################################################################

#####################################################################################################
#                                    START OF GUI                                                   #
####################################################################################################
root = Tk()
root.resizable(FALSE,FALSE)
root.title("DFA Visualizer")
root.config(background="dark cyan")

frm_right = tk.Frame()
frm_right.config(background="dark cyan")
var1 = tk.StringVar()
lbl_finalState = tk.Label(master=frm_right, text="Enter the final state(s)", height=1, background="dark cyan", font=("Verdana",12,'bold'),fg="white")
txtFinalState = tk.Text(master=frm_right, height=2, width=12,font=("Verdana",12),fg="black")
lbl_alphabet = tk.Label(master=frm_right, text="Enter the alphabet", height=1, background="dark cyan", font=("Verdana",12,'bold'),fg="white")
txtAlphabet = tk.Text(master=frm_right, height=2, width=12,font=("Verdana",12),fg="black")
lbl_states = tk.Label(master=frm_right, text="Enter the states", height=1, background="dark cyan", font=("Verdana",12,'bold'),fg="white")
txtStates = tk.Text(master=frm_right, height=2, width=12,font=("Verdana",12),fg="black")
lbl_sequence = tk.Label(master=frm_right, text="Enter the sequence", height=1, background="dark cyan", font=("Verdana",12,'bold'),fg="white")
txtSequence = tk.Text(master=frm_right, height=2, width=12,font=("Verdana",12),fg="black")

btn_Run = tk.Button(master=frm_right, text="   Run   ",command=lambda:onClickRun(txtInitialState,txtFinalState,txt,txtAlphabet,txtStates,txtSequence) ,height=1,background="dark cyan",font=("Verdana",12,'bold'),fg="white")
lbl_finalState.grid(row=0, column=0,pady=0)
txtFinalState.grid(row=1, column=0,pady=(5,24))
lbl_alphabet.grid(row=2, column=0,pady=0)
txtAlphabet.grid(row=3, column=0,pady=(5,24))
lbl_states.grid(row=4, column=0,pady=0)
txtStates.grid(row=5, column=0,pady=(5,24))
lbl_sequence.grid(row=6, column=0,pady=0)
txtSequence.grid(row=7, column=0,pady=(5,24))
btn_Run.grid(row=9, column=0, padx=5, pady=(5,100))

frm_middle=tk.Frame()
frm_middle.config(background="dark cyan")
lbl_initialState = tk.Label(master=frm_middle, text="Enter the initial state", height=1, background="dark cyan", font=("Verdana",12,'bold'),fg="white")
txtInitialState = tk.Text(master=frm_middle, height=2, width=5,font=("Verdana",12),fg="black")
lbl_states = tk.Label(master=frm_middle,width=15,height=1, text="Transitions", background="dark cyan",font=("Verdana",12,'bold'),fg="white")
txt = tk.Text(master=frm_middle, height=20, width=18,font=("Verdana",12),fg="black")

lbl_initialState.grid(row=0, column=0,pady=0)
txtInitialState.grid(row=1, column=0, pady=(5,24))
lbl_states.grid(row=2, column=0, padx=8, pady=8)
txt.grid(row=3, column=0, pady=1)

scroll = ttk.Scrollbar(frm_middle)
scroll.config(command=txt.yview)
txt.config(yscrollcommand=scroll.set)
scroll.grid(row=3, column=3,sticky='NS',padx=0)

frm_left = tk.Frame()
frm_left.config(background="dark cyan")
lbl_top = tk.Label(master=frm_left, text="DFA Visualizer",  background="dark cyan", font=("Verdana",12,'bold'),fg="white")
lbl_bottom = tk.Label(master=frm_left, text="Written Results", background="dark cyan", font=("Verdana",12,'bold'),fg="white")

lbl_top.grid(row=0, column=0, padx=5, pady=5)
lbl_bottom.grid(row=2, column=0, padx=5, pady=(30,30))

fig = plt.Figure(figsize=(8, 5))
canvas = FigureCanvasTkAgg(fig, frm_left)
canvas.draw()
canvas.get_tk_widget().grid(row=1, column=0,padx=30)

frm_right.grid(row=0, column=2, padx=5, pady=5)
frm_middle.grid(row=0, column=1, padx=5, pady=(5,15))
frm_left.grid(row=0, column=0, padx=5, pady=5)

root.mainloop()
#####################################################################################################
#                                    END OF GUI                                                     #
####################################################################################################

