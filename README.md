### marist-mscs621-2019-boniello


# MaristAir Cloud Project

## -- Introduction --
This project is a simple airline reservation web application to allow users to schedule flights at an airport. The goal of this project is to showcase a hybrid cloud environment using a real-world example most people have used.

The application webpage is meant to be deployed across any number of cloud providers. It is able to integrate with any configured database target, allowing for data flexibility between application instances. As well, this provides options to run the applications in different public clouds and source a private on-premises database or another database in the cloud depending on what the airport needs.

For example, two airport proivders can run the same code, but have them configured to target their own private database. Another example is a single airport running multiple instances of the app for load-balancing, and having each configured to target a single central database.

The application is created using:

    Python-flask front end
    One or more MYSQL databases on the backend
    Python MySQLdb library used to pass SQL information between the two over TCPIP.


The main functions available to an airport administrator are:

        Set a Database target and port
        Add Flight entries to the targeted DB
        List reservations users have made

A general user would then have access to:

        Creating an account
        Making a reservation

For demo purposes all functions are available, and privilege level is denoted on the homepage. Additionally, two cloud app instances and databases are pre-configured for testing purposes.


#### Project Objective
From the course: *The objective is to learn how the native cloud applications can be developed and deployed into the hybrid cloud environment. Each student needs to set up and configure a hybrid cloud environment(IBM Cloud + other cloudand local cloud environment)and run a cloud application that is built by him/herself.*

The application deploys two separate instances of the python flask webpage app 'MaristAir' on IBM Cloud and AWS, and show  each are configurable within the cloud to target independent databases, as well as operate off a single shared database.

This exemplifies a hybrid cloud environment since many webpages are deployed accross different providers, and are configurable to target other public or private databases. Scalability is also acheived as more cloud databases and webpages could be configured as needed as user demand grows.

The ideal use of this application for a single company would have many webpages deployed within multiple clouds and target a private database for security.

#### Connectivity

For this project, there are two public webpages & databases that were configured for testing purposes. Connectivity information is as follows:

- ***Local Cloud:***
IP = http://127.0.0.1:5000
Valid DBs = ['db', maristairdb1, maristairdb2]

- ***IBM Cloud:***
IP = 173.193.92.200:31356
Valid DBs =  [maristairdb1, maristairdb2]

- ***AWS ECS:***
IP = http://3.80.195.167:5000
Valid DBs = [maristairdb1, maristairdb2]


*Database Info*

The maristairdb1 and maristairdb2 are the hostnames for the public databases. If testing this project, please use one of these on port 3306 (note, they are the same domain). 

- maristairdb1.ced3raw81xcn.us-east-1.rds.amazonaws.com
- maristairdb2.ced3raw81xcn.us-east-1.rds.amazonaws.com

The database 'db' is the name of the docker mysql5.7 image started in the same namespace as the local docker execution of my app using docker-compose. It is not available for public testing.



#### History
This project was originally developed as a proof-of-concept for a database course. The original intent was to interact on a localhost between the 127.0.0.1:5000 flask server and the local database instance using python's mysqldb libs. In order to configure the app for cloud deployment, three major changes were required:

- Change the MySQLDB database connection call to accept a configurable database IP and port
- Add in a webpage (changeDatabase) to allow an admin user to configure the database IP/port
- Change the html code to accept python-flask arguments passed based on the HOSTNAME of the cloud service, allowing for portability between providers. Ex: Links to Homepage should target the same cloud instance, not another IP or 127.0.0.1



## -- Dependencies --

1. **Configured MySQL Database**
  - Located in the 'db' folder are two configuration files:
      - MaristAirDBSQL.sql = initial table and user creation
      - MaristAir_Inserts.sql = populate tables with information on airlines, cities, options, and planes
  - A separate Database administrator would have to set this up outside of the application. This is because the app is supposed to target a customer database, which should be pre-built by them with whatever information that is relevant to their area (ex. Domestic-only airport vs International flights).

