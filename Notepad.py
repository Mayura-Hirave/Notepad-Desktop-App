import tkinter
import tkinter.messagebox  # Access to standard Tk dialog boxes.
# https://docs.python.org/3/library/tkinter.messagebox.html

import tkinter.filedialog
import tkinter.messagebox
import sys
import os


class Notepad:
    def __init__(self):
        self.__main_window = tkinter.Tk()
        self.__main_window.title("Untitled - Notepad")
        self.__main_window.geometry("600x300")
        self.__main_window.minsize(600, 300)  # width, height

        os.chdir(sys._MEIPASS)  # remove this line, while running this code in IDE
        self.__main_window.wm_iconbitmap("icon.ico")

        self.__textarea = tkinter.Text(self.__main_window, font="lucida 13")
        self.__textarea.pack(fill=tkinter.BOTH, expand=True)

        scrollbar = tkinter.Scrollbar(self.__textarea)
        scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        scrollbar.config(command=self.__textarea.yview)
        self.__textarea.config(yscrollcommand=scrollbar.set)

        self.__file_location = None
        self.__selected_cancel = False

        menu_bar = tkinter.Menu(self.__main_window)

        file_menu = tkinter.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.__new_file)
        file_menu.add_command(label="Open", command=self.__open_file)
        file_menu.add_command(label="Save", command=self.__save_file)
        file_menu.add_command(label="Save As", command=self.__saveas_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.__exit_app)

        edit_menu = tkinter.Menu(menu_bar, tearoff=0)

        edit_menu.add_command(label="Cut", command=lambda: self.__textarea.event_generate("<<Cut>>"))
        edit_menu.add_command(label="Copy", command=lambda: self.__textarea.event_generate("<<Copy>>"))
        edit_menu.add_command(label="Paste", command=lambda: self.__textarea.event_generate("<<Paste>>"))
        edit_menu.add_command(label="Delete", command=lambda: self.__textarea.event_generate("<BackSpace>"))

        help_menu = tkinter.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About Notepad", command=self.__about)

        menu_bar.add_cascade(label="File", menu=file_menu)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.__main_window.config(menu=menu_bar)

    def __new_file(self):
        if len(self.__textarea.get(1.0, tkinter.END)) > 1:
            self.__save_file_dialog()
            if self.__selected_cancel:
                return
        self.__main_window.title("Untitled - Notepad")
        self.__textarea.delete(1.0, tkinter.END)
        self.__file_location = None

    def __open_file(self):
        if len(self.__textarea.get(1.0, tkinter.END)) > 1:
            self.__save_file_dialog()
            if self.__selected_cancel:
                return

        file = tkinter.filedialog.askopenfile(defaultextension=".txt",
                                              filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
        if file:
            self.__file_location = file.name
            filename = file.name.split('/')[-1].split('.')[0]
            self.__main_window.title(f"{filename} - Notepad")
            self.__textarea.delete(1.0, tkinter.END)
            self.__textarea.insert(1.0, file.read())
            file.close()

    def __save_file(self):
        if not self.__file_location:
            self.__saveas_file()
            return

        try:
            file = open(file=self.__file_location, mode='w')
            file.write(self.__textarea.get(1.0, tkinter.END))
            file.close()
        except Exception as e:
            print('Exception:', str(e))
            self.__saveas_file()

    def __saveas_file(self):
        file = tkinter.filedialog.asksaveasfile(initialfile="*.txt", defaultextension=".txt",
                                                filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])

        if file:
            self.__file_location = file.name
            filename = file.name.split('/')[-1].split(".")[0]
            self.__main_window.title(f"{filename} - Notepad")
            file.write(self.__textarea.get(1.0, tkinter.END))
            file.close()
        else:
            self.__selected_cancel = True

    def __exit_app(self):
        if len(self.__textarea.get(1.0, tkinter.END)) > 1:
            self.__save_file_dialog()
            if self.__selected_cancel:
                return
        self.__main_window.destroy()

    def __about(self):
        child_window = tkinter.Toplevel(self.__main_window)
        child_window.geometry("300x130")
        child_window.minsize(300, 130)
        child_window.maxsize(300, 130)
        child_window.transient(self.__main_window)
        child_window.title("About Notepad")

        frame = tkinter.Frame(child_window)

        label = tkinter.Label(frame, text=f"This app is created using Tkinter by Mayura.")
        label.pack(pady=30)

        button = tkinter.Button(frame, text="OK", command=child_window.destroy)
        button.pack(side=tkinter.RIGHT, pady=10)
        frame.pack()
        child_window.grab_set()

    def run(self):
        self.__main_window.mainloop()

    def __save_file_dialog(self):
        def cancel():
            self.__selected_cancel = True
            child_window.destroy()

        def dont_save():
            self.__selected_cancel = False
            child_window.destroy()

        def save():
            self.__selected_cancel = False
            self.__save_file()
            child_window.destroy()

        child_window = tkinter.Toplevel(self.__main_window, background="white")
        child_window.geometry("350x100")
        child_window.minsize(350, 100)
        child_window.maxsize(350, 100)
        child_window.transient(self.__main_window)
        child_window.title("Notepad")

        frame = tkinter.Frame(child_window, background="white")
        filename = self.__main_window.title().split(' - ')[0]
        label = tkinter.Label(frame, text=f"Do you want to save changes to {filename}?", foreground="blue",
                              font="lucida 10", background="white")
        label.pack(pady=15, side=tkinter.LEFT, padx=5)
        frame.pack(expand=True, side=tkinter.TOP, fill=tkinter.BOTH)

        frame = tkinter.Frame(child_window)
        button = tkinter.Button(frame, text="Cancel", command=cancel)
        button.pack(side=tkinter.RIGHT, padx=10, pady=10, ipadx=10)
        button = tkinter.Button(frame, text="Don't Save", command=dont_save)
        button.pack(side=tkinter.RIGHT, pady=10, ipadx=10)
        button = tkinter.Button(frame, text="Save", command=save)
        button.pack(side=tkinter.RIGHT, padx=10, pady=10, ipadx=10)

        frame.pack(expand=True, side=tkinter.BOTTOM, fill=tkinter.BOTH, ipadx=5, ipady=10)

        child_window.grab_set()
        child_window.wait_window()


if __name__ == '__main__':
    app = Notepad()
    app.run()
