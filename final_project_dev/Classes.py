from flask import Flask, render_template, jsonify, request, redirect, url_for, session, g, flash
import MySQLdb
import time
from datetime import datetime

##############################################################
			#Reservation#
##############################################################

class Reservation:
	def __init__(self):
		self.reservation_id = ""
		self.flight_id = ""
		self.user_id = ""
		self.billing_id = ""
		self.timestamp = ""
		self.reservation_seat = ""
		self.reservation_total = ""

	def getReservations(self,user):
		try:
			user.connectAsRead()
			sql = "SELECT * FROM Reservation"
			user.cursor.execute(sql)
			data = user.cursor.fetchall()
			print("-----------------------------")

			return data
		except:
			return "ERROR"

	def addReservation(self,user):
		try:
			user.connectAsInsert()
			print("-----------------------------")
			sql = "INSERT INTO Reservation (flight_id,user_id,billing_id,reservation_seat,reservation_total)VALUES ('%s','%s','%s','%s','%s')" % (self.flight_id,self.user_id,self.billing_id,self.reservation_seat,self.reservation_total)
			print(sql)
			user.cursor.execute(sql)
			user.conn.commit() #Commit ALL changes to DB

			sql = "SELECT reservation_id FROM Reservation WHERE `user_id`='"+self.user_id+"'ORDER BY timestamp DESC"
			print("-----------------------------")
			print(sql)
			user.cursor.execute(sql)
			data = user.cursor.fetchall()
			print(data[0][0])
			print("-----------------------------")

			return data[0][0]
		except:
			return "ERROR"




##############################################################
                        #Billing#
##############################################################
class Billing:
	def __init__(self):
		self.billing_id = ""
		self.user_id = ""
		self.billing_card_num = ""
		self.billing_card_expr = ""
		self.billing_card_csv = ""
		self.billing_firstname = ""
		self.billing_lastname = ""
		self.billing_address = ""
		self.billing_city = ""
		self.billing_state = ""
		self.billing_zip = ""

	def getBillingPerUser(self,user):
		try:
			user.connectAsRead()
			print("-----------------------------")		
			sql = "SELECT * FROM Billing WHERE `billing_id`='" + user.uid + "'"
			print (sql)
			self.cursor.execute(sql)
			data = user.cursor.fetchall()
			print(data)
			print("-----------------------------")		

			return data
		except:
			return "ERROR"	

	def addBilling(self,user):
		try:
			user.connectAsInsert()
			print("-----------------------------")
			sql = "INSERT INTO Billing (user_id,billing_card_num,billing_card_expr,billing_card_csv,billing_firstname,billing_lastname,billing_address,billing_city,billing_state,billing_zip) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (self.user_id,self.billing_card_num,self.billing_card_expr,self.billing_card_csv,self.billing_firstname,self.billing_lastname,self.billing_address,self.billing_city,self.billing_state,self.billing_zip)
			print(sql)
			user.cursor.execute(sql)
			user.conn.commit() 

			sql = "SELECT billing_id FROM Billing WHERE `user_id`='"+self.user_id+"'ORDER BY billing_timestamp DESC"
			print("-----------------------------")
			print(sql)
			user.cursor.execute(sql)
			data = user.cursor.fetchall()
			print(data[0][0])
			print("-----------------------------")
	
			return data[0][0]
		except:
			return "ERROR"

##############################################################
			#Option#
##############################################################
class Option:

	def __init__(self):
		self.option_id = ""
		self.option_name = ""
		self.option_price = ""

	def getOption(self,user,option_id):
		try:
			user.connectAsRead()
			sql = "SELECT * FROM Options WHERE `option_id`='" + str(option_id) + "'"
			print("--------------------------------")
			print(sql)
			user.cursor.execute(sql)
			data = user.cursor.fetchall()
			print(data)
			print("--------------------------------")
			return data
		except:
			return "ERROR"



	def getAllOptions(self,user):
		try:
			user.connectAsRead()
			sql = "SELECT * FROM Options"
			print("--------------------------------")
			print(sql)
			user.cursor.execute(sql)
			data = user.cursor.fetchall()
			print(data)
			print("--------------------------------")
			return data	
		except:
			return "ERROR"

	def addUserOption(self,user,reservation_id,option_id):
		try:
			user.connectAsInsert()
			print("--------------------------------")
			sql = "INSERT INTO Option_List (reservation_id,option_id) VALUES ('%s','%s')" % (reservation_id,option_id)
			print(sql)	
			user.cursor.execute(sql)
			user.conn.commit() #Commit changes to DB
			print("--------------------------------")
			
			return "Success"
		except:
			return "ERROR"

	

