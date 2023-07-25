import tkinter as tk

root = tk.Tk()

test = tk.Label(root, text="Red", bg="red", fg="white")
test.pack(side=tk.BOTTOM)
test = tk.Label(root, text="Green", bg="green", fg="white")
test.pack(side=tk.BOTTOM)
test = tk.Label(root, text="purple", bg="purple", fg="white")
test.pack(padx=15, pady=20, side=tk.LEFT)

root.mainloop()