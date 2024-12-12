
import tkinter as tk
from tkinter import ttk, messagebox
import webview


class InternetBrowser:
    def __init__(self, root):
        self.root = root
        self.root.title("Browser de Internet OOP")
        self.root.geometry("1200x800")  # Ajustăm dimensiunea ferestrei

        # Bara de navigare
        self.toolbar = tk.Frame(self.root)
        self.toolbar.pack(side="top", fill="x")

        self.back_button = tk.Button(self.toolbar, text="Back", command=self.go_back)
        self.back_button.pack(side="left", padx=5, pady=5)

        self.forward_button = tk.Button(self.toolbar, text="Forward", command=self.go_forward)
        self.forward_button.pack(side="left", padx=5, pady=5)

        self.refresh_button = tk.Button(self.toolbar, text="Refresh", command=self.refresh_page)
        self.refresh_button.pack(side="left", padx=5, pady=5)

        self.url_entry = tk.Entry(self.toolbar, width=70)
        self.url_entry.pack(side="left", padx=5, pady=5, fill="x", expand=True)
        self.url_entry.bind("<Return>", self.navigate_to_url)

        self.search_button = tk.Button(self.toolbar, text="Go", command=self.navigate_to_url)
        self.search_button.pack(side="left", padx=5, pady=5)

        self.new_tab_button = tk.Button(self.toolbar, text="New Tab", command=self.add_new_tab)
        self.new_tab_button.pack(side="left", padx=5, pady=5)

        self.favorites_button = tk.Button(self.toolbar, text="Add to Favorites", command=self.add_to_favorites)
        self.favorites_button.pack(side="left", padx=5, pady=5)

        self.history_button = tk.Button(self.toolbar, text="History", command=self.show_history)
        self.history_button.pack(side="left", padx=5, pady=5)

        # Crearea unei notebook pentru taburi sub bara de navigare
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")

        # Crearea unui tab nou
        self.add_new_tab()

        # Date interne
        self.history = []
        self.favorites = []
        self.back_stack = []
        self.forward_stack = []

    def add_new_tab(self):
        frame = tk.Frame(self.notebook)
        self.notebook.add(frame, text="New Tab")
        self.notebook.select(frame)
        tk.Label(frame, text="Introdu o adresă URL sau caută ceva.", font=("Arial", 16)).pack(expand=True, fill="both")

        # Adăugăm un widget PyWebView
        webview_window = webview.create_window('Browser Tab', 'about:blank')
        webview.start()

    def close_current_tab(self):
        current_tab = self.notebook.select()
        if current_tab:
            confirm = messagebox.askyesno("Confirmare", "Sigur doriți să închideți acest tab?")
            if confirm:
                self.notebook.forget(current_tab)

    def navigate_to_url(self, event=None):
        url = self.url_entry.get()
        if url.lower() in ["youtube", "you tube"]:
            url = "https://www.youtube.com"
        elif not url.startswith("http"):
            url = f"https://yandex.com/search/?text={url}"
        self.update_stacks(url)
        webview_window = webview.create_window('Browser Tab', url)
        webview.start()

    def update_stacks(self, url):
        if self.history:
            self.back_stack.append(self.history[-1])
        self.history.append(url)
        self.forward_stack.clear()

    def refresh_page(self):
        webview_window = webview.create_window('Browser Tab', self.history[-1])
        webview.start()

    def go_back(self):
        if self.back_stack:
            url = self.back_stack.pop()
            self.history.append(url)
            webview_window = webview.create_window('Browser Tab', url)
            webview.start()

    def go_forward(self):
        if self.forward_stack:
            url = self.forward_stack.pop()
            self.history.append(url)
            webview_window = webview.create_window('Browser Tab', url)
            webview.start()

    def add_to_favorites(self):
        if self.history:
            current_url = self.history[-1]
            if current_url not in self.favorites:
                self.favorites.append(current_url)
                messagebox.showinfo("Favorites", f"Adăugat la favorite: {current_url}")
            else:
                messagebox.showinfo("Favorites", "URL-ul este deja în favorite.")

    def show_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title("Istoric")
        history_window.geometry("400x300")

        history_list = tk.Listbox(history_window)
        history_list.pack(fill="both", expand=True)

        for url in self.history:
            history_list.insert(tk.END, url)

        tk.Button(history_window, text="Închide", command=history_window.destroy).pack()


if __name__ == "__main__":
    root = tk.Tk()
    browser = InternetBrowser(root)
    root.mainloop()
