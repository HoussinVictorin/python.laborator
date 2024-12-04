import tkinter as tk
from tkinter import colorchooser, filedialog
from tkinter import messagebox

class RedactorGrafic:
    def __init__(self, root):
        self.root = root
        self.root.title("Redactor Grafic")
        
        # Initializare canvas pentru desen
        self.canvas = tk.Canvas(root, width=800, height=600, bg="white")
        self.canvas.pack(side=tk.TOP, padx=10, pady=10)

        # Variabile de culoare
        self.bg_color = "white"
        self.fg_color = "black"

        # Variabila pentru instrumentul curent
        self.current_tool = "linie"

        # Crearea barei de instrumente
        self.create_toolbar()

    def create_toolbar(self):
        toolbar = tk.Frame(self.root)
        toolbar.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Butoane pentru instrumente
        self.rect_btn = tk.Button(toolbar, text="Dreptunghi", command=self.select_rectangle)
        self.rect_btn.pack(fill=tk.X)
        
        self.oval_btn = tk.Button(toolbar, text="Oval", command=self.select_oval)
        self.oval_btn.pack(fill=tk.X)

        self.line_btn = tk.Button(toolbar, text="Linie", command=self.select_line)
        self.line_btn.pack(fill=tk.X)
        
        self.clear_btn = tk.Button(toolbar, text="Sterge", command=self.clear_canvas)
        self.clear_btn.pack(fill=tk.X)
        
        self.save_btn = tk.Button(toolbar, text="Salveaza", command=self.save_image)
        self.save_btn.pack(fill=tk.X)
        
        self.load_btn = tk.Button(toolbar, text="Deschide", command=self.load_image)
        self.load_btn.pack(fill=tk.X)

        # Butoane pentru selectarea culorii
        self.color_btn = tk.Button(toolbar, text="Alege Culoare", command=self.choose_color)
        self.color_btn.pack(fill=tk.X)
        
        # Bara de culori
        color_toolbar = tk.Frame(self.root)
        color_toolbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.bg_color_btn = tk.Button(color_toolbar, text="Culoare fundal", command=self.choose_bg_color)
        self.bg_color_btn.pack(side=tk.LEFT, padx=5)

    def choose_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.fg_color = color

    def choose_bg_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.bg_color = color
            self.canvas.config(bg=self.bg_color)

    def select_rectangle(self):
        self.current_tool = "dreptunghi"

    def select_oval(self):
        self.current_tool = "oval"

    def select_line(self):
        self.current_tool = "linie"

    def clear_canvas(self):
        self.canvas.delete("all")

    def save_image(self):
        messagebox.showinfo("Salvare", "Nu este.")

    def load_image(self):
        messagebox.showinfo("Deschidere", "nu este.")

    def draw_shape(self, event):
        if self.current_tool == "linie":
            # Desenează o linie continuă pe măsură ce se mișcă mouse-ul
            self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill=self.fg_color)
            # Colorează fundalul (pixelii pe unde trece linia)
            self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline=self.fg_color, fill=self.fg_color)
            self.start_x = event.x
            self.start_y = event.y
        elif self.current_tool == "dreptunghi":
            # Desenează un dreptunghi pe măsură ce utilizatorul trage mouse-ul
            self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline=self.fg_color)
        elif self.current_tool == "oval":
            # Desenează un oval pe măsură ce utilizatorul trage mouse-ul
            self.canvas.create_oval(self.start_x, self.start_y, event.x, event.y, outline=self.fg_color)

    def start_draw(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.current_tool == "linie":
            self.canvas.bind("<B1-Motion>", self.draw_shape)
        elif self.current_tool in ["dreptunghi", "oval"]:
            self.canvas.bind("<B1-Motion>", self.draw_shape)

    def stop_draw(self, event):
        self.canvas.unbind("<B1-Motion>")

if __name__ == "__main__":
    root = tk.Tk()
    app = RedactorGrafic(root)

    app.canvas.bind("<ButtonPress-1>", app.start_draw)
    app.canvas.bind("<ButtonRelease-1>", app.stop_draw)

    root.mainloop()
