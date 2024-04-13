# CancerAndPM2.5Analysis
This application provides a visual representation of air quality data for different locations in Louisiana. It allows users to select specific coordinates on a map or input coordinates manually to retrieve air quality information. The data is fetched from a SQL Server database named "AirPollution".

Required Packages
tkinter
PIL (Python Imaging Library)
pyodbc
pip install tkinter pillow pyodbc

How to Use
Opening the Application:

Run the Python script (LouisianaAirPollution.py) to launch the application.
Viewing the Map:

Upon launching, a window will appear displaying the map of Louisiana.
Select Coordinates:

Click on Map: Click anywhere on the map to select coordinates. A red marker will indicate the selected location.
Manual Input: Alternatively, you can manually enter coordinates in the input box provided. Press Enter or click the "Search" button to fetch data for the entered coordinates.
Coordinate Bank: You can select coordinates from the list of available coordinates displayed in the "Available Coordinates" section. Click on a coordinate in the list to populate the input box with the selected coordinates. Press Enter or click the "Search" button to fetch data for the selected coordinates.
View Air Quality Data:

After selecting or entering coordinates, the application will fetch air quality data corresponding to those coordinates. The fetched data will be displayed in the labeled fields for CO2, PM2.5, PM10, Temperature, and Humidity.
Adding New Data:

To add new data to the database, first select or enter the coordinates for the location where the data will be added.
Enter the new data values for CO2, PM2.5, PM10, Temperature, and Humidity in the provided input fields.
Click the "Add New Data" button to insert the new data into the database. The list of available coordinates will be updated accordingly.
Clear Entries:

Use the "Clear" button to clear all entries in the input fields for coordinates and air quality data.
Closing the Application:

Close the application window to exit the program.