2. **Python3.6**
  - The application uses the python:3.6 image located within Dockerhub
  - Additional python dependencies are located in requirements.txt and include:
     - flask = the backbone of the application, creates the web interface
     - mysqlclient = the database interface libs to connect to a MySQL database

3. **Web Browser**
  - Interaction with the app, as well as initial setup on IBM Cloud and AWS require the use of a web browser.

4. **Docker**
  - Allows development of the python application in the local env to be pushed to Dockerhub. Both IBM and AWS will source this image: jboniello/maristair:1.0




## -- Deployment --

### *Local Environment*
The design was tested using the following setup:

        Windows 10 laptop
        Running VirtualBox + Vagrant using Ubuntu VM
        Docker to run a python 3.6 image
        Docker-compose also links to a docker mysql5.7 image to run a local database within the namespace called "db"

##### Docker commands
- docker build -t maristair:latest .
- docker tag maristair jboniello/maristair:1.0
- docker push jboniello/maristair:1.0
- [The Docker Compose Link](https://github.com/jboniello/marist-mscs621-2019-boniello/blob/master/final_project_dev/docker-compose.yml)
- docker ps
```
CONTAINER ID        IMAGE                   COMMAND                  CREATED             STATUS              PORTS                                NAMES
9adf41ce8c01        final_project_dev_app   "python app.py"          2 days ago          Up 27 hours         0.0.0.0:5000->5000/tcp               final_project_dev_app_1
b8993cabb27b        mysql:5.7               "docker-entrypoint.s…"   2 days ago          Up 27 hours         33060/tcp, 0.0.0.0:32000->3306/tcp   final_project_dev_db_1
```

##### Local Database Config:
- mysql --host='127.0.0.1' --port=32000 -u root -p < MaristAirDBSQL.sql
- mysql --host='127.0.0.1' --port=32000 -u root -p < MaristAir_Inserts.sql



### *Cloud Environments*

*Cloud services used:*
- Github to store source code (you are here!)
- Dockerhub image tested in the local setup was pushed to repository: jboniello/maristair:1.0
- IBM Cloud using Kubernetes Service was deployed via CLI tools (ibmcloud / kubectl) as learned in this class.
- AWS container was deployed using Amazon ECS (Elastic Container Service) using their webpage interface.
- AWS RDS services were also used to create 2 databases instances, since I need persistent databases for the demonstration.


#### IBM Deployment using Kubernetes:

Below are the commands used to deploy the docker image to IBM cloud and start the service using IBM Kubernetes. The ibmcloud and kubectl where pre-installed as part of the class (lab 5).

- ibmcloud login -a cloud.ibm.com -r us-south -g Default

- ibmcloud ks cluster config --cluster bnnrbbnd0cm3ttj81ivg   (Create this cluster on IBM's webpage)

- export KUBECONFIG=/root/.bluemix/plugins/container-service/clusters/bnnrbbnd0cm3ttj81ivg/kube-config-hou02-maristair_cluster.yml

- kubectl run maristairdeploy --image=docker.io/jboniello/maristair:1.0

- kubectl expose deployment/maristairdeploy --type=NodePort --name=maristairservice --port=80 --target-port=5000


- kubectl get services
 ```
 NAME               TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
  kubernetes         ClusterIP   172.21.0.1      <none>        443/TCP          4d10h
  maristairdeploy    NodePort    172.21.149.0    <none>        5000:31356/TCP   4d9h
  maristairservice   NodePort    172.21.119.11   <none>        80:31645/TCP     4d9h
```
- kubectl describe service maristairdeploy
```
  Name:                     maristairdeploy
  Namespace:                default
  Labels:                   run=maristairdeploy
  Annotations:              <none>
  Selector:                 run=maristairdeploy
  Type:                     NodePort
  IP:                       172.21.149.0
  Port:                     <unset>  5000/TCP
  TargetPort:               5000/TCP
  NodePort:                 <unset>  31356/TCP
  Endpoints:                172.30.109.135:5000
  Session Affinity:         None
  External Traffic Policy:  Cluster
  Events:                   <none>
```

External IP is accessed by the nodeport: http://173.193.92.200:31356
By default, the application is setup to use the database found on  maristairdb1.ced3raw81xcn.us-east-1.rds.amazonaws.com:3306



#### AWS Delpoyment using ECS

- Create a default cluster: https://console.aws.amazon.com/ecs/home?region=us-east-1#/clusters
- Create a container: https://console.aws.amazon.com/ecs/home?region=us-east-1#/firstRun
    - Amazon makes it simple by selecting the "custom" option
    - Give the container a name, enter the dockerhub image 'jboniello/maristair:1.0" , and set port to 5000
- Give the container a VPC and configure network rules to allow all Inbound/OutBound connections (0.0.0.0/0)
- Screenshots of webpages are located in screenshot folder
- Run a task using the container, and get the IP and port (Screenshot = AWSrunningTaskContainer.PNG)


External IP is accessed by: IP = http://3.80.195.167:5000
By default, the application is setup to use the database found on  maristairdb1.ced3raw81xcn.us-east-1.rds.amazonaws.com:3306


#### Database Config

The two cloud database instances were created using AWS RDS (relational database service). Creation is easy, as MySQL 5.7 is a selectable option.

The important configuration steps are: 
- Assign the name
- Select MySQL5.7
- Select other options like storage capacity
- Assign VPC to allow public routable IP configuration

Once initialized, a database admin can use the MySQL command line to initialize the database. The pre-configured databases for this project are shown below:

**maristairdb1**
-  mysql -u admin -p -h maristairdb1.ced3raw81xcn.us-east-1.rds.amazonaws.com -P 3306 < MaristAirDBSQL.sql
- mysql -u admin -p -h maristairdb1.ced3raw81xcn.us-east-1.rds.amazonaws.com -P 3306 < MaristAir_Inserts.sql

** maristairdb2**
- mysql -u admin -p -h maristairdb2.ced3raw81xcn.us-east-1.rds.amazonaws.com -P 3306 < MaristAirDBSQL.sql
- mysql -u admin -p -h maristairdb2.ced3raw81xcn.us-east-1.rds.amazonaws.com -P 3306 < MaristAir_Inserts.sql


## -- Architecture --

Below is the image of the project design architecture + deployment. Additionally, the database ERD is shown.


**Architecture**<br>

![Architecture](https://raw.githubusercontent.com/jboniello/marist-mscs621-2019-boniello/master/docs/arch.PNG)


**Database Entity Relationship Diagram**<br>
![Database ERD](https://raw.githubusercontent.com/jboniello/marist-mscs621-2019-boniello/master/docs/Database/ERD_MaristAir.JPG)



## -- Interaction and API--

Users interact with this application entirely through GET and POST requests to the host. 

*All pages are accessed in the following method*

  http:// hostip:port/pageName

where hostip and port are dependent on which cloud instance a user is accessing (local vs IBM vs AWS)

***IBM***
http://173.193.92.200:31356/index.html
<br>
***AWS***
http://3.80.195.167:5000/index.html
<br>
***Local***
http://127.0.0.1:5000/index.html
<br>

PageNames:
1. index.html - homepage consisting of links to other pages.
2. createAccount - creates a user account based on email, telephone, and password
2. login - creates a session for a user if it was created
3. logout - terminates the session for the user
4. reservation - allows a user to see flights available and make reservation and payment
5. addFlight - allows an admin to create new flight listings
6. changeDatabase - allows an admin to set the database target for ONLY the current runtime of this instance
7. listing - allows an admin to view all reservations that have been made.

*Note -- reference to HTML includes: html, javascript (js), and CSS for ease of reading*

#####  APIs
**/ or /index.html**

*-GET requests-*
- Returns HTML with links to the other method webpages. This page will also display status returned by the server if coming from another page (i.e after a reservation)

<br>

**/createAccount**

*-GET requests-*
- Returns HTML containing an input form containing the fields: email, phone, password1, password2

*-POST requests-*
<br>
Accepts:
  - email -- string, will be user account name
  - phone -- string, additional contact point
  - password1 -- string, user password
  - password2 -- string, user password again

Action:
    Server will check if user email exists already, and if the password1 and password2 are matching. Server will attempt to create account in "User" table within targeted database and return status back to user.

<br>

**/login**

*-GET requests-*
- Returns HTML containing an input form containing the fields: email, password

*-POST requests-*
<br>
Accepts:
- email -- string, user account
- password -- string, user password

Action:
    Server will attempt to login to webpage by checking credentials against the information entered into Database during the createAccount step.
    
<br>

**/logout**

*-GET requests-*
- Returns user to index.html and removes session credentials

<br>

**/addFlight**

*-GET requests-*
<br>
  Returns HTML with a form containing the following fields:
- sourceCity -- selectable, predefined list of cities. Fetched from DB
- depart -- string , will be used to create datetime object in database for departure time
- departGate -- string, departure gate at airport
- destCity -- selectable, predefined list of cities. Fetched from DB
- arrive -- string , will be used to create datetime object in database for arrival time
- arriveGate -- string, arrival gate at airport
- plane -- selectable, predefined list of valid planes. Includes plane ID, airline, and plane type (ex: Plane #4, JetBlue, A320). Fetched from DB
- price -- string, defines base price of a flight before add-on options

*-POST requests-*
<br>
  Accepts:
   - sourceCity, depart, departGate, destCity, arrive, arriveGate, plane, price
   
Action:
    Server takes input fields, maps them into SQL command, and inserts entry to the "Flight" table in the target database.

<br>

**/reservation**

*-GET requests-*
- Retrieves all current flight listings from the database, as well as available options, and displays them for the user. Additionally will check if user is signed in, and if so will ask them to make a flight selection and add in billing information to the HTML form.

*-POST requests-*
<br>
  Accepts:
  
   - flight -- string, the flight ID of the selected flight in the list
   - billingCardNum -- string, credit card number
   - billingCardDate -- string, credit card expiration date. Converted to datetime object on server
   - billingCardCSV -- string, credit card special code on back
   - billingCardFirst -- string, first name
   - billingCardLast -- string, last name
   - billingCardStreet -- string, street address
   - billingCardCity -- string, city
   - billingCardState -- string, state
   - billingCardZip -- string, zip code of city
   - option1, option2, optionN -- option 1 through N are based on available options, retieved during GET. The POST requests accepts the option as a string in form 'optionX', based on the checklist from GET.

  Action:
  - Server will create a reservation ID based on user inputs for flight selection, available options, and billing info. Errors will be returned if any of the options are invalid, or if a credit card is not a valid number.
  - A seat number is assigned based on remaining seats available (based on plane defined by database admin).
  - The total cost of the flight is added based on base price + options.
  - The reservation is assigned a reservation_id, and an entry is submitted to the database

  *Note -- user ID is retrieved for the session based on the login operation*

<br>

**/listing**

*-GET requests-*
  <br>
Retrieves the list of reservations from the table in database, and displays them for an admin user. The list includes:

- reservation_id -- primary key for a reservation
- flight_id -- link to flight_id from Flight table
- user_id -- link to user_id from User table
- billing_id -- link to a billing_id account from Billing table
- timestamp -- creation date of the reservation
- reservation_seat -- seat on the plane
- reservation_total -- total cost for the reservation

<br>

**/changeDatabase**

*-GET requests-*
 - Returns the currently set database target IP address and Port number. As well, returns an HTML form to change the current target IP and Port.

*-POST requests-*
<br>
  Accepts:
- databaseHost -- string, the IP address of the new database target
- databasePort -- string, the Port number of the new database target

Action:
    Will set the application runtime code to use the new IP and Port within the MySQLDB calls.



