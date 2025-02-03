from tkinter import *
from tkinter import messagebox,filedialog
import requests
from bs4 import BeautifulSoup
import plyer
import pandas as pd
import turtle
import time
import tkinter as tk


def main_application():
    def datacollected():
        def notification(title, message):
            plyer.notification.notify(
                title=title,
                message=message,
                app_icon='corona.ico',
                timeout=15
            )

        url = "https://worldometers.info/coronavirus/"
        res = requests.get(url)
        soup = BeautifulSoup(res.content, 'html.parser')
        tbody = soup.find('tbody')
        abc = tbody.find_all('tr')
        country_notification = cntdata.get().strip().lower()

        if not country_notification:
            messagebox.showerror("Error", "Please enter a country name.", parent=coro)
            return

        serial_number, countries, total_cases, new_cases, total_death, new_deaths, total_recovered, active_cases = [], [], [], [], [], [], [], []
        serious_critical, total_cases_permn, total_deaths_permn, total_tests, total_test_permillion, total_pop = [], [], [], [], [], []

        header = ['serial_number', 'countries', 'total_cases', 'new_cases', 'total_death', 'new_deaths',
                  'total_recovered',
                  'active_cases', 'serious_critical', 'total_cases_permn', 'total_deaths_permn', 'total_tests',
                  'total_test_permillion', 'total_pop']

        country_found = False  # Flag to check if the country was found

        for i in abc:
            id = i.find_all('td')
            country_name = id[1].text.strip().lower()

            # Only process data for the specified country
            if country_name != country_notification:
                continue

            country_found = True  # Set flag to True if the country is found

            totalcases1 = int(id[2].text.strip().replace(',', ""))
            totaldeath = id[4].text.strip().replace(',', "")
            newcases = id[3].text.strip().replace(',', "")
            newdeaths = id[5].text.strip().replace(',', "")
            notification(
                f"CORONA RECENT UPDATES OF {country_notification.capitalize()}",
                f"Total Cases : {totalcases1}\nTotal Deaths : {totaldeath}\nNew Cases : {newcases}\nNew Deaths : {newdeaths}"
            )

            serial_number.append(id[0].text.strip())
            countries.append(id[1].text.strip())
            total_cases.append(id[2].text.strip().replace(',', ""))
            new_cases.append(id[3].text.strip().replace(',', ""))
            total_death.append(id[4].text.strip().replace(',', ""))
            new_deaths.append(id[5].text.strip().replace(',', ""))
            total_recovered.append(id[6].text.strip().replace(',', ""))
            active_cases.append(id[7].text.strip().replace(',', ""))
            serious_critical.append(id[8].text.strip().replace(',', ""))
            total_cases_permn.append(id[9].text.strip().replace(',', ""))
            total_deaths_permn.append(id[10].text.strip().replace(',', ""))
            total_tests.append(id[11].text.strip().replace(',', ""))
            total_test_permillion.append(id[12].text.strip().replace(',', ""))
            total_pop.append(id[13].text.strip().replace(',', ""))
            break  # Stop processing once the specified country's data is found

        if not country_found:
            messagebox.showerror("Error", f"Country '{country_notification.capitalize()}' not found.", parent=coro)
            return

        dataframe = pd.DataFrame(list(zip(serial_number, countries, total_cases, new_cases, total_death, new_deaths,
                                          total_recovered, active_cases, serious_critical, total_cases_permn,
                                          total_deaths_permn, total_tests, total_test_permillion, total_pop)),
                                 columns=header)

        for a in flist:
            if a == 'html':
                path2 = f'{path}/coronadata_{country_notification}.html'
                dataframe.to_html(path2)
            if a == 'json':
                path2 = f'{path}/coronadata_{country_notification}.json'
                dataframe.to_json(path2)
            if a == 'csv':
                path2 = f'{path}/coronadata_{country_notification}.csv'
                dataframe.to_csv(path2)
            if len(flist) != 0:
                messagebox.showinfo("Notification",
                                    f"Corona Record for {country_notification.capitalize()} is saved at {path2}",
                                    parent=coro)

    def downloaddata():
        global path
        if len(flist) != 0:
            path = filedialog.askdirectory()
            print(path)
        else:
            pass
        datacollected()
        flist.clear()
        Inhtml.configure(state='normal')
        Injson.configure(state='normal')
        Incsv.configure(state='normal')

    def inhtmldownload():
        flist.append('html')
        Inhtml.configure(state='disabled')

    def injsondownload():
        flist.append('json')
        Injson.configure(state='disabled')

    def incsvdownload():
        flist.append('csv')
        Incsv.configure(state='disabled')

    coro = Tk()
    coro.title("Corona Virus Tracker Application")
    coro.geometry('800x600')  # Set size to 450x450
    coro.configure(bg="#F5F5F5")  # Light background
    coro.iconbitmap('corona.ico')
    coro.resizable(False, False)  # Disable resizing
    flist = []

    # Full-width header label
    mainlabel = Label(coro, text="Corona Virus Live Tracker", font=("Arial", 20, "bold"), bg="#28A745", fg="white",
                      width=50, height=2)
    mainlabel.grid(row=0, column=0, columnspan=2, pady=20)

    # Country label with professional look
    label1 = Label(coro, text="Enter Country Name", font=("Arial", 16, "bold"), bg="#F5F5F5")
    label1.grid(row=1, column=0, padx=20, pady=10, sticky='e')

    # Entry for country name
    cntdata = StringVar()
    entry1 = Entry(coro, textvariable=cntdata, font=("Arial", 14), relief=RIDGE, bd=2, width=25)
    entry1.grid(row=1, column=1, padx=20, pady=10, sticky='w')

    # Label for file download option
    label2 = Label(coro, text="Select File Type", font=("Arial", 16, "bold"), bg="#F5F5F5")
    label2.grid(row=2, column=0, padx=20, pady=10, sticky='e')

    # Buttons for file type options
    Inhtml = Button(coro, text="HTML", bg="#17A2B8", font=("Arial", 14, "bold"), relief=RIDGE, activebackground="Black",
                    activeforeground="White", bd=5, width=10, command=inhtmldownload)
    Inhtml.grid(row=2, column=1, padx=20, pady=10)

    Injson = Button(coro, text="JSON", bg="#17A2B8", font=("Arial", 14, "bold"), relief=RIDGE, activebackground="Black",
                    activeforeground="White", bd=5, width=10, command=injsondownload)
    Injson.grid(row=3, column=1, padx=20, pady=10)

    Incsv = Button(coro, text="EXCEL", bg="#17A2B8", font=("Arial", 14, "bold"), relief=RIDGE, activebackground="Black",
                   activeforeground="White", bd=5, width=10, command=incsvdownload)
    Incsv.grid(row=4, column=1, padx=20, pady=10)

    # Submit button
    Submit = Button(coro, text="Submit", bg="#28A745", font=("Arial", 16, "bold"), relief=RIDGE,
                    activebackground="#7B0519", activeforeground="White", bd=5, width=20, command=downloaddata)
    Submit.grid(row=5, column=0, columnspan=2, pady=20)

    coro.mainloop()
# Function to display a splash screen using Turtle
def show_splash_screen():
    wn = turtle.Screen()
    wn.bgcolor("Black")
    wn.screensize(450,450)
    wn.title("Corona Virus Tracker Application")
    root =wn._root
    root.iconbitmap('corona.ico')

    # Create the turtle
    t = turtle.Turtle()
    t.goto(0, 150)
    a, b = 0, 0
    t.speed(200)
    t.pencolor("green")

    # Draw pattern
    while True:
        t.forward(a)
        t.right(b)
        a = a + 3
        b = b + 1
        if b == 210:
            break
        t.hideturtle()

    t.color("green")
    t.penup()

    # Display the message
    t.goto(0, 275)  # Position at the center
    t.write("Welcome to Corona Virus Tracker Application!", align="center", font=("Arial", 24, "bold"))
    time.sleep(2)
    t.hideturtle()

    # Close the Turtle graphics window
    turtle.bye()

show_splash_screen()
main_application()
