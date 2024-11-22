import tkinter as tk
from tkinter import filedialog, messagebox


class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Redactor Text OOP")
        self.root.geometry("600x400")

        # Creare zonă de text
        self.text_area = tk.Text(self.root, wrap="word")
        self.text_area.pack(expand=True, fill="both")

        # Creare meniu
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # Meniul "Fișier"
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Fișier", menu=self.file_menu)
        self.file_menu.add_command(label="Deschide", command=self.open_file)
        self.file_menu.add_command(label="Salvează", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Ieșire", command=self.root.quit)

    # Metodă pentru a deschide un fișier
    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, "r") as file:
                    content = file.read()
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(tk.END, content)
                self.root.title(f"Redactor Text OOP - {file_path}")
            except Exception as e:
                messagebox.showerror("Eroare", f"A apărut o eroare la deschiderea fișierului: {e}")

    # Metodă pentru a salva un fișier
    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, "w") as file:
                    file.write(self.text_area.get(1.0, tk.END))
                messagebox.showinfo("Succes", "Fișier salvat cu succes!")
            except Exception as e:
                messagebox.showerror("Eroare", f"A apărut o eroare la salvarea fișierului: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    editor = TextEditor(root)
    root.mainloop()
