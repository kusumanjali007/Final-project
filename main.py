import tkinter as tk
from tkinter import Button, ttk, messagebox
from tkcalendar import Calendar
from datetime import datetime
from PIL import Image
import pytz

# Dummy credentials for the login
USERNAME = "Kusumadeepa@gmail.com"
PASSWORD = "password"


def open_calendar_window(check_type):
    calendar_window = tk.Toplevel(root)
    calendar_window.title(f"Select {check_type} Date")
    calendar_window.geometry("300x300")

    cal = Calendar(calendar_window, selectmode='day', date_pattern='y-mm-dd')
    cal.grid(row=0, column=0, padx=10, pady=10)

    def get_selected_date_and_close():
        selected_date = cal.selection_get()
        print(f"Selected {check_type} Date:", selected_date)
        if check_type == "Check-in":
            checkin_date.set(selected_date)
        elif check_type == "Check-out":
            checkout_date.set(selected_date)
        calendar_window.destroy()

    submit_button = tk.Button(calendar_window, text="Submit", command=get_selected_date_and_close)
    submit_button.grid(row=1, column=0, padx=10, pady=10)

def confirm_booking():
    if checkin_date.get() == "" or checkout_date.get() == "" or place_combobox.get() == "" or transport_var.get() == "":
        messagebox.showerror("Error", "Please fill in all the details.")
    else:
        checkin_date_obj = datetime.strptime(checkin_date.get(), "%Y-%m-%d")
        checkout_date_obj = datetime.strptime(checkout_date.get(), "%Y-%m-%d")

        if checkout_date_obj <= checkin_date_obj:
            messagebox.showerror("Error", "Check-out date should be greater than Check-in date.")
        else:
            confirmation_window = tk.Toplevel(root)
            confirmation_window.title("Confirmation")
            confirmation_window.geometry("400x300")
            confirmation_window.configure(bg="white")

            confirmation_label = tk.Label(confirmation_window, text="Booking Confirmed!", font=("Arial", 20), bg="white")
            confirmation_label.pack(pady=10)

            tk.Label(confirmation_window, text=f"Check-in Date: {checkin_date.get()}", bg="white").pack()
            tk.Label(confirmation_window, text=f"Check-out Date: {checkout_date.get()}", bg="white").pack()
            tk.Label(confirmation_window, text=f"Selected Place: {place_combobox.get()}", bg="white").pack()
            tk.Label(confirmation_window, text=f"Selected Transport: {transport_var.get()}", bg="white").pack()

            done_image = tk.PhotoImage(file="done1.png")
            done_label = tk.Label(confirmation_window, image=done_image)
            done_label.image = done_image
            done_label.pack(pady=10)

def create_currency_converter_window():
    converter_window = tk.Toplevel(root)
    converter_window.title("Currency Converter")
    converter_window.geometry("300x200")

    def perform_conversion():
        amount = float(amount_var.get())
        from_currency = from_currency_var.get()
        to_currency = to_currency_var.get()

        exchange_rate_usd = 0.012  # Example exchange rate (USD to INR)
        exchange_rate_eur = 0.011
        exchange_rate_gbp =0.0094
        exchange_rate_inr = 83.45

        if from_currency == 'USD':
            from_exchange_rate = exchange_rate_usd
        elif from_currency == 'EUR':
            from_exchange_rate = exchange_rate_eur
        elif from_currency == 'GBP':
            from_exchange_rate = exchange_rate_gbp
        elif from_currency == 'INR':
            from_exchange_rate = exchange_rate_inr
        else:
            raise ValueError("Invalid 'From' currency")

        if to_currency == 'USD':
            to_exchange_rate = exchange_rate_usd
        elif to_currency == 'EUR':
            to_exchange_rate = exchange_rate_eur
        elif to_currency == 'GBP':
            to_exchange_rate = exchange_rate_gbp
        elif to_currency == 'INR':
            to_exchange_rate = exchange_rate_inr
        else:
            raise ValueError("Invalid 'To' currency")

        converted_amount = amount * (to_exchange_rate / from_exchange_rate)
        result_label.config(text=f"Converted Amount: {converted_amount:.2f} {to_currency}")

    amount_label = tk.Label(converter_window, text="Enter Amount:")
    amount_label.grid(row=0, column=0, padx=10, pady=10)
    amount_var = tk.DoubleVar()
    amount_entry = tk.Entry(converter_window, textvariable=amount_var)
    amount_entry.grid(row=0, column=1, padx=10, pady=10)

    from_currency_label = tk.Label(converter_window, text="From Currency:")
    from_currency_label.grid(row=1, column=0, padx=10, pady=10)
    from_currency_var = tk.StringVar()
    from_currency_menu = ttk.Combobox(converter_window, textvariable=from_currency_var, values=['USD', 'EUR', 'GBP', 'INR'])
    from_currency_menu.grid(row=1, column=1, padx=10, pady=10)
    from_currency_menu.set('USD')

    to_currency_label = tk.Label(converter_window, text="To Currency:")
    to_currency_label.grid(row=2, column=0, padx=10, pady=10)
    to_currency_var = tk.StringVar()
    to_currency_menu = ttk.Combobox(converter_window, textvariable=to_currency_var, values=['USD', 'EUR', 'GBP', 'INR'])
    to_currency_menu.grid(row=2, column=1, padx=10, pady=10)
    to_currency_menu.set('USD')

    convert_button = tk.Button(converter_window, text="Convert", command=perform_conversion)
    convert_button.grid(row=3, column=0, columnspan=2, pady=10)

    result_label = tk.Label(converter_window, text="")
    result_label.grid(row=4, column=0, columnspan=2, pady=10)

