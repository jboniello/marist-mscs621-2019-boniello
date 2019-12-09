from flask import Flask, render_template, jsonify, request, redirect, url_for, session, g, flash
import MySQLdb
from datetime import timedelta
from datetime import datetime
import time
import json
import re
from functools import wraps
from Classes import User
from Classes import City
from Classes import Flight
from Classes import Plane
from Classes import Reservation
from Classes import Option
from Classes import Billing

app = Flask(__name__)
app.secret_key = "thisisasecret"
dbHost = "maristairdb1.ced3raw81xcn.us-east-1.rds.amazonaws.com"
dbPort = "3306"


@app.route('/')
@app.route('/index.html')
def homepage():
    return render_template("index.html")


@app.route("/createAccount", methods=['GET', 'POST'])
def createAccount():
	if request.method == "POST":

		email = request.form["email"]
		phone = request.form["phone"]
		password1 = request.form["password1"]
		password2 = request.form["password2"]

		#Password check
		if password1 != password2:
			flash("Error: Passwords do not match. Please re-enter")
			return render_template("createAccount.html")

		user = User(dbHost, dbPort) #instantiate user class

		status = user.createAccount(email,password1, phone)
		flash(status)
		return render_template("createAccount.html")
	else:
		return render_template("createAccount.html")


@app.route('/logout')
def logout():
	user = User(dbHost,dbPort)
	status = user.userLogOut()
	flash(status)
	return redirect("/")	

@app.route("/login", methods=['GET', 'POST'])
def login():
	if request.method == "POST":
		user = User(dbHost,dbPort)
		status = user.userLogin(request.form["username"],request.form["password"])
		flash(status)
		return redirect("index.html")

	else:
		return render_template("login.html")


@app.route("/addFlight", methods=['GET', 'POST'])
def addFlight():
	user = User(dbHost,dbPort)
	if request.method == "POST":
		flight = Flight()
		flight.flight_source_city = request.form.get("sourceCity")
		flight.flight_depart = request.form["depart"]
		flight.flight_source_gate = request.form["departGate"]
		flight.flight_dest_city = request.form.get("destCity")
		flight.flight_arrive = request.form["arrive"]
		flight.flight_dest_gate = request.form["arriveGate"]
		flight.plane_id = request.form.get("plane")
		flight.flight_base_price = request.form["price"]

		status = flight.addFlight(user) 
		print(status)
		flash(status)
		#return redirect("addFlight")
		return redirect("addFlight")
	else:
		city_list = []
		cities = City()
		cities = cities.getAllCities(user)

		#Create a list with all cities
		for i in range(0,len(cities)):
			city = City()
			city.city_id = cities[i][0]
			city.city_name = cities[i][1]
			city.city_state = cities[i][2]
			city.city_lat = cities[i][3]
			city.cit_long = cities[i][4]

			city_list.append(city)


		plane_list = []
		planes = Plane()
		planes = planes.getAllPlanes(user)

		for j in range(0,len(planes)):
			plane = Plane()
			plane.plane_id = planes[j][0]
			plane.airline_id = planes[j][1]	
			plane.plane_model = planes[j][2]
			plane.plane_seats = planes[j][3]
			plane.airline_name = planes[j][4] 			

			plane_list.append(plane)

		return render_template("addFlight.html", city_list=city_list, plane_list=plane_list)


