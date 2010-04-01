from Tkinter import *

class Notebook:
   def __init__(self, root):
      self.active_fr = None
      self.count = 0
      self.choice = IntVar(0)

      # creates notebook's frames structure
      self.rb_fr = Frame(root, borderwidth=0, relief=RIDGE)
      self.rb_fr.grid(row=0,column=0,sticky=N)
      self.screen_fr = Frame(root, borderwidth=1, relief=RIDGE)
      self.screen_fr.grid(row=0,column=1)

      self.grid_opts={'ipadx':10,'ipady':10}
                
   # return a root frame reference for the external frames (screens)
   def __call__(self):
      return self.screen_fr
          
   # add a new frame (screen) to the (bottom/left of the) notebook
   def add_screen(self, fr, title):

      b = Radiobutton(self.rb_fr, text=title, indicatoron=0, \
            variable=self.choice, value=self.count, \
            command=lambda: self.display(fr))
      b.grid(row=self.count,sticky=W+E)

      # ensures the first frame will be
      # the first selected/enabled
      if not self.active_fr:
         fr.grid(row=0,column=1,**self.grid_opts)
         self.active_fr = fr
      self.count += 1

      # returns a reference to the newly created
      # radiobutton (allowing its configuration/destruction)         
      return b

   # hides the former active frame and shows 
   # another one, keeping its reference
   def display(self, fr):

      self.active_fr.grid_forget()
      fr.grid(row=0,column=1,columnspan=self.count,**self.grid_opts)
      self.active_fr = fr

