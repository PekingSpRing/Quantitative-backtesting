import tkinter as tk
from tkcalendar import Calendar

def on_date_select(event):
    selected_date = cal.selection_get()
    print("Selected date is:", selected_date)

root = tk.Tk()

cal = Calendar(root, selectmode='day')
cal.pack()

cal.bind("<<CalendarSelected>>", on_date_select)

root.mainloop()