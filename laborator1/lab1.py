import math
import tkinter as tk

a=['1','2','3','4','5','6','7','8','9','0']

class Calculator:
    def __init__(self):
        self.memory = None

    # Operații aritmetice de bază
    def calculate(self, expression):
        try:
            # Înlocuiește funcțiile textuale cu funcții Python
            expression = expression.replace('sin', 'self.sinus')
            expression = expression.replace('cos', 'self.cosinus')
            expression = expression.replace('tan', 'self.tangenta')
            expression = expression.replace('log(', 'self.logaritm(')
            expression = expression.replace('ln', 'self.logaritm_natural')
            expression = expression.replace('lg', 'self.logaritm')
            expression = expression.replace('rad(', 'self.radical(')  # Evaluare radical
            expression = expression.replace('%', '/100*')  # Evaluare procent

            # Evaluează expresia matematică
            return eval(expression)
        except Exception as e:
            return str(e)

    def adunare(self, a, b):
        return a + b

    def scadere(self, a, b):
        return a - b

    def inmultire(self, a, b):
        return a * b

    def impartire(self, a, b):
        if b == 0:
            raise ValueError("Impartire la zero!")
        return a / b

    def exponentiere(self, a, b):
        return a ** b

    def modulo(self, a, b):
        return a % b

    def radical(self, a):
        if a < 0:
            raise ValueError("Radical din numar negativ!!!")
        return math.sqrt(a)

    def sinus(self, a):
        return math.sin(math.radians(a))

    def cosinus(self, a):
        return math.cos(math.radians(a))

    def tangenta(self, a):
        return math.tan(math.radians(a))

    def logaritm_zecimal(self, a):
        return math.log10(a)
    
    def logaritm(self, a):
        return math.log2(a)

    def logaritm_natural(self, a):
        return math.log(a)


class CalculatorGui:
    def __init__(self, master):
        self.master = master
        self.master.title("Calculator")
        self.calculator = Calculator()
        self.expression = ""
        self.memory_value = None

        # Input
        self.entry = tk.Entry(master, width=25, font=('Arial', 25))
        self.entry.grid(row=0, column=0, columnspan=4)

        self.create_buttons()

    def create_buttons(self):
        # Butoane
        buttons = [
            '(', ')', 'bin','hex','=',
            'C', '1', '2', '3', '+', 
            'M', '4', '5', '6', '-', 
            'MR','7', '8', '9', '/', 
            'rad','sin', 'cos', 'tan', '*',
            'log', 'ln', 'lg', '.', '0',
            'MC','**',',','%', '<-',
        ]

        row_val = 1
        col_val = 0
        for button in buttons:
            action = lambda x=button: self.on_button_click(x)
            if button == 'C':  # Culoarea butonului 'C'
                tk.Button(self.master, text=button, command=action, width=9, height=1, font=('Arial', 16),
                          bg='red', fg='white').grid(row=row_val, column=col_val, sticky="nsew")
            elif button == '=':  # Culoarea butonului '='
                tk.Button(self.master, text=button, command=action, width=9, height=1, font=('Arial', 16),
                          bg='black', fg='white').grid(row=row_val, column=col_val, sticky="nsew")
            elif button == a:  # Culoarea butonului '='
                tk.Button(self.master, text=button, command=action, width=9, height=1, font=('Arial', 16),
                          bg='yelow', fg='black').grid(row=row_val, column=col_val, sticky="nsew")
            else:
                tk.Button(self.master, text=button, command=action, width=9, height=1, font=('Arial', 16)).grid(row=row_val, column=col_val, sticky="nsew")
            col_val += 1
            if col_val > 4:
                col_val = 0
                row_val += 1

        # Ajustează greutatea rândurilor și coloanelor pentru un design responsive
        for i in range(6):
            self.master.grid_columnconfigure(i, weight=1)
        for i in range(1, row_val + 1):
            self.master.grid_rowconfigure(i, weight=1)

    def on_button_click(self, char):
        if char == '=':
            try:
                result = self.calculator.calculate(self.expression)
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, str(result))
                self.expression = str(result)
                self.memory_value = result  # Memorizează rezultatul
            except Exception as e:
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, "Error")
                self.expression = ""
        elif char == 'C':
            self.entry.delete(0, tk.END)
            self.expression = ""

        elif char == 'M':
            if self.memory_value is not None:
                self.memory_value=self.expression
            else:
                self.memory_value = self.expression
        elif char == 'MR':
            if self.memory_value is not None:
                self.entry.insert(tk.END, str(self.memory_value))
                self.expression += str(self.memory_value)
            else:
                self.entry.insert(tk.END, "No value in memory")
        elif char == 'MC':
             if self.memory_value is not None:
                self.memory_value=0
        elif char in ['+', '-', '*', '/', '**', '%']:
            if self.expression and not self.expression.endswith((' ', '+', '-', '*', '/', '^', '%')):
                self.expression += ' ' + char + ' '
                self.entry.insert(tk.END, ' ' + char + ' ')
        elif char in '**':
            if self.expression and not self.expression.endswith('**'):
                self.expression += ' ' + char + ' '
                self.entry.insert(tk.END, ' ' + char + ' ')
        elif char in ['log', 'ln', 'lg']:
            if self.expression:
                self.expression += f'{char}('  # Adaugă paranteză pentru logaritmi
                self.entry.insert(tk.END, char + '(')
        elif char in ['sin', 'cos', 'tan']:
            if self.expression:
                self.expression += f'{char}('  # Adaugă paranteză pentru funcțiile trigonometrice
                self.entry.insert(tk.END, char + '(')
        elif char == 'rad':
            self.expression += 'rad('  # Adaugă 'rad(' în expresie
            self.entry.insert(tk.END, 'rad(')  # Afișează 'rad(' în câmpul de input
        elif char == ')':
            self.expression += ')'  # Permite închiderea parantezei
            self.entry.insert(tk.END, ')')  # Afișează ')' în câmpul de input
        elif char == '<-':  # Buton pentru a șterge ultima cifră
            self.expression = self.expression[:-1]  # Șterge ultima cifră din expresie
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, self.expression)  # Afișează expresia actualizată
        elif char in ['bin', 'hex']:
            try:
                num = float(self.entry.get())
                self.entry.delete(0, tk.END)
                if char == 'bin':
                    self.entry.insert(tk.END, bin(int(num))[2:])  # Transformare în binar
                elif char == 'hex':
                    self.entry.insert(tk.END, hex(int(num))[2:])  # Transformare în hexazecimal
            except ValueError:
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, "Error")
        else:
            self.expression += char
            self.entry.insert(tk.END, char)


if __name__ == "__main__":
    root = tk.Tk()
    gui = CalculatorGui(root)
    root.mainloop()
