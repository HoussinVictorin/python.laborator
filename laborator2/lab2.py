import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, colorchooser
from tkinter import ttk

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Redactor Text OOP")
        self.root.geometry("800x600")

        # Creăm un Notebook pentru a adăuga taburi
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")

        # Creăm primul tab (fereastră de text)
        self.add_new_tab()

        # Creăm meniul
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # Meniul "Fișier"
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Fișier", menu=self.file_menu)
        self.file_menu.add_command(label="Deschide", command=self.open_file)
        self.file_menu.add_command(label="Salvează", command=self.save_file)
        self.file_menu.add_command(label="Salvează formatat", command=self.save_formatted_file)
        self.file_menu.add_command(label="Nou tab", command=self.add_new_tab)
        self.file_menu.add_command(label="Șterge tab", command=self.close_tab)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Ieșire", command=self.root.quit)

        # Meniul "Editare"
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Editare", menu=self.edit_menu)
        self.edit_menu.add_command(label="Căutare", command=self.search_text)
        self.edit_menu.add_command(label="Înlocuire", command=self.replace_text)  # Adăugat pentru Înlocuire
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Undo", command=self.undo)
        self.edit_menu.add_command(label="Redo", command=self.redo)

        # Meniul "Formatare"
        self.format_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Formatare", menu=self.format_menu)
        self.format_menu.add_command(label="Bold", command=self.toggle_bold)
        self.format_menu.add_command(label="Italic", command=self.toggle_italic)
        self.format_menu.add_command(label="Underline", command=self.toggle_underline)
        self.format_menu.add_command(label="Schimbă culoarea textului", command=self.show_color_selector)
        self.format_menu.add_command(label="Schimbă culoarea fundalului", command=self.show_background_color_selector)

        # Listă de fonturi
        self.font_list = tk.Listbox(self.root, height=6)
        self.font_list.pack(side="left", fill="y", padx=10)
        fonts = ["Arial", "Calibri", "Times New Roman", "Courier New", "Verdana"]
        for font in fonts:
            self.font_list.insert(tk.END, font)
        self.font_list.bind('<<ListboxSelect>>', self.change_font_from_list)

        # Listă de culori
        self.color_list = tk.Listbox(self.root, height=6)
        self.color_list.pack(side="left", fill="y", padx=10)
        colors = ["black", "red", "green", "blue", "purple"]
        for color in colors:
            self.color_list.insert(tk.END, color)
        self.color_list.bind('<<ListboxSelect>>', self.change_color_from_list)

        # ComboBox pentru mărimea fontului
        self.size_combobox = ttk.Combobox(self.root, values=["8", "10", "12", "14", "16", "18", "20", "24", "28"], state="readonly")
        self.size_combobox.set("12")  # Setăm mărimea implicită
        self.size_combobox.pack(side="left", padx=10)
        self.size_combobox.bind("<<ComboboxSelected>>", self.change_font_size)

    # Metodă pentru crearea unui nou tab
    def add_new_tab(self):
        text_area = tk.Text(self.notebook, wrap="word", font=("Arial", 12), undo=True)
        tab_id = self.notebook.add(text_area, text="Document Nou")
        self.notebook.select(tab_id)
        self.text_area = text_area

    # Metodă pentru ștergerea unui tab
    def close_tab(self):
        current_tab = self.notebook.select()
        if current_tab:
            confirm = messagebox.askyesno("Confirmare", "Sigur doriți să închideți acest tab?")
            if confirm:
                self.notebook.forget(current_tab)

    # Metodă pentru Undo
    def undo(self):
        try:
            self.text_area.edit_undo()
        except Exception as e:
            messagebox.showinfo("Undo", "Nu există acțiuni de undo.")

    # Metodă pentru Redo
    def redo(self):
        try:
            self.text_area.edit_redo()
        except Exception as e:
            messagebox.showinfo("Redo", "Nu există acțiuni de redo.")

    # Metodă pentru schimbarea fontului
    def change_font_from_list(self, event):
        selected_font = self.font_list.get(self.font_list.curselection())
        current_size = self.size_combobox.get()
        self.text_area.config(font=(selected_font, int(current_size)))

    # Metodă pentru schimbarea mărimii fontului
    def change_font_size(self, event):
        selected_size = self.size_combobox.get()
        current_font = self.text_area.cget("font").split()
        self.text_area.config(font=(current_font[0], int(selected_size)))

    # Metodă pentru schimbarea culorii textului
    def change_color_from_list(self, event):
        selected_color = self.color_list.get(self.color_list.curselection())
        self.change_text_color(selected_color)

    # Metodă pentru schimbarea culorii textului
    def change_text_color(self, color):
        selected_text = self.text_area.tag_ranges(tk.SEL)
        if selected_text:
            self.text_area.tag_add("highlight", selected_text[0], selected_text[1])
            self.text_area.tag_configure("highlight", foreground=color)
        else:
            self.text_area.config(fg=color)

    # Metodă pentru alegerea culorii textului
    def show_color_selector(self):
        color_code = colorchooser.askcolor(title="Selectează o culoare")[1]
        if color_code:
            self.change_text_color(color_code)

    # Metodă pentru schimbarea fundalului textului
    def change_background_color(self, color):
        selected_text = self.text_area.tag_ranges(tk.SEL)
        if selected_text:
            self.text_area.tag_add("bg_highlight", selected_text[0], selected_text[1])
            self.text_area.tag_configure("bg_highlight", background=color)
        else:
            self.text_area.config(bg=color)

    # Metodă pentru alegerea culorii fundalului
    def show_background_color_selector(self):
        color_code = colorchooser.askcolor(title="Selectează o culoare de fundal")[1]
        if color_code:
            self.change_background_color(color_code)

    # Metodă pentru aplicarea bold-ului
    def toggle_bold(self):
        selected_text = self.text_area.tag_ranges(tk.SEL)
        if selected_text:
            current_tags = self.text_area.tag_names(selected_text[0])
            if "bold" in current_tags:
                self.text_area.tag_remove("bold", selected_text[0], selected_text[1])
            else:
                self.text_area.tag_add("bold", selected_text[0], selected_text[1])
                current_font = self.text_area.cget("font").split()
                self.text_area.tag_configure("bold", font=(current_font[0], current_font[1], "bold"))
        else:
            current_font = self.text_area.cget("font").split()
            if "bold" not in current_font:
                self.text_area.config(font=(current_font[0], current_font[1], "bold"))
            else:
                self.text_area.config(font=(current_font[0], current_font[1]))

    # Metodă pentru aplicarea cursivului
    def toggle_italic(self):
        selected_text = self.text_area.tag_ranges(tk.SEL)
        if selected_text:
            current_tags = self.text_area.tag_names(selected_text[0])
            if "italic" in current_tags:
                self.text_area.tag_remove("italic", selected_text[0], selected_text[1])
            else:
                self.text_area.tag_add("italic", selected_text[0], selected_text[1])
                current_font = self.text_area.cget("font").split()
                self.text_area.tag_configure("italic", font=(current_font[0], current_font[1], "italic"))
        else:
            current_font = self.text_area.cget("font").split()
            if "italic" not in current_font:
                self.text_area.config(font=(current_font[0], current_font[1], "italic"))
            else:
                self.text_area.config(font=(current_font[0], current_font[1]))

    # Metodă pentru aplicarea subliniatului
    def toggle_underline(self):
        selected_text = self.text_area.tag_ranges(tk.SEL)
        if selected_text:
            current_tags = self.text_area.tag_names(selected_text[0])
            if "underline" in current_tags:
                self.text_area.tag_remove("underline", selected_text[0], selected_text[1])
            else:
                self.text_area.tag_add("underline", selected_text[0], selected_text[1])
                current_font = self.text_area.cget("font").split()
                self.text_area.tag_configure("underline", font=(current_font[0], current_font[1], "underline"))
        else:
            current_font = self.text_area.cget("font").split()
            if "underline" not in current_font:
                self.text_area.config(font=(current_font[0], current_font[1], "underline"))
            else:
                self.text_area.config(font=(current_font[0], current_font[1]))

    # Metodă pentru deschiderea unui fișier
    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, file.read())

    # Metodă pentru salvarea unui fișier
    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text_area.get(1.0, tk.END))

    # Metodă pentru salvarea fișierului formatat
    def save_formatted_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML Files", "*.html"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                content = self.text_area.get(1.0, tk.END)
                content = f"<html><body><pre>{content}</pre></body></html>"
                file.write(content)

    # Metodă pentru căutarea unui text
    def search_text(self):
        search_term = simpledialog.askstring("Căutare", "Introdu textul de căutare:")
        if search_term:
            start_pos = '1.0'
            while True:
                start_pos = self.text_area.search(search_term, start_pos, stopindex=tk.END)
                if not start_pos:
                    break
                end_pos = f"{start_pos}+{len(search_term)}c"
                self.text_area.tag_add("highlight", start_pos, end_pos)
                self.text_area.tag_configure("highlight", background="yellow")
                start_pos = end_pos

    # Metodă pentru înlocuirea unui text
    def replace_text(self):
        search_term = simpledialog.askstring("Înlocuire", "Introdu textul de căutare:")
        replace_term = simpledialog.askstring("Înlocuire", "Introdu textul de înlocuire:")
        if search_term and replace_term:
            content = self.text_area.get(1.0, tk.END)
            new_content = content.replace(search_term, replace_term)
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, new_content)

# Creăm fereastra principală
root = tk.Tk()
editor = TextEditor(root)
root.mainloop()
