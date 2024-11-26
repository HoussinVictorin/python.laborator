import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, colorchooser
from tkinter import ttk

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Redactor Text OOP")
        self.root.geometry("800x600")

        # Create a Notebook to add tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")

        # Create the first tab (text area)
        self.add_new_tab()

        # Create the menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # "File" menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Fișier", menu=self.file_menu)
        self.file_menu.add_command(label="Deschide", command=self.open_file)
        self.file_menu.add_command(label="Salvează", command=self.save_file)
        self.file_menu.add_command(label="Salvează formatat", command=self.save_formatted_file)
        self.file_menu.add_command(label="Nou tab", command=self.add_new_tab)
        self.file_menu.add_command(label="Șterge tab", command=self.close_tab)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Ieșire", command=self.root.quit)

        # "Edit" menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Editare", menu=self.edit_menu)
        self.edit_menu.add_command(label="Căutare", command=self.search_text)
        self.edit_menu.add_command(label="Înlocuire", command=self.replace_text)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Undo", command=self.undo)
        self.edit_menu.add_command(label="Redo", command=self.redo)

        # "Format" menu
        self.format_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Formatare", menu=self.format_menu)
        self.format_menu.add_command(label="Bold", command=self.toggle_bold)
        self.format_menu.add_command(label="Italic", command=self.toggle_italic)
        self.format_menu.add_command(label="Underline", command=self.toggle_underline)
        self.format_menu.add_command(label="Schimbă culoarea textului", command=self.show_color_selector)
        self.format_menu.add_command(label="Schimbă culoarea fundalului", command=self.show_background_color_selector)

        # Font list
        self.font_list = tk.Listbox(self.root, height=6)
        self.font_list.pack(side="left", fill="y", padx=10)
        fonts = ["Arial", "Calibri", "Times New Roman", "Courier New", "Verdana"]
        for font in fonts:
            self.font_list.insert(tk.END, font)
        self.font_list.bind('<<ListboxSelect>>', self.change_font_from_list)

        # Color list
        self.color_list = tk.Listbox(self.root, height=6)
        self.color_list.pack(side="left", fill="y", padx=10)
        colors = ["black", "red", "green", "blue", "purple"]
        for color in colors:
            self.color_list.insert(tk.END, color)
        self.color_list.bind('<<ListboxSelect>>', self.change_color_from_list)

        # ComboBox for font size
        self.size_combobox = ttk.Combobox(self.root, values=["8", "10", "12", "14", "16", "18", "20", "24", "28"], state="readonly")
        self.size_combobox.set("12")  # Set the default font size
        self.size_combobox.pack(side="left", padx=10)
        self.size_combobox.bind("<<ComboboxSelected>>", self.change_font_size)

    # Method for creating a new tab
    def add_new_tab(self):
        text_area = tk.Text(self.notebook, wrap="word", font=("Arial", 12), undo=True)
        tab_id = self.notebook.add(text_area, text="Document Nou")
        self.notebook.select(tab_id)
        self.text_area = text_area

    # Method to close a tab
    def close_tab(self):
        current_tab = self.notebook.select()
        if current_tab:
            confirm = messagebox.askyesno("Confirmare", "Sigur doriți să închideți acest tab?")
            if confirm:
                self.notebook.forget(current_tab)

    # Method for Undo
    def undo(self):
        try:
            self.text_area.edit_undo()
        except Exception as e:
            messagebox.showinfo("Undo", "Nu există acțiuni de undo.")

    # Method for Redo
    def redo(self):
        try:
            self.text_area.edit_redo()
        except Exception as e:
            messagebox.showinfo("Redo", "Nu există acțiuni de redo.")

    # Method for changing font from the font list
    def change_font_from_list(self, event):
        selected_font = self.font_list.get(self.font_list.curselection())
        current_size = self.size_combobox.get()
        self.text_area.config(font=(selected_font, int(current_size)))

    # Method for changing font size
    def change_font_size(self, event):
        selected_size = self.size_combobox.get()
        current_font = self.text_area.cget("font").split()
        self.text_area.config(font=(current_font[0], int(selected_size)))

    # Method for changing the text color
    def change_color_from_list(self, event):
        selected_color = self.color_list.get(self.color_list.curselection())
        self.change_text_color(selected_color)

    # Method for changing text color
    def change_text_color(self, color):
        selected_text = self.text_area.tag_ranges(tk.SEL)
        if selected_text:
            self.text_area.tag_add("highlight", selected_text[0], selected_text[1])
            self.text_area.tag_configure("highlight", foreground=color)
        else:
            self.text_area.config(fg=color)

    # Method to open the color picker for text
    def show_color_selector(self):
        color_code = colorchooser.askcolor(title="Selectează o culoare")[1]
        if color_code:
            self.change_text_color(color_code)

    # Method for changing the background color of the text
    def change_background_color(self, color):
        selected_text = self.text_area.tag_ranges(tk.SEL)
        if selected_text:
            self.text_area.tag_add("bg_highlight", selected_text[0], selected_text[1])
            self.text_area.tag_configure("bg_highlight", background=color)
        else:
            self.text_area.config(bg=color)

    # Method to open the background color picker
    def show_background_color_selector(self):
        color_code = colorchooser.askcolor(title="Selectează o culoare de fundal")[1]
        if color_code:
            self.change_background_color(color_code)

    # Method for bold text
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

    # Method for italic text
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

    # Method for underline text
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

    # Method to open a file and load content into the text area
    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".doc", filetypes=[("Text Files", "*.doc"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                self.text_area.delete(1.0, tk.END)  # Clear existing content
                self.text_area.insert(tk.END, file.read())  # Insert file content

    # Method to save the current content as a plain text file
    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".doc", filetypes=[("Text Files", "*.doc"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text_area.get(1.0, tk.END))

    # Method to save the content as an HTML formatted file
    def save_formatted_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML Files", "*.html"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                content = self.text_area.get(1.0, tk.END)
                content = f"<html><body><pre>{content}</pre></body></html>"
                file.write(content)

    # Method to search for text
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

    # Method for replacing text
    def replace_text(self):
        search_term = simpledialog.askstring("Înlocuire", "Introdu textul de căutare:")
        if not search_term:
            return
        
        replace_term = simpledialog.askstring("Înlocuire", "Introdu textul de înlocuire:")
        if not replace_term:
            return

        replace_all = messagebox.askyesno("Înlocuire", "Doriți să înlocuiți toate instanțele?")
        
        if replace_all:
            content = self.text_area.get(1.0, tk.END)
            new_content = content.replace(search_term, replace_term)
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, new_content)
        else:
            start_pos = '1.0'
            while True:
                start_pos = self.text_area.search(search_term, start_pos, stopindex=tk.END)
                if not start_pos:
                    break
                end_pos = f"{start_pos}+{len(search_term)}c"
                self.text_area.tag_add("highlight", start_pos, end_pos)
                self.text_area.tag_configure("highlight", background="yellow")
                replace_choice = messagebox.askyesno("Înlocuire", f"Doriți să înlocuiți acest cuvânt: '{search_term}'?")
                if replace_choice:
                    self.text_area.delete(start_pos, end_pos)
                    self.text_area.insert(start_pos, replace_term)
                start_pos = f"{start_pos}+1c"  # Continue searching after the current match


# Create the main window and run the editor
if __name__ == "__main__":
    root = tk.Tk()
    editor = TextEditor(root)
    root.mainloop()
