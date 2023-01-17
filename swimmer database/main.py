from tkinter import *
from PIL import ImageTk
from tkinter import messagebox

window = Tk()

def login():
    # Empty fields in login
    if usernameEntry.get() == "" or passEntry.get() == "":
        messagebox.showerror("Login denied.", "Fields cannot be empty.")

    # Enter user = jtian and pass = UCRO
    elif usernameEntry.get() == "jtian" and passEntry.get() == "UCRO": 
        messagebox.showinfo("Login successful.", "Welcome swimmer")
        window.destroy()
        import sps
        
    else:
        messagebox.showerror("Login denied.", "Please re-enter your userId and password.")

# Window top left corner at (0, 0) with dimensions 1000px x 700px
window.geometry("1000x700+0+0") 
window.title("Swimmer Login")

window.resizable(False, False) # Cannot maximize image

backgroundImg = ImageTk.PhotoImage(file="swimlogin.png")

bgLabel = Label(window, image=backgroundImg)
bgLabel.place(x=0, y=0)

loginFrame = Frame(window)
loginFrame.place(x=250, y=150) # Where to place login inputs

iconImg = ImageTk.PhotoImage(file="swimicon.png")
iconLabel = Label(loginFrame, image=iconImg)
iconLabel.grid(row=0, column=0, columnspan=2)

usernameLabel = Label(loginFrame, text="swimID", compound=LEFT, 
                font=('arial', 20))
usernameLabel.grid(row=1, column=0, pady=10, padx=20)

usernameEntry = Entry(loginFrame, font=('arial', 20))
usernameEntry.grid(row=1, column=1, pady=10, padx=20)

passwordLabel = Label(loginFrame, text="password", compound=LEFT
                ,font=('arial', 20))
passwordLabel.grid(row=2, column=0, pady=10, padx=20)

passEntry = Entry(loginFrame, font=('arial', 20))
passEntry.grid(row=2, column=1, pady=10, padx=20)

loginBtn = Button(loginFrame, text="Login", font=('arial', 20)
            ,fg="white", bg="darkturquoise", activebackground="darkturquoise"
            , activeforeground="white", cursor="hand2", command=login)
loginBtn.grid(row=3, column=1, padx=20, pady=10)

window.mainloop()