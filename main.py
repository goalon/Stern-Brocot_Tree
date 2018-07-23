from tkinter import *

root = Tk()

root.title("Stern-Brocot tree")

w = 1366
h = 768

canvas = Canvas(root, width=w, height=h)

canvas.create_text(10, 10, text="0", underline=0)
canvas.create_text(10, 22, text="1")
canvas.create_text(w/2, 10, text="1", underline=0)
canvas.create_text(w/2, 22, text="1")
canvas.create_text(w - 10, 10, text="1", underline=0)
canvas.create_text(w - 10, 22, text="0")


def construct(x, y, length, depth, middle, left, right):
    if depth > 0:
        canvas.create_line(x, y, x - length, y + 75)
        l = (middle[0] + left[0], middle[1] + left[1])
        canvas.create_text(x - length, y + 85, text=l[0], underline=0)
        canvas.create_text(x - length, y + 97, text=l[1])
        construct(x - length, y + 105, length / 2, depth - 1, l, left, middle)
        canvas.create_line(x, y, x + length, y + 75)
        r = (middle[0] + right[0], middle[1] + right[1])
        canvas.create_text(x + length, y + 85, text=r[0], underline=0)
        canvas.create_text(x + length, y + 97, text=r[1])
        construct(x + length, y + 105, length / 2, depth - 1, r, middle, right)


construct(w/2, 30, w/4, 6, (1, 1), (0, 1), (1, 0))

marks = []


def find(stats, n, x, y, length, depth, middle, left, right):
    if depth >= 0:
        marks.append(canvas.create_rectangle(x - 10, y - 28, x + 8, y - 2))
    if n[0] * middle[1] < n[1] * middle[0]:
        stats.insert(170, 'L')
        l = (middle[0] + left[0], middle[1] + left[1])
        find(stats, n, x - length, y + 105, length / 2, depth - 1, l, left, middle)
    elif n[0] * middle[1] > n[1] * middle[0]:
        stats.insert(170, 'P')
        r = (middle[0] + right[0], middle[1] + right[1])
        find(stats, n, x + length, y + 105, length / 2, depth - 1, r, middle, right)


def generate(stats, n, x, y, length, depth, middle, left, right):
    l = (middle[0] + left[0], middle[1] + left[1])
    if n >= l[1]:
        generate(stats, n, x - length, y + 105, length / 2, depth - 1, l, left, middle)
    stats.insert(170, str(middle[0]) + '/' + str(middle[1]) + ' ')
    if depth >= 0:
        marks.append(canvas.create_rectangle(x - 10, y - 28, x + 8, y - 2))
    r = (middle[0] + right[0], middle[1] + right[1])
    if n >= r[1]:
        generate(stats, n, x + length, y + 105, length / 2, depth - 1, r, middle, right)


frameStatus = Frame(root)
frameStatus.pack(side=BOTTOM)

status = Entry(frameStatus, bd=1, width=170)
status.pack(side=BOTTOM)

frameButton = Frame(root)
frameButton.pack(side=BOTTOM)

entry = Entry(frameButton, bd=1, width=145)
entry.pack(side=RIGHT)


def clear_path():
    status.delete(0, 170)
    while marks:
        canvas.delete(marks.pop())


def clear(event):
    entry.delete(0, 145)
    clear_path()


def show_path(event):
    clear_path()
    number = entry.get().split('/')
    denominator = int(number.pop())
    numerator = int(number.pop())
    find(status, (numerator, denominator), w / 2, 30, w / 4, 6, (1, 1), (0, 1), (1, 0))


def show_generated(event):
    clear_path()
    number = int(entry.get())
    status.insert(170, '0/1 ')
    generate(status, number, w / 2 - w / 4, 135, w / 8, 5, (1, 2), (0, 1), (1, 1))
    status.insert(170, '1/1 ')


buttonFind = Button(frameButton, text="Szukaj", bg="green")
buttonFind.bind("<Button-1>", show_path)
buttonFind.pack(side=RIGHT)

buttonGenerate = Button(frameButton, text="Generuj", bg="blue")
buttonGenerate.bind("<Button-1>", show_generated)
buttonGenerate.pack(side=RIGHT)

buttonClear = Button(frameButton, text="Czyść", bg="red")
buttonClear.bind("<Button-1>", clear)
buttonClear.pack(side=RIGHT)

canvas.pack()

root.mainloop()