def get_current_time(timezone):
    tz = pytz.timezone(timezone)
    current_time = datetime.now(tz)
    return current_time.strftime('%H:%M:%S %p')

def calculate_time_difference():
    source_timezone = source_timezone_combobox.get()
    destination_timezone = destination_timezone_combobox.get()

    if source_timezone and destination_timezone:
        source_time = get_current_time(source_timezone)
        destination_time = get_current_time(destination_timezone)

        time_difference = calculate_time_delta(source_time, destination_time)
        messagebox.showinfo("Time Difference", f"The time difference between {source_timezone} and {destination_timezone} is {time_difference}")
    else:
        messagebox.showerror("Error", "Please select both source and destination timezones.")

def calculate_time_delta(source_time, destination_time):
    fmt = '%H:%M:%S %p'
    source_time = datetime.strptime(source_time, fmt)
    destination_time = datetime.strptime(destination_time, fmt)

    if source_time > destination_time:
        delta = source_time - destination_time
    else:
        delta = destination_time - source_time

    return str(delta)

def update_ist_time():
    tz = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(tz)
    ist_time = current_time.strftime('%H:%M:%S %p')
    ist_label.config(text=f"Current Time in IST: {ist_time}", font=("Arial", 25))
    ist_label.after(1000, update_ist_time)

def open_timezone_window():
    global source_timezone_combobox, destination_timezone_combobox, ist_label
    timezone_window = tk.Toplevel(root)
    timezone_window.title("Select Time Zone")
    timezone_window.geometry("550x250")

    timezone_frame = tk.Frame(timezone_window, bg="white")
    timezone_frame.pack(fill=tk.BOTH, expand=True)

    ist_label = tk.Label(timezone_frame, text="", bg="white")
    ist_label.grid(row=1, column=0, columnspan=2, pady=10)

    source_label = tk.Label(timezone_frame, text="Source Timezone:", bg="white")
    source_label.grid(row=2, column=0, padx=5, pady=5)

    source_timezones = pytz.all_timezones
    source_timezone_combobox = ttk.Combobox(timezone_frame, values=source_timezones)
    source_timezone_combobox.grid(row=2, column=1, padx=5, pady=5)
    source_timezone_combobox.set("")

    destination_label = tk.Label(timezone_frame, text="Destination Timezone:", bg="white")
    destination_label.grid(row=3, column=0, padx=5, pady=5)

    destination_timezones = pytz.all_timezones
    destination_timezone_combobox = ttk.Combobox(timezone_frame, values=destination_timezones)
    destination_timezone_combobox.grid(row=3, column=1, padx=5, pady=5)
    destination_timezone_combobox.set("")

    calculate_button = tk.Button(timezone_frame, text="Calculate Time Difference", command=calculate_time_difference, bg="black", fg="white")
    calculate_button.grid(row=4, column=0, columnspan=2, pady=10)

    update_ist_time()

