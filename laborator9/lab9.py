import tkinter as tk
from tkinter import filedialog, colorchooser, ttk
from PIL import Image, ImageDraw, ImageTk


class MiniPaint:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini Paint Funcțional")
        self.root.attributes('-fullscreen', True)  # Pornire în modul ecran complet
        self.root.bind("<Escape>", self.exit_fullscreen)

        # Dimensiuni canvas
        self.canvas_width = self.root.winfo_screenwidth()
        self.canvas_height = self.root.winfo_screenheight() - 100  # Spațiu pentru toolbar

        # Variabile
        self.current_color = "black"
        self.bg_color = "white"
        self.brush_size = 5
        self.fill_color = "red"  # Culoarea pentru funcția de umplere
        self.curve_points = []  # Punctele pentru curba Bezier
        self.edit_mode = False  # Mod de editare a obiectelor existente
        self.selected_item = None  # Obiect selectat pentru modificare

        # Imaginea curentă
        self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), self.bg_color)
        self.draw = ImageDraw.Draw(self.image)

        # Configurare UI
        self.setup_toolbar()
        self.setup_color_bar()
        self.setup_canvas()

    def exit_fullscreen(self, event=None):
        """Ieșire din modul fullscreen."""
        self.root.attributes('-fullscreen', False)

    def setup_toolbar(self):
        """Configurarea barei de instrumente."""
        toolbar = tk.Frame(self.root, relief=tk.RAISED, bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Butoane
        tk.Button(toolbar, text="Salvează", command=self.save_image).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(toolbar, text="Deschide", command=self.open_image).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(toolbar, text="Clear", command=self.clear_canvas).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(toolbar, text="Imagine Nouă", command=self.new_image).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(toolbar, text="Alege Culoare", command=self.choose_fill_color).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(toolbar, text="Editează Obiect", command=self.toggle_edit_mode).pack(side=tk.LEFT, padx=5, pady=5)

        # Selectarea figurii
        self.shape = tk.StringVar(value="linie dreaptă")
        shapes = ["linie dreaptă", "linie curbată (Bezier)", "dreptunghi", "oval", "guma"]
        ttk.Combobox(toolbar, textvariable=self.shape, values=shapes, state="readonly").pack(side=tk.LEFT, padx=5, pady=5)

        # Dimensiunea pensulei
        self.brush_size_var = tk.IntVar(value=self.brush_size)
        ttk.Combobox(toolbar, textvariable=self.brush_size_var, values=list(range(1, 21)), state="readonly").pack(side=tk.LEFT, padx=5, pady=5)

    def setup_color_bar(self):
        """Configurarea barei de culori."""
        color_bar = tk.Frame(self.root, relief=tk.RAISED, bd=2)
        color_bar.pack(side=tk.TOP, fill=tk.X)

        tk.Button(color_bar, text="Culoare desen", command=self.choose_draw_color).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(color_bar, text="Culoare fundal", command=self.choose_bg_color).pack(side=tk.LEFT, padx=5, pady=5)

    def setup_canvas(self):
        """Configurarea canvas-ului."""
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg=self.bg_color)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Evenimente
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw_shape)
        self.canvas.bind("<ButtonRelease-1>", self.finish_draw)

    def new_image(self):
        """Creează o imagine nouă."""
        self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), self.bg_color)
        self.draw = ImageDraw.Draw(self.image)
        self.clear_canvas()

    def save_image(self):
        """Salvează imaginea curentă."""
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            self.image.save(file_path)

    def open_image(self):
        """Deschide o imagine existentă."""
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg"), ("All files", "*.*")])
        if file_path:
            self.image = Image.open(file_path).resize((self.canvas_width, self.canvas_height))
            self.draw = ImageDraw.Draw(self.image)
            self.update_canvas()

    def clear_canvas(self):
        """Curăță canvas-ul."""
        self.canvas.delete("all")
        self.image.paste(self.bg_color, [0, 0, self.canvas_width, self.canvas_height])
        self.update_canvas()

    def update_canvas(self):
        """Actualizează canvas-ul cu imaginea curentă."""
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def choose_draw_color(self):
        """Selectează culoarea de desen."""
        color = colorchooser.askcolor(color=self.current_color)[1]
        if color:
            self.current_color = color

    def choose_bg_color(self):
        """Selectează culoarea de fundal."""
        color = colorchooser.askcolor(color=self.bg_color)[1]
        if color:
            self.bg_color = color
            self.new_image()

    def choose_fill_color(self):
        """Alege culoarea pentru funcția de umplere."""
        color = colorchooser.askcolor(color=self.fill_color)[1]
        if color:
            self.fill_color = color

    def toggle_edit_mode(self):
        """Comută modul de editare."""
        self.edit_mode = not self.edit_mode
        self.canvas.config(cursor="hand2" if self.edit_mode else "arrow")

    def start_draw(self, event):
        """Începe desenarea."""
        if self.edit_mode:
            self.select_item(event.x, event.y)
            return

        self.start_x, self.start_y = event.x, event.y
        if self.shape.get() == "linie curbată (Bezier)":
            self.curve_points = [(self.start_x, self.start_y)]

    def draw_shape(self, event):
        """Desenează pe canvas."""
        if self.edit_mode:
            return

        x, y = event.x, event.y
        self.canvas.delete("preview")  # Șterge previzualizarea anterioară

        if self.shape.get() == "linie dreaptă":
            self.canvas.create_line(self.start_x, self.start_y, x, y, fill=self.current_color, width=self.brush_size_var.get(), tags="preview")
        elif self.shape.get() == "linie curbată (Bezier)":
            self.curve_points.append((x, y))
            self.canvas.create_line(self.curve_points, fill=self.current_color, width=self.brush_size_var.get(), tags="preview")
        elif self.shape.get() == "dreptunghi":
            self.canvas.create_rectangle(self.start_x, self.start_y, x, y, fill=self.fill_color, outline=self.current_color, tags="preview")
        elif self.shape.get() == "oval":
            self.canvas.create_oval(self.start_x, self.start_y, x, y, fill=self.fill_color, outline=self.current_color, tags="preview")
        elif self.shape.get() == "guma":
            self.canvas.create_rectangle(x - self.brush_size, y - self.brush_size, x + self.brush_size, y + self.brush_size, fill=self.bg_color, outline=self.bg_color)

    def finish_draw(self, event):
        """Finalizează desenul."""
        if self.edit_mode:
            return

        x, y = event.x, event.y
        if self.shape.get() == "linie dreaptă":
            self.draw.line([self.start_x, self.start_y, x, y], fill=self.current_color, width=self.brush_size_var.get())
        elif self.shape.get() == "linie curbată (Bezier)":
            self.curve_points.append((x, y))
            self.draw.line(self.curve_points, fill=self.current_color, width=self.brush_size_var.get())
        elif self.shape.get() == "dreptunghi":
            self.draw.rectangle([self.start_x, self.start_y, x, y], fill=self.fill_color, outline=self.current_color)
        elif self.shape.get() == "oval":
            self.draw.ellipse([self.start_x, self.start_y, x, y], fill=self.fill_color, outline=self.current_color)
        self.update_canvas()

    def select_item(self, x, y):
        """Selectează un obiect existent pentru modificare."""
        closest = self.canvas.find_closest(x, y)
        self.selected_item = closest[0] if closest else None
        if self.selected_item:
            self.canvas.itemconfig(self.selected_item, outline="blue")  # Evidențiază obiectul


if __name__ == "__main__":
    root = tk.Tk()
    app = MiniPaint(root)
    root.mainloop()