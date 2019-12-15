

#MaristAir Cloud Project

##-- Introduction --

This project is a simple airline reservation web application to allow users to schedule flights at an airport. The goal of this project is to showcase a hybrid cloud environment using a real-world example most people have used. There are a few entities to consider regarding booking a flight at an airport:

- User (that's you!)
- Admin (that's me)
- Airport hosting the application (IBM and AWS in this case) 

Some things you, the user, will want:
- Check flight's that are available to different cities
- Create an account
- Book flights

The admin will want to configure:
- Add new flights
- See who made reservations
- Set a target database for information to be stored in

The airport will want to have all the above operational for users at any given time, so they will host their service on a cloud provider for the benefits of constant uptime and scalability.


##-- User Interface --
The airline application interface is supported using python-flask web framework. This python code exposes the functions that are expected by the stackholders above:

1. index.html - homepage consisting of links to other pages.
2. createAccount - creates a user account based on email, telephone, and password
2. login - creates a session for a user if it was created
3. logout - terminates the session for the user
4. reservation - allows a user to see flights available and make reservation and payment
5. addFlight - allows an admin to create new flight listings
6. changeDatabase - allows an admin to set the database target for ONLY the current runtime of this instance
7. listing - allows an admin to view all reservations that have been made. 


##-- Data Storage --
The application must save the information somewhere! This is done using a pre-configured MySQL database and making SQL calls to it using python's MySQLDB libraries. The exciting part of this project is the databases for each instance are configurable! For example, one database can hold information regarding all flights within the US. Another can hold flights just within the UK. Another can then hold international flights between the two countries. Since each database is targetable, multiple instances can be spawned for each.


##-- Cloud Hybridity --
Using one instance of the application will get the job done, but to truly benefit from cloud computing, it is essential to be able to run multiple containers. In this demo project, IBM Kubernetes and AWS ECS are used to each host an instance of MaristAir. Even better are these instances can be used to show off selectable database targeting per container!

Each instance is initially set to share a database. So for example, users on both platforms would see shared data. Now either of the running containers can be switched to another configured database at anytime, without a restart! This means that separate data is shown on both sites. This is useful for proving the application's use by a varity of independent organizations that do not want to share data.

Below is an image of deploying the application from a local environment to the multiple cloud providers:

![Architecture](https://raw.githubusercontent.com/jboniello/marist-mscs621-2019-boniello/master/docs/arch.PNG)



If interested, please see the README.md on the GitHub page for more detailed information!