def order_pizza(): #function to create a pizza ordering window
    pizza_order_window = tk.Toplevel(root)
    pizza_order_window.title("Pizza Order")
    pizza_order_window.geometry("600x500")

    # Load the image
    pizzaimage = tk.PhotoImage(file="pizza1.png") # Update with your image file path
    pimage_label = tk.Label(pizza_order_window, image=pizzaimage, width="600", height="200")
    pimage_label.image = pizzaimage
    pimage_label.grid(row=0,column=0,columnspan=2)

    size_label = tk.Label(pizza_order_window, text="Select Pizza Size:")
    size_label.grid(row=1, column=0, padx=10, pady=10)
    size_var = tk.StringVar()
    size_menu = ttk.Combobox(pizza_order_window, textvariable=size_var, values=['Small', 'Medium', 'Large'])
    size_menu.grid(row=1, column=1, padx=10, pady=10)
    size_menu.set('Medium')

    topping_label = tk.Label(pizza_order_window, text="Select Toppings:")
    topping_label.grid(row=3, column=0, padx=10, pady=10)
    topping_options = ['Pepperoni', 'Mushrooms', 'Onions', 'Sausage', 'Green Peppers']
    toppings_vars = {topping: tk.BooleanVar() for topping in topping_options}
    for i,topping in enumerate(topping_options):
        chk_topping = tk.Checkbutton(pizza_order_window, text=topping, variable=toppings_vars[topping])
        chk_topping.grid(row=i+3, column=1, sticky='w', padx=10)

    address_label = tk.Label(pizza_order_window, text="Delivery Address:")
    address_label.grid(row=len(topping_options)+3, column=0, padx=10, pady=10)
    address_var = tk.StringVar()
    address_entry = tk.Entry(pizza_order_window, textvariable=address_var)
    address_entry.grid(row=len(topping_options)+3, column=1, padx=10, pady=10)

    confirm_button = tk.Button(pizza_order_window, text="Confirm Order", command=lambda: confirm_order(size_var.get(), toppings_vars, address_var.get(), pizza_order_window))
    confirm_button.grid(row=len(topping_options)+4, column=0, columnspan=2, pady=10)

def confirm_order(size, toppings_vars, address, window): #function to confirm the order
    # Check if any field is empty
    if size == "" or address == "":
        messagebox.showerror("Error", "Please fill in all the details.")
    else:
        toppings = [topping for topping, var in toppings_vars.items() if var.get()]

        # Check if toppings are selected
        if not toppings:
            messagebox.showerror("Error", "Please select at least one topping.")
        else:
            # If all fields are filled, proceed with order confirmation
            size_prices = {'Small': 200, 'Medium': 350, 'Large': 500}
            topping_price = 50
            pizza_price = size_prices[size] + len(toppings) * topping_price

            order_summary = f"Order Summary:\nSize: {size}\nToppings: {', '.join(toppings)}\nDelivery Address: {address}\nTotal Price: ${pizza_price:.2f}"

            messagebox.showinfo("Order Confirmation", order_summary)
            window.destroy()


            # Function to handle the submission of customer details
            def submit_details():
                name = entry_name.get()
                age = entry_age.get()
                gender = entry_gender.get()
                contact = entry_contact.get()

                # Basic validation
                if not name or not age or not gender or not contact:
                    messagebox.showwarning("Input Error", "All fields are required")
                    return

                # Display the details in the text widget
                details_text.insert(tk.END, f"Name: {name}\n")
                details_text.insert(tk.END, f"Age: {age}\n")
                details_text.insert(tk.END, f"Gender: {gender}\n")
                details_text.insert(tk.END, f"Contact: {contact}\n\n")

                # Clear the entry fields
                entry_name.delete(0, tk.END)
                entry_age.delete(0, tk.END)
                entry_gender.delete(0, tk.END)
                entry_contact.delete(0, tk.END)

            # Create the main window
            root = tk.Tk()
            root.title("Travel Application")

            # Create and place labels and entry widgets
            tk.Label(root, text="Customer Name:").grid(row=0, column=0, padx=10, pady=5)
            entry_name = tk.Entry(root)
            entry_name.grid(row=0, column=1, padx=10, pady=5)

            tk.Label(root, text="Age:").grid(row=1, column=0, padx=10, pady=5)
            entry_age = tk.Entry(root)
            entry_age.grid(row=1, column=1, padx=10, pady=5)

            tk.Label(root, text="Gender:").grid(row=2, column=0, padx=10, pady=5)
            entry_gender = tk.Entry(root)
            entry_gender.grid(row=2, column=1, padx=10, pady=5)

            tk.Label(root, text="Contact:").grid(row=3, column=0, padx=10, pady=5)
            entry_contact = tk.Entry(root)
            entry_contact.grid(row=3, column=1, padx=10, pady=5)

            # Create and place the submit button
            submit_button = tk.Button(root, text="Submit", command=submit_details)
            submit_button.grid(row=4, column=0, columnspan=2, pady=10)

            # Create a text widget to display the details
            details_text = tk.Text(root, width=40, height=10)
            details_text.grid(row=5, column=0, columnspan=2, padx=10, pady=10)





def validate_credentials(username, password):
    return username == USERNAME and password == PASSWORD

def login():
    entered_username = username_entry.get()
    entered_password = password_entry.get()

    if validate_credentials(entered_username, entered_password):
        login_window.destroy()
        show_main_window()
    else:
        messagebox.showerror("Login Failed", "Invalid Email or password")



