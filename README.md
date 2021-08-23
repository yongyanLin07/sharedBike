# About the Project
![Bike Rental Homepage](./static/images/homepage.png?raw=true "Bike Rental Homepage")

This is the LAB_01_2k's implementation of the E2E Bike Sharing Application Team Project. This application serves as a pltform for users to rent a bike from one of the many available locations acorss the city and effortlessly return it at any location without any hassels, and for operators and managers to carry out administrative and business related tasks from one easy to access web portal.

## Technology Stack
The web application is built using following framework technologies to support application functionality:
- [Flask](https://flask.palletsprojects.com/en/1.1.x/)
- [SQLite](https://www.sqlite.org/index.html)
- [Bootstrap](https://getbootstrap.com/)

# Getting Started
This web-application is accessed locally on the user’s system by unpacking the project files in a project directory and running the main application file through Python 3 interpreter.

## Prerequisites
This application relies on certain external python libraries to work correctly and to enhance the user experience which are as detailed below and in the “requirements.txt” file that comes bundled with the application:
- flask
- sqlalchemy
- flask_sqlalchemy
- flask_login
- werkzeug
- pandas
- plotly
- stripe

## Installation
After copying all the files in a project directory, run the following command either in windows command prompt (where python and pip are recognized as valid commands) or through Anaconda prompt:
```
pip install -r requirements.txt
```
Running the above command would install all the required libraries for this application.

## Run Application
Once the libraries are installed, following command can be used to run the server from the same command window as previously used:
```
python app.py
```
Alternatively, the application can also be run in an IDE like spyder3 by opening app.py in the IDE and running after the requirements are installed. 

# Usage
Once successfully started, opening http:// localhost:8000 in a web browser would open the login page with username and password text boxes. Following usernames and passwords come default with the application for each role:

| Username | Password | Role |
| ------ | ------ | ------ |
| user | user | Customer |
| admin | admin | Manager |
| operator | operator | Operator |

To close the web-application and shut down the server, press *CTRL+C* in the terminal that is running the web server.

## Features
### Basic Functionality
Application has implemented following basic functionalities for each role:
- Customer
  - Rent a bike from any available location.
  - Return a bike to any location.
  - Report a bike as defective.
  - Pay any charge on the account.
- Operator
    - Track location and status of all bikes.
    - Repair a defective bike.
    - Move bikes to different locations in the city.
- Manager
    - Generate different types of reports.

### Advanced Functionality
Application has implemented following complex functionalities for each role:
- Customer
  - Upload image of the defective bike while reporting.
  - Recharge wallet by card.
  - Pay for the bike rental by card.
  - As a fraud prevention measure, customer cannot rent a new bike without paying for the earlier ride.
- Operator
    - Retreive defective bike image while working on the report.
- Manager
    - Add a new location.
    - Add a new bike.
    - Approve or reject a defective bike report.
    - Create a bike transfer request task.
    - Assign defective bike report/bike transfer task to operator.
    - Create a new customer/operator.

# Acknowledgements
- [Guide to README](https://github.com/othneildrew/Best-README-Template)
- [Plotly for Interactive HTML Charts](https://plotly.com/python/interactive-html-export/)
- [Stripe API for Python](https://github.com/stripe/stripe-python)