import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os

matrix = None
N = 19

def choose_file():
    """Обробка натискання кнопки 'Обрати' — вибір файлу + перевірка + запуск аналізу"""
    result_text.delete("1.0", tk.END)
    global matrix

    filepath = filedialog.askopenfilename(
        title="Оберіть текстовий файл з матрицею",
        filetypes=[("Текстові файли", "*.txt"), ("Усі файли", "*.*")]
    )
    if not filepath:
        return

    entry_path.delete(0, tk.END)
    entry_path.insert(0, filepath)

    if not read_matrix():
        return

    if len(matrix) != N or not all(len(row) == N for row in matrix):
        result_text.insert(tk.END, "Матриця не правильного розміру.\nНеобхідний розмір точно 19×19.")
        matrix = None 
        return

    check()
    


def read_matrix():
    global matrix
    filepath = entry_path.get().strip()

    if not filepath or not os.path.isfile(filepath):
        messagebox.showwarning("Помилка", "Оберіть існуючий файл")
        return False

    temp = []

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                try:
                    row = [int(x) for x in line.split() if x.strip()]
                    if row:
                        temp.append(row)
                except ValueError:
                    messagebox.showerror(
                        "Помилка формату",
                        f"Не число в рядку {line_num}:\n{line.strip()}\n\n"
                        "Усі значення мають бути цілими числами."
                    )
                    return False

        if not temp:
            messagebox.showwarning("Попередження", "У файлі немає валідних рядків з числами")
            return False

        matrix = temp
        return True

    except Exception as e:
        messagebox.showerror("Помилка читання файлу", f"{type(e).__name__}: {e}")
        return False


def check():
    global matrix
    result_text.delete("1.0", tk.END)

    n = len(matrix)

    directions = [
        (0, 1),
        (1, 0),
        (1, 1),
        (1, -1)
    ]

    players = [1,2]
    
    for i in range(n):
        for j in range(n):
            if matrix[i][j] not in players:
                continue

            win = matrix[i][j]

            for di, dj in directions:
                count = 1
                ni, nj = i + di, j + dj

                while 0 <= ni < n and 0 <= nj < n and matrix[ni][nj] == win:
                    count += 1
                    ni += di
                    nj += dj

                if count == 5:
                    prev_i = i - di
                    prev_j = j - dj

                    if 0 <= prev_i < n and 0 <= prev_j < n and matrix[prev_i][prev_j] == win:
                        continue

                    if 0 <= ni < n and 0 <= nj < n and matrix[ni][nj] == win:
                        continue

                    result_text.insert(
                        tk.END,
                        f"Переміг: {win}\n   З координатою ({i + 1}; {j + 1})"
                    )
                    return

    result_text.insert(tk.END, "Переможця немає")

    

root = tk.Tk()
root.geometry("640x520")

tk.Label(root, text="Файл:").pack(pady=(15,4), anchor="w", padx=15)

frame = tk.Frame(root)
frame.pack(fill="x", padx=15)

entry_path = tk.Entry(frame, width=60)
entry_path.pack(side="left", fill="x", expand=True, padx=(0,8))

tk.Button(frame, text="Обрати", width=12, command=choose_file).pack(side="right")

result_text = scrolledtext.ScrolledText(root, height=10, width=70, font=("Consolas", 10))
result_text.pack(padx=15, pady=(4,15), fill="both", expand=True)

root.mainloop()