def show_main_window():
    global root, checkin_date, checkout_date, place_combobox, transport_var

    root = tk.Tk()
    root.title("Travel  Management Application")
    root.geometry("900x700")

    app_frame = tk.Frame(root, bg="white")
    app_frame.pack(fill=tk.BOTH, expand=True)

    title_label = tk.Label(app_frame, text="Travel Management Application", font=("Georgia", 25), bg="white", fg="#638d75")
    title_label.grid(row=0, column=1, columnspan=2, padx=10, pady=10)

    navbar_frame = tk.Frame(app_frame, bg="#638d75", relief=tk.RAISED, bd=2)
    navbar_frame.grid(row=1, column=0, columnspan=4, sticky="ew")

    food_button = tk.Button(navbar_frame, text="Order Food", bg="white", fg="#638d75", command=order_pizza)
    food_button.grid(row=0, column=1, padx=5, pady=5)

    time_button = tk.Button(navbar_frame, text="Time Zone", bg="white", fg="#638d75", command=open_timezone_window)
    time_button.grid(row=0, column=2, padx=5, pady=5)

    currency_button = tk.Button(navbar_frame, text="Currency Converter", bg="white", fg="#638d75", command=create_currency_converter_window)
    currency_button.grid(row=0, column=3, padx=5, pady=5)

    image = tk.PhotoImage(file="travel1.png")  # Update with your image file path
    image_label = tk.Label(app_frame, image=image, width="1300", height="300")
    image_label.grid(row=2, column=0, columnspan=4, padx=10, pady=10)

    date_frame = tk.Frame(app_frame, bg="white")
    date_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

    checkin_date = tk.StringVar()
    checkout_date = tk.StringVar()

    checkin_label = tk.Label(date_frame, text="Check-in Date:", bg="white")
    checkin_label.grid(row=0, column=0, padx=40, pady=10)
    checkin_entry = tk.Entry(date_frame, textvariable=checkin_date, state="readonly")
    checkin_entry.grid(row=0, column=1, padx=10, pady=10)

    checkout_label = tk.Label(date_frame, text="Check-out Date:", bg="white")
    checkout_label.grid(row=0, column=3, padx=40, pady=10)
    checkout_entry = tk.Entry(date_frame, textvariable=checkout_date, state="readonly")
    checkout_entry.grid(row=0, column=4, padx=10, pady=10)

    checkin_button = tk.Button(date_frame, text="Select Check-in Date", bg="black", fg="white", command=lambda: open_calendar_window("Check-in"))
    checkin_button.grid(row=0, column=2, padx=15, pady=5)

    checkout_button = tk.Button(date_frame, text="Select Check-out Date", bg="black", fg="white", command=lambda: open_calendar_window("Check-out"))
    checkout_button.grid(row=0, column=5, padx=15, pady=5)

    place_frame = tk.Frame(app_frame, bg="white")
    place_frame.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

    place_label = tk.Label(place_frame, text="Select Place:", bg="white")
    place_label.grid(row=0, column=0, padx=5, pady=5)

    places = ["New York", "London", "Paris", "USA", "Delhi","Agra","Mumbai", "kolkata", "Goa", "Canada","Mysore","Chennai"]
    place_combobox = ttk.Combobox(place_frame, values=places)
    place_combobox.grid(row=0, column=1, padx=5, pady=5)

    transport_frame = tk.Frame(app_frame, bg="white")
    transport_frame.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

    transport_label = tk.Label(transport_frame, text="Select Transport:", bg="white")
    transport_label.grid(row=0, column=0, padx=5, pady=5)

    transport_var = tk.StringVar(value=" ")
    car_radio = tk.Radiobutton(transport_frame, text="Car", variable=transport_var, value="Car", bg="white")
    car_radio.grid(row=0, column=1, padx=5, pady=5)
    train_radio = tk.Radiobutton(transport_frame, text="Train", variable=transport_var, value="Train", bg="white")
    train_radio.grid(row=0, column=2, padx=5, pady=5)
    Flight_radio = tk.Radiobutton(transport_frame, text="Flight", variable=transport_var, value="Flight", bg="white")
    Flight_radio.grid(row=0, column=3, padx=5, pady=5)

    Bus_radio = tk.Radiobutton(transport_frame, text="Bus", variable=transport_var, value="BUS", bg="white")
    Bus_radio.grid(row=0, column=4, padx=5, pady=5)

    confirm_button = tk.Button(app_frame, text="Confirm Booking", bg="black", fg="white", command=confirm_booking)
    confirm_button.grid(row=6, column=0, columnspan=3, pady=10)

    root.mainloop()

# Login window
login_window = tk.Tk()
login_window.title(" Login Here ")
login_window.geometry("600x400")

username_label = tk.Label(login_window, text="Email:")
username_label.pack(pady=5)
username_entry = tk.Entry(login_window)
username_entry.pack(pady=5)

password_label = tk.Label(login_window, text="Password:")
password_label.pack(pady=5)
password_entry = tk.Entry(login_window, show="*")
password_entry.pack(pady=5)

login_button = tk.Button(login_window, text="Login", command=login)
login_button.pack(pady=20)

login_window.mainloop()