##############################################################
			   #User#
##############################################################
class User:
	def __init__(self,database,port):
		self.uid = str(session.get('user_id'))
		self.email =  str(session.get('username'))
		self.password = ""
		self.phone = ""
		self.created = ""
		self.conn = ""
		self.cursor = ""
		self.database = database
		self.port = int(port)

		self.connectAsRead() #Initialize as read-only user


	#Establish DB connection
	def connect2db(self,dbuser,password):
		conn = MySQLdb.connect(host=self.database,
			port = self.port,
			user = dbuser,
			passwd = password,
			db = "MaristAir")
		cursor = conn.cursor()
		self.conn = conn
		self.cursor = cursor
		return cursor, conn

	#Connect as a read-only user
	def connectAsRead(self):
		self.connect2db("readuser","readuser1")
	#Connect as a insert/update user
	def connectAsInsert(self):
		self.connect2db("insertuser","insertuser1")


	#Account Login Function
	def userLogOut(self):
		session['username'] = None
		session['user_id'] = None
		session['logged_in'] = False
		return "Logged out"


	def userLogin(self,email,password):
		try:
			self.connectAsRead()
			sql = "SELECT user_id, user_email, user_password FROM User WHERE `user_email`='" + email + "'"
			print("--------------------------------")
			print(sql)
			self.cursor.execute(sql)
			data = self.cursor.fetchall()
			print("DB data:" + str(data))	
			print("User data: " + email + ", " + password) 
			print("--------------------------------")
			if not data: 
				return "ERROR: Account does not exist!"

			else:
				# data[0][0] = user_id
				# data[0][1] = email	
				# data[0][2] = password	

				returnedPassword = data[0][2] 
				if (password == returnedPassword):
					session['username'] = email
					session['user_id'] = data[0][0]
					session['logged_in'] = True
					print("Successfully logged in as: " + email)
					return "Successfully logged in as: " + email

				else:
					session['username'] = None
					session['user_id'] = None
					session['logged_in'] = False
					print("ERROR: Invalid credentials, try again")
					return "ERROR: Invalid credentials, try again"
				

		except:
			print("ERROR: Failed to login.")
			return "ERROR: Failed to login."


	#Account Creation Function
	def createAccount(self, email, password, phone):
		try:
			#Basic error checking on input fields
			if email == "":
				return "ERROR: Email is empty!"
			if phone == "":
				return "ERROR: Phone is empty!"
			if password == "":
				return "ERROR: Password is empty!"


			#Check if email already exists in DB	
			sql = "SELECT user_email FROM User WHERE `user_email`='" + email + "'"
			print("--------------------------------")
			print (sql)
			check = self.cursor.execute(sql) #Execute sql command
			print ("Exists?:" + str(check))
			print("--------------------------------")
			if not check: 
				self.connectAsInsert()
				print("--------------------------------")
				sql = "INSERT INTO User (user_email,user_password,user_phone) VALUES ('%s','%s','%s')" % (email,password,phone)
				print (sql)
				self.cursor.execute(sql)		
				self.conn.commit() #Commit changes to DB
				print("Successfully created user: " + email)
				print("--------------------------------")
				return "Successfully created user: " + email
			else:
				return "ERROR: User already exists! Please use a different email."

		except:
			return "ERROR: Failed to create user account."



##############################################################
			   #City#
##############################################################
class City:

	def __init__(self):
		self.city_id = ""
		self.city_name= ""		
		self.city_state = ""
		self.city_lat = ""
		self.city_long = ""


	def getAllCities(self,user):
		try:
			sql = "SELECT * FROM City"
			print("-----------------------------")
			print(sql)
			user.cursor.execute(sql)
			data = user.cursor.fetchall()
			print(data)	
			print("-----------------------------")
			return data
		except:
			return "ERROR"




##############################################################
			   #Plane#
##############################################################
class Plane:


	def __init__(self):
		self.plane_id = ""
		self.airline_id = ""
		self.airline_name = ""
		self.plane_model = ""
		self.plane_seats = ""

	def getAllPlanes(self,user):
		try:
			#sql = "SELECT * FROM Plane"
			sql = "SELECT plane_id,Plane.airline_id,plane_model, plane_seats,airline_name FROM Plane INNER JOIN Airline ON Plane.airline_id=Airline.airline_id"
			print("-----------------------------")
			print(sql)
			user.cursor.execute(sql)
			data = user.cursor.fetchall()
			print(data)
			print("-----------------------------")
			return data		
		except:
			return "ERROR"

##############################################################
			   #Flight#
##############################################################
class Flight:
	def __init__(self):
		self.flight_id = ""
		self.flight_source_city = ""
		self.flight_source_gate = ""
		self.flight_dest_id = ""
		self.flight_dest_gate = ""
		self.flight_rem_seats = ""
		self.flight_depart = ""
		self.flight_arrive = ""
		self.flight_base_price = ""
		self.plane_id = ""
		self.airline_id = ""
		self.plane_model = ""
		self.plane_seats = ""
		self.airline_name = "" 
		self.source_id = ""
		self.source_name = ""
		self.source_state = ""
		self.source_lat = ""
		self.source_long = ""
		self.dest_id = ""
		self.dest_name = ""
		self.dest_state = ""
		self.dest_lat = ""
		self.dest_long = ""

	def getSeat(self,user,flight_id):
		try:
			user.connectAsInsert()
			print("-----------------------------")
			sql = "SELECT flight_rem_seats FROM Flight WHERE `flight_id`='" + str(flight_id) + "'"
			print (sql)
			user.cursor.execute(sql)
			data = user.cursor.fetchall()
			print(data)
			print("-----------------------------")
			seat = data[0][0]
			sql = "UPDATE `MaristAir`.`Flight` SET `Flight`.`flight_rem_seats` = `Flight`.`flight_rem_seats` - 1 WHERE (`Flight`.`flight_rem_seats` > 0) AND (`Flight`.`flight_id`='"+str(flight_id)+"')"
			print(sql)
			user.cursor.execute(sql)
			user.conn.commit()
			print("-----------------------------")	

			return seat

		except:
			return "ERROR"


	def getBasePrice(self,user,flight_id):
		try:
			user.connectAsRead()
			print("-----------------------------")
			sql = "SELECT flight_base_price FROM Flight WHERE `flight_id`='" + str(flight_id) + "'"
			print (sql)
			user.cursor.execute(sql)
			data = user.cursor.fetchall()
			print(data)
			print("-----------------------------")

			return data[0][0]
		except:
			return "ERROR"



	#Retrieve JOINED table with flight, plane, city, and airline info
	def getAllFlightsData(self,user):
		try:

			#Sub-queries to get each table to join

			f = "(SELECT * FROM Flight) as f,"
			p = "(SELECT plane_id,Plane.airline_id,plane_model, plane_seats,airline_name FROM Plane INNER JOIN Airline ON Plane.airline_id=Airline.airline_id) as p,"
			s = "(SELECT city_id AS source_id, city_name AS source_name, city_state AS source_state, city_lat AS source_lat, city_long AS source_long FROM City) as s,"
			d = "(SELECT city_id AS dest_id, city_name AS dest_name, city_state AS dest_state, city_lat AS dest_lat, city_long AS dest_long FROM City) as d"

			#Full sql query to join flight,plane/airline, and city tables
			sql ="SELECT * FROM (" +f + p + s + d +" ) WHERE (f.flight_source_city=s.source_id AND f.flight_dest_city=d.dest_id AND f.plane_id=p.plane_id)"
	
			print("-----------------------------")
			print(sql)
			user.cursor.execute(sql)
			data = user.cursor.fetchall()
			print(data)
			print("-----------------------------")
			return data
		except:
			return "ERROR"

	
	#Add Flight Insert SQL
	def addFlight(self,user):

		try:
			nested = "(SELECT plane_seats FROM Plane WHERE `plane_id`='"+self.plane_id+"')"
			user.connectAsInsert()
			sql = "INSERT INTO Flight (flight_source_city,flight_source_gate,flight_dest_city,flight_dest_gate,flight_rem_seats, flight_depart, flight_arrive, flight_base_price, plane_id) VALUES ('%s','%s','%s','%s',%s,'%s','%s','%s','%s')" % (self.flight_source_city, self.flight_source_gate, self.flight_dest_city, self.flight_dest_gate, nested, self.flight_depart, self.flight_arrive, self.flight_base_price, self.plane_id)	

			print(sql)

			user.cursor.execute(sql)
			user.conn.commit()		

			return "Successfully added flight to DB"

		except:
			return "ERROR: Unable to commit to DB"



