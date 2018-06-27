import Problema
import tkinter as tk
import tkinter

from tkinter import ttk
from tkinter import *

win = tk.Tk()
win.title("Algoritmo Genético por Paso de Enfriamiento -Jesus-Y-Sergio-")
win.resizable(0, 0)

filename_label = ttk.Label(win, text="Localización del fichero")
filename_label.grid(column=0, row=0)

filename = tk.StringVar()
filename_entry = ttk.Entry(win, width=40, textvariable=filename)
filename_entry.grid(column=1, row=0)
filename_entry.focus()

times_run_label = ttk.Label(win, text="Número de ejecuciones")
times_run_label.grid(column=0, row=2)
times_run = tk.IntVar()
times_run_entry = ttk.Entry(win, width=10, textvariable=times_run)
times_run_entry.grid(column=1, row=2)


def run_stats():
    win = tk.Tk()
    win.title("Algoritmo Genético por Paso de Enfriamiento -Jesus-Y-Sergio-")
    win.resizable(0, 0)
    text_label = ttk.Label(win, text="Resultados")
    text_label.grid(column=0, row=0)
    text_results = tk.Text(win, width=100, height=15)
    text_results.grid(column=0, row=1)
    progressbar = ttk.Progressbar(orient=tk.HORIZONTAL)
    progressbar.grid(row=3, column=2)
    win.mainloop()


def parametros():
    path = filename.get()
    params = times_run.get()
    return path, params


def ejecutar():
    text_label = ttk.Label(win, text="Resultados")
    text_label.grid(column=0, row=0)
    progressbar = ttk.Progressbar(orient=tk.HORIZONTAL)
    progressbar.grid(row=3, column=2)
    progressbar.step(50)
    win.update()
    ejecutar2()
    win.update()


def ejecutar2():
    path, params = parametros()
    problema = Problema.Problema(path, params)
    colores = problema.ejecutarAlgoritmo()
    text_result = Text(win)
    v = 0
    final = colores.__len__
    for c in colores:
        text_result.insert(END, "Vertice")
        text_result.insert(END, v)
        text_result.insert(END, ": ")
        text_result.insert(END, c)
        text_result.insert(END, " \n")
        v = v + 1

    text_result.grid(column=1, row=40)
    progressbar = ttk.Progressbar(orient=tk.HORIZONTAL)
    progressbar.grid(row=3, column=2)
    progressbar.step(99.9)
    win.update()
    win.mainloop()


stats_button = ttk.Button(win, text="EJECUTAR", command=ejecutar)
stats_button.grid(column=2, row=8)

win.mainloop()
