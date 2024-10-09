import random
from tkinter import *
from tkinter import messagebox
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = password_letters + password_symbols + password_numbers

    random.shuffle(password_list)

    password = "".join(password_list)
    password_entry.delete(0,END)
    password_entry.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SEARCH WEBSITE ------------------------------ #
def search_password():
    website = website_entry.get().title()
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")
    else:
        if website in data:
            username = data[website]["username"]
            password = data[website]["password"]
            # Create a new Toplevel window for displaying the credentials
            top = Toplevel(window)
            top.title(website)
            top.config(padx=20, pady=20)

            username_label = Label(top, text="Username:")
            username_label.grid(column=0, row=0, padx=5, pady=5)
            username_entry = Entry(top, width=35)
            username_entry.grid(column=1, row=0, padx=5, pady=5)
            username_entry.insert(0, username)
            username_entry.config(state="readonly")

            password_label = Label(top, text="Password:")
            password_label.grid(column=0, row=1, padx=5, pady=5)
            password_entry = Entry(top, width=35)
            password_entry.grid(column=1, row=1, padx=5, pady=5)
            password_entry.insert(0, password)  # Insert the password into the Entry widget
            password_entry.config(state="readonly")  # Make it readonly but selectable

            close_button = Button(top, text="Close", command=top.destroy)
            close_button.grid(column=1, row=2, pady=10)
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exists.")

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website = website_entry.get().title()
    username = username_entry.get()
    passcode = password_entry.get()
    new_data = {
        website: {
            "username":username,
            "password":passcode
        }
    }
    if len(website) == 0 or len(username) == 0 or len(passcode) == 0:
        messagebox.showwarning(title="Oops", message="Please don't leave any field empty")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \nUsername: {username} \nPassword: {passcode} \nIs it ok to save?")
        if is_ok:
            try:
                with open("data.json", "r") as file:
                    data = json.load(file)
            except FileNotFoundError:
                with open("data.json", "w") as file:
                    json.dump(new_data, file, indent=4)
            else:
                data.update(new_data)
                with open("data.json", "w") as file:
                    json.dump(data, file, indent=4)
            finally:
                website_entry.delete(0,END)
                username_entry.delete(0,END)
                password_entry.delete(0,END)

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg="white")


canvas = Canvas(width=200, height=200, bg="white", highlightthickness=0)
logo = PhotoImage(file="logo.png")
canvas.create_image(140,100,image=logo)
canvas.grid(column=1, row=0)

website_label= Label(text="Website:", bg="white")
website_label.grid(column=0, row=1)
website_entry = Entry(width=32)
website_entry.grid(column=1, row=1)
website_entry.focus()
website_button = Button(text="Search", width=15, command=search_password)
website_button.grid(column=2, row=1)

username_label= Label(text="Username:", bg="white")
username_label.grid(column=0, row=2)
username_entry = Entry(width=51)
username_entry.grid(column=1, row=2, columnspan=2)

password_label = Label(text="Password:", bg="white")
password_label.grid(column=0, row=3)
password_entry = Entry(width=32)
password_entry.grid(column=1, row=3)
password_button = Button(text="Generate Password", command=generate_password)
password_button.grid(column=2, row=3)

add_button = Button(text="Add", width=43, command=save_password)
add_button.grid(column=1, row=4, columnspan=2)

window.mainloop()