@app.route("/reservation", methods=['GET', 'POST'])
def reservation():
	user = User(dbHost,dbPort)
	print ("USER: " + user.email)
	if request.method == "POST":
		reservation = Reservation()
		
		#Get flight id from user
		reservation.flight_id = request.form.get("flight")

		#Get user_id from session
		reservation.user_id = user.uid


		#Get Base Price of flight
		flight = Flight()
		reservation.reservation_total = float(flight.getBasePrice(user,reservation.flight_id))

		#Establish billing
		billing = Billing()
		billing.user_id = user.uid 
		billing.billing_card_num = request.form["billingCardNum"]
		billing.billing_card_expr = datetime.strftime((datetime.strptime(request.form["billingCardDate"], '%m/%y')), "%Y-%m-%d")
		print(billing.billing_card_expr)
		billing.billing_card_csv = request.form["billingCardCSV"]
		billing.billing_firstname = request.form["billingCardFirst"]
		billing.billing_lastname = request.form["billingCardLast"]
		billing.billing_address = request.form["billingCardStreet"]
		billing.billing_city = request.form["billingCardCity"]
		billing.billing_state = request.form["billingCardState"]
		billing.billing_zip = request.form["billingCardZip"]

		status = billing.addBilling(user)
		if(status == "ERROR"):
			flash("ERROR: Problem adding payment method")
			return redirect("/") 	

		else:
			#Set reservation.billing_id after creating the billing above
			reservation.billing_id = status	

		#Get User selected options
		option_list = []
		option_total = 0.0
		for i in range(1,7):	
			opt_id = request.form.get("option"+str(i))
			#print("opt_id: " + str(opt_id))
			if(opt_id != None):
				option = Option()	
				data = option.getOption(user,opt_id)
				option.option_id = data[0][0]
				option.option_name = data[0][1]
				option.option_price = data[0][2] 
				
				#Set option total based on each option proce
				option_total = option_total + float(option.option_price)

				option_list.append(option)

		#Set new total based on base + option price
		reservation.reservation_total = reservation.reservation_total + float(option_total)	
		#Calculate seat position based on remaining seats available
		reservation.reservation_seat=flight.getSeat(user,reservation.flight_id)

		#Add reservation
		reservation.reservation_id =reservation.addReservation(user)

		flash("Your reservation ID is: " + str(reservation.reservation_id))

		#Add options selected to option list
			

		for i in range(0,len(option_list)):
			option.addUserOption(user,reservation.reservation_id,option_list[i].option_id)

		return redirect("/")






	else:

		flight_list = []
		flights = Flight()
		flights = flights.getAllFlightsData(user)

		for i in range(0,len(flights)):
			flight = Flight()

			flight.flight_id = flights[i][0] 
			flight.flight_source_city = flights[i][1] 
			flight.flight_source_gate = flights[i][2] 
			flight.flight_dest_id = flights[i][3] 
			flight.flight_dest_gate = flights[i][4] 
			flight.flight_rem_seats = flights[i][5] 
			flight.flight_depart = flights[i][6] 
			flight.flight_arrive = flights[i][7] 
			flight.flight_base_price = flights[i][8] 
			flight.plane_id = flights[i][9] 
			#flights[i][10] - duplicate (plane_id)
			flight.airline_id = flights[i][11]
			flight.plane_model = flights[i][12]
			flight.plane_seats = flights[i][13]
			flight.airline_name = flights[i][14]
			#flights[i][15] - duplicate (source_id)
			flight.source_name = flights[i][16]
			flight.source_state = flights[i][17]
			flight.source_lat = flights[i][18]
			flight.source_long = flights[i][19]
			#flights[i][20] - duplicate (dest_id) 
			flight.dest_name = flights[i][21]
			flight.dest_state = flights[i][22]
			flight.dest_lat = flights[i][23]
			flight.dest_long = flights[i][24]

			flight_list.append(flight)

		option_list = []
		options = Option()
		options = options.getAllOptions(user)

		for i in range(0,len(options)):
			option = Option()

			option.option_id = options[i][0]
			option.option_name = options[i][1]
			option.option_price = options[i][2]
		
			option_list.append(option)	




		return render_template("reservation.html", user=user,flight_list=flight_list,option_list=option_list)


@app.route("/listing", methods=['GET', 'POST'])
def listing():
	user = User(dbHost,dbPort)
	reservation = Reservation()
	reservations = reservation.getReservations(user)
	listing_list = []
	for i in range(0,len(reservations)):
	        listing	= Reservation()
	        listing.reservation_id = reservations[i][0]	
	        listing.flight_id = reservations[i][1]	
	        listing.user_id = reservations[i][2]	
	        listing.billing_id = reservations[i][3]	
	        listing.timestamp = reservations[i][4]	
	        listing.reservation_seat = reservations[i][5]	
	        listing.reservation_total = reservations[i][6]	
	        listing_list.append(listing)

	return render_template("listing.html",dbHost=dbHost,dbPort=dbPort,listing_list=listing_list)

@app.route("/changeDatabase", methods=['GET', 'POST'])
def changeDatabase():
	global dbHost
	global dbPort
	if request.method == "POST":

		newHost = request.form["databaseHost"]
		newPort = request.form["databasePort"]
		dbHost = newHost
		dbPort = newPort

	#	user = User() #instantiate user class

	#	status = user.createAccount(email,password1, phone)
		flash(newHost+""+newPort)
		return render_template("changeDatabase.html",dbHost=dbHost,dbPort=dbPort)
	else:

		#dbHost=dbHost
		#dbPort=dbPort
		return render_template("changeDatabase.html",dbHost=dbHost,dbPort=dbPort)






if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host='0.0.0.0')
