import tkinter as tk
from tkinter import *
import pyodbc
import tkcalendar
import tkintermapview
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime

class LoginPage(tk.Tk): # login page
    def __init__(self):
        super().__init__()
        
        # Update the window to calculate its width and height
        self.update_idletasks()
        self.title("Login")

        # Calculate the center coordinates relative to the screen
        x = (self.winfo_screenwidth() - self.winfo_reqwidth()) / 2
        y = (self.winfo_screenheight() - self.winfo_reqheight()) / 2

        # Set the window's geometry to be centered on the screen
        self.geometry(f"+{int(x)}+{int(y)}")
        self.resizable(False, False)

        self.username_label = ttk.Label(self, text="Username:")
        self.username_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        self.username_entry = ttk.Entry(self)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        self.password_label = ttk.Label(self, text="Password:")
        self.password_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        self.login_button = ttk.Button(self, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()


        if username == "admin" and password == "password":
            messagebox.showinfo("Login Successful", "Welcome Admin!")
            self.destroy()  # Close the login window
            app = LouisianaMapApp(admin=True)   # give admin priviliges
            app.mainloop()
        elif username == "guest" and password == "guestpassword":
            messagebox.showinfo("Login Successful", "Welcome Guest!")
            self.destroy()  # Close the login window
            app = LouisianaMapApp(admin=False) # restrict admin privileges
            app.mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

class LouisianaMapApp(tk.Tk):   # our main window
    def __init__(self, admin=False):
        super().__init__()
        self.marker_dict = {}
        
        self.title("Air Quality of Louisiana")
        self.geometry("1300x650")

        self.admin = admin

        self.create_widgets()

    def create_widgets(self):
        self.input_label = tk.Label(self, text="Selected City:")
        self.input_label.grid(column=0, row=1, sticky="NW")

        self.input_entry = tk.Entry(self, width=35)
        self.input_entry.grid(column=1, row=1, sticky="NW")

        self.date_label = tk.Label(self, text="Date: ")
        self.date_label.grid(column=0, row=2, sticky="NW", pady=(100, 10))

        self.calendar = tkcalendar.Calendar(self, year=2024, month=3, day=22)
        self.calendar.grid(column=1, row=2, rowspan=2, sticky="NW", pady=(100, 10))

        self.year_label = tk.Label(self, text="Year: ")
        self.year_label.grid(column=2, row=1, sticky="E")

        self.year_entry = tk.Entry(self, width=35)
        self.year_entry.grid(column=3, row=1, sticky="W")

        self.sort_label = tk.Label(self, text="Sort: ")
        self.sort_label.grid(column=2, row=2, sticky="SE")

        self.highest_first_sort = tk.Radiobutton(self, text="Highest First", value="highest")
        self.highest_first_sort.grid(column=3, row=2, sticky="SW")

        self.lowest_first_sort = tk.Radiobutton(self, text="Lowest first", value="lowest")
        self.lowest_first_sort.grid(column=3, row=3, sticky="NW")

        self.sort_search_button = tk.Button(self, text="Search by sort", command=self.sortSearch)
        self.sort_search_button.grid(column=4, row=1, sticky="W")

        self.add_submit_button = tk.Button(self, text="Search", command=self.on_user_input)
        self.add_submit_button.grid(column=1, row=4, sticky="E")

        self.add_clear_button = tk.Button(self, text="Clear All", command=self.clear_input)
        self.add_clear_button.grid(column=3, row=4, sticky="W")

        self.map_widget = tkintermapview.TkinterMapView(self, width=500, height=500, corner_radius=5)
        self.map_widget.grid(column=3, row=2, padx=(120,10), pady=(50, 10), rowspan=5, columnspan=5, sticky="SE")
        self.map_widget.set_position(30.9843, -91.9623)
        self.map_widget.set_zoom(7)
        self.map_widget.add_left_click_map_command(self.left_click_event)

        if self.admin:  # if user = admin, add the add more data
            self.add_data_widget = tk.Button(self, text="Add Data", command=self.open_new_data_window)
            self.add_data_widget.grid(column=2, row=4, sticky="W")

        self.output_label = tk.Label(self, text="Output:")
        self.output_label.grid(column=2, row=5, sticky="SW")

        self.air_quality_labels = {}
        labels = ["PM 2.5", "Lung Cancer Cases", "City with highest/lowest rate: "]
        for i, label_text in enumerate(labels):
            label = tk.Label(self, text=f"{label_text}")
            label.grid(column=1, row=6+i*30, sticky="SE")
            entry = tk.Entry(self, width=20)
            entry.grid(column=2, row=6+i*30, sticky="SE")
            self.air_quality_labels[label_text] = entry

        try:
            # our 3 databases
            AirPollutionDB = {
                'server': 'localhost',
                'database': 'AirPollution2',
                'username': 'sa',
                'password': 'DB_Password',
                'driver': '{ODBC Driver 18 for SQL Server}'

            }
            LungCancerDB = {
                'server': 'localhost',
                'database': 'LungCancer',
                'username': 'sa',
                'password': 'DB_Password',
                'driver': '{ODBC Driver 18 for SQL Server}'

            }
            LocationDB = {
                'server': 'localhost',
                'database': 'Location',
                'username': 'sa',
                'password': 'DB_Password',
                'driver': '{ODBC Driver 18 for SQL Server}'
            }

            # connect to all 3 databases
            self.AirPollutionConnection = pyodbc.connect(
                f"DRIVER={AirPollutionDB['driver']};SERVER={AirPollutionDB['server']};DATABASE={AirPollutionDB['database']};"
                f"UID={AirPollutionDB['username']};PWD={AirPollutionDB['password']};TrustServerCertificate=yes"
            )

            self.LungCancerConnection = pyodbc.connect(
                f"DRIVER={LungCancerDB['driver']};SERVER={LungCancerDB['server']};DATABASE={LungCancerDB['database']};"
                f"UID={LungCancerDB['username']};PWD={LungCancerDB['password']};TrustServerCertificate=yes"
            )
            self.LocationConnection = pyodbc.connect(
                f"DRIVER={LocationDB['driver']};SERVER={LocationDB['server']};DATABASE={LocationDB['database']};"
                f"UID={LocationDB['username']};PWD={LocationDB['password']};TrustServerCertificate=yes"
            )
            
            self.loadCities() 
        except Exception as e:
            print("Error connecting to SQL Server:", e)

    def fetch_air_quality_data(self, city, lon, date):
        try:
            cursor = self.AirPollutionConnection.cursor()
            query = "SELECT PM25 FROM BatonRouge2 WHERE Date = ? AND City = ?"
            cursor.execute(query, (date, city))
            rows = cursor.fetchall()
            return rows[0] if rows else None
        except Exception as e:
            print("Error fetching air quality data:", e)
            return None

    def fetchLungCancerRates(self, city, lon, date):
        try:
            cursor = self.LungCancerConnection.cursor()
            query = "SELECT Count FROM LungCancerRates2 WHERE Year = ? AND Parish = ?"
            cursor.execute(query, (date, city))
            rows = cursor.fetchall()
            return rows[0] if rows else None
        except Exception as e:
                print("Error fetching Lung Cancer Rates", e)
                return None

    def clear_input(self):
        for widget in self.winfo_children():
            # Check if the widget is an entry box
            if isinstance(widget, tk.Entry):
                # Clear the entry box
                widget.delete(0, 'end')

    def loadCities(self):
        cursor = self.AirPollutionConnection.cursor()
        cursor.execute("SELECT DISTINCT City FROM BatonRouge2")
        city = cursor.fetchall()
        print("Fetched cities:", city)

    def on_user_input(self):    
        city = self.input_entry.get()
        date_str = self.calendar.get_date()
        date_obj = datetime.strptime(date_str, '%m/%d/%y')
        formatted_date = date_obj.strftime('%Y-%m-%d')
        formatted_date2 = date_obj.strftime('%Y')
        coords = self.fetch_coordinates(city)

        air_quality_data = self.fetch_air_quality_data(city, formatted_date, formatted_date)
        print("Air quality data:", air_quality_data)

        if air_quality_data is not None:
            if air_quality_data:
                self.air_quality_labels["PM 2.5"].delete(0, tk.END)
                self.air_quality_labels["PM 2.5"].insert(0, air_quality_data[0])
                print("Setting PM 2.5 marker...")
            else:
                print("No air quality data found for the provided city.")
        else:
            print("No air quality data found for the provided city.")

        lung_cancer_data = self.fetchLungCancerRates(city, formatted_date2, formatted_date2)
        print("Lung cancer data:", lung_cancer_data)

        if lung_cancer_data is not None:
            if lung_cancer_data:
                self.air_quality_labels["Lung Cancer Cases"].delete(0, tk.END)
                self.air_quality_labels["Lung Cancer Cases"].insert(0, lung_cancer_data[0])
                print("Setting lung cancer marker...")
            else:
                print("No Cancer Rate Data found")
        else:
            print("No Cancer Rate Data found")

        self.update_marker(coords, city, formatted_date, air_quality_data, lung_cancer_data)



    def update_marker(self, coords, city, date, air_quality_data, lung_cancer_data):
        # Check if marker exists for the coordinates
        if coords in self.marker_dict:
            # If marker exists, check if the new city is the same as the city of the existing marker
            existing_marker_city = self.marker_dict[coords]["city"]
            if existing_marker_city == city:
                # If the cities match, update the text of the existing marker with new data
                marker_text = f"City: {city}, Date: {date}\nPM 2.5: {air_quality_data}\nLung Cancer Cases: {lung_cancer_data}"
                self.marker_dict[coords]["marker"].set_text(marker_text)
                return
            else:
                # If the cities don't match, remove the previous marker
                self.map_widget.remove_marker(self.marker_dict[coords]["marker"])
                del self.marker_dict[coords]

        # Create a new marker with updated information
        marker_text = f"City: {city}\nDate: {date}\nPM 2.5: {air_quality_data}\nLung Cancer Cases: {lung_cancer_data}"
        new_marker = self.map_widget.set_marker(coords[0], coords[1], text=marker_text, font=('Arial', 10))
        self.marker_dict[coords] = {"marker": new_marker, "city": city}









    def fetch_coordinates(self, city):
        cities = {
            "Alexandria": (31.332153069519233, -92.478657421875),
            "Baton Rouge": (30.4515, -91.1871),
            "Lafayette": (30.2241, -92.0198),
            "Shreveport": (32.5252, -93.7502)
            # Add coordinates for other cities
        }
        
        return cities.get(city)  # Return coordinates for the specified city if found




    def left_click_event(self, coords):
        print("Left click event with coordinates:", coords[0], coords[1])
        
        cities = {
            "Alexandria": {"latitude": (31.2756, 31.3718), "longitude": (-92.5373, -92.4181)},
            "Baton Rouge": {"latitude": (30.3798, 30.5583), "longitude": (-91.2811, -91.0627)},
            "Chalmette/Vista": {"latitude": (29.9462, 29.9638), "longitude": (-89.9599, -89.9447)},
            "Geismar": {"latitude": (30.1895, 30.2374), "longitude": (-91.0059, -90.9646)},
            "Hammond1": {"latitude": (30.5044, 30.5649), "longitude": (-90.5121, -90.4418)},
            "Hammond2": {"latitude": (30.493, 30.532), "longitude": (-90.5032, -90.4431)},
            "Houma": {"latitude": (29.5417, 29.6516), "longitude": (-90.8129, -90.6942)},
            "New Orleans": {"latitude": (29.9499, 30.081), "longitude": (-90.179, -90.0378)},
            "Kenner": {"latitude": (29.9831, 30.0384), "longitude": (-90.2585, -90.2146)},
            "Lafayette": {"latitude": (30.0941, 30.2815), "longitude": (-92.1014, -91.8371)},
            "Marrero": {"latitude": (29.8841, 29.915), "longitude": (-90.168, -90.0867)},
            "Monroe": {"latitude": (32.4571, 32.5591), "longitude": (-92.0955, -92.0217)},
            "PortAllen": {"latitude": (30.4364, 30.4992), "longitude": (-91.2679, -91.2082)},
            "Shreveport": {"latitude": (32.4543, 32.7006), "longitude": (-94.0417, -93.7152)},
            "Vinton": {"latitude": (30.1507, 30.2249), "longitude": (-93.5337, -93.4488)}
        }
        
        clicked_city = None
        
        for city, values in cities.items():
            lat_range = values["latitude"]
            lon_range = values["longitude"]
            if lat_range[0] <= coords[0] <= lat_range[1] and lon_range[0] <= coords[1] <= lon_range[1]:
                clicked_city = city
                break
        
        if clicked_city:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, clicked_city)
        else:
            print("Clicked outside of any specified city")

    def sortSearch(self):
        cursor = self.LungCancerConnection.cursor()

        


    def open_new_data_window(self): 
        top = Toplevel()
        top.geometry("400x300")
        top.title("Add New Data")

        city_label = Label(top, text="City: ")
        city_label.grid(column=1, row=1)

        self.city_entry = Entry(top, width=25)
        self.city_entry.grid(column=2, row=1)

        date_label = Label(top, text="Date: ")
        date_label.grid(column=1, row=2)

        self.date = tkcalendar.Calendar(top, year=2024, month=3, day=22, font=("Arial", 8))
        self.date.grid(column=2, row=2)

        pm25_label = Label(top, text="PM 2.5: ")
        pm25_label.grid(column=1, row=3)

        self.pm_25_entry = Entry(top, width=25)
        self.pm_25_entry.grid(column=2, row=3)

        cancer_data_label = Label(top, text="Lung Cancer Cases: ")
        cancer_data_label.grid(column=1, row=4)

        self.cancer_data_entry = Entry(top, width=25)
        self.cancer_data_entry.grid(column=2, row=4)

        sumbit_button = Button(top, text="Submit", command=self.add_data)
        sumbit_button.grid(column=1, row=5)
        top.mainloop()

    def add_data(self):
        try:   
            LungCancerCursor = self.LungCancerConnection.cursor()
            AirPollutionCursor = self.AirPollutionConnection.cursor() 

            city = self.city_entry.get()   # get city
            date_str = self.date.get_date() # get date
            date_obj = datetime.strptime(date_str, '%m/%d/%y')  # create the format for SQL Server
            formatted_date = date_obj.strftime('%Y-%m-%d')  # finally format the date
            pm25 = self.pm_25_entry.get()

            query = "INSERT INTO BatonRouge2 (City, Date, PM25) VALUES (?, ?, ?)"  # corrected the query syntax
            AirPollutionCursor.execute(query, (city, formatted_date, pm25))  # added comma to separate query and tuple
            self.AirPollutionConnection.commit()

            #TODO Add way to add Cancer #'s to db

            print("New Data added successfully")
        except Exception as e:
            print("Error adding new data:", e)

if __name__ == "__main__":
    login_page = LoginPage()
    login_page.mainloop()

