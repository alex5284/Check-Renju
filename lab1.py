import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os

matrix = None

def choose_file():
    result_text.delete("1.0", tk.END)
    global matrix 

    filepath = filedialog.askopenfilename(
        title="Выберите текстовый файл с матрицей",
        filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
    )
    if not filepath:
        return

    entry_path.delete(0, tk.END)
    entry_path.insert(0, filepath)
    read_matrix()
    is_matrix_corect = True
    if len(matrix) != 19: is_matrix_corect = False

    for i in range(len(matrix)):
        if len(matrix[i]) != 19: 
            is_matrix_corect = False
            break
    
    if is_matrix_corect == True: check()
    else: result_text.insert(tk.END, "Матриця не правильного розміру. Необхідний розмір 19х19.")
    


def read_matrix():
    global matrix
    
    filepath = entry_path.get().strip()
    if not filepath or not os.path.isfile(filepath):
        messagebox.showwarning("Ошибка", "Выберите файл")
        return

    try:
        matrix = []
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                row = [int(x) for x in line.split() if x]
                if row:
                    matrix.append(row)

        if not matrix:
            messagebox.showwarning("Предупреждение", "В файле нет чисел")
            return

    except Exception as e:
        messagebox.showerror("Ошибка", str(e))


def check():
    global matrix
    result_text.delete("1.0", tk.END)

    n = len(matrix)

    directions = [
        (0, 1),
        (1, 0),
        (1, 1),
        (-1, 1)
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