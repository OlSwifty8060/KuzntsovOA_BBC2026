import tkinter as tk
from tkinter import ttk, messagebox

balance = 0.0  # текущий баланс


def update_balance():
    """Обновляет надпись с балансом"""
    balance_label.config(text=f"Баланс: {balance:.2f} {currency.get()}")


def do_operation():
    """Обработка кнопки «Выполнить»"""
    global balance

    #  проверка данных 
    name = owner.get().strip()
    if name == "":
        messagebox.showerror("Ошибка", "Введите имя клиента")
        return

    try:
        value = float(amount.get().replace(",", "."))
    except ValueError:
        messagebox.showerror("Ошибка", "Сумма должна быть числом")
        return

    if value <= 0:
        messagebox.showerror("Ошибка", "Сумма должна быть больше нуля")
        return

    op = operation.get()
    if op == "withdraw" and value > balance:
        messagebox.showerror("Ошибка", "Недостаточно средств")
        return

    #  диалоговое окно подтверждения 
    if confirm.get():
        text = "Пополнить" if op == "deposit" else "Снять"
        if not messagebox.askyesno("Подтверждение", f"{text} {value:.2f}?"):
            return

    #  сама операция 
    if op == "deposit":
        balance += value
        history.insert(tk.END, f"{name}: +{value:.2f}\n")
    else:
        balance -= value
        history.insert(tk.END, f"{name}: -{value:.2f}\n")

    update_balance()
    amount.delete(0, tk.END)


def clear_history():
    history.delete("1.0", tk.END)


def exit_app():
    if messagebox.askyesno("Выход", "Закрыть программу?"):
        root.destroy()


#  главное окно 
root = tk.Tk()
root.title("Еще один банк")
root.geometry("380x430")

#  текстовые элементы и поля ввода 
tk.Label(root, text="Имя клиента:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
owner = tk.Entry(root)
owner.grid(row=0, column=1, columnspan=2, padx=10, pady=5, sticky="we")

tk.Label(root, text="Сумма:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
amount = tk.Entry(root)
amount.grid(row=1, column=1, columnspan=2, padx=10, pady=5, sticky="we")

#  выбор параметров 
operation = tk.StringVar(value="deposit")
tk.Radiobutton(root, text="Пополнить", variable=operation, value="deposit").grid(row=2, column=0, padx=10, sticky="w")
tk.Radiobutton(root, text="Снять", variable=operation, value="withdraw").grid(row=2, column=1, sticky="w")

tk.Label(root, text="Валюта:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
currency = ttk.Combobox(root, values=["₽", "$", "€"], state="readonly", width=5)
currency.current(0)
currency.grid(row=3, column=1, sticky="w")
currency.bind("<<ComboboxSelected>>", lambda event: update_balance())  # выбор

confirm = tk.BooleanVar(value=True)
tk.Checkbutton(root, text="Спрашивать подтверждение", variable=confirm).grid(
    row=4, column=0, columnspan=3, padx=10, sticky="w")

# кнопочки
tk.Button(root, text="Выполнить", command=do_operation).grid(row=5, column=0, padx=10, pady=10, sticky="we")
tk.Button(root, text="Очистить", command=clear_history).grid(row=5, column=1, pady=10, sticky="we")
tk.Button(root, text="Выход", command=exit_app).grid(row=5, column=2, padx=10, pady=10, sticky="we")

#  вывод результатов 
balance_label = tk.Label(root, text="", font=("Arial", 14, "bold"))
balance_label.grid(row=6, column=0, columnspan=3, pady=5)

tk.Label(root, text="История операций:").grid(row=7, column=0, columnspan=3, padx=10, sticky="w")
history = tk.Text(root, height=8)
history.grid(row=8, column=0, columnspan=3, padx=10, pady=5, sticky="we")

root.columnconfigure(1, weight=1)
update_balance()
root.mainloop()