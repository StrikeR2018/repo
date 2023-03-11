from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os

# Configuration

app = Flask(__name__)

app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
app.config["MYSQL_USER"] = "cs340_osuid"
app.config["MYSQL_PASSWORD"] = "password"
app.config["MYSQL_DB"] = "cs340_osuid"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

# Routes 

@app.errorhandler(500)
def internal_error(e):
     #return a custom error to our user to explain why they might have got it.
     return render_template('500.html')

@app.route("/")
def index():
    return render_template("index.j2")

@app.route("/index")
def home():
    return render_template("index.j2")
     

@app.route("/planets", methods=["POST", "GET"])
def planets():

    # Add planets to the table 
    if request.method == "POST":
            if request.form.get("Add_Planet"):
                # gets the inputs from the form
                planet_name = request.form["planet_name"]
                distance_from_hq = request.form["distance_from_hq"]
                description = request.form["description"]
                query = "INSERT INTO Planets(planet_name, distance_from_hq, description) VALUES (%s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (planet_name, distance_from_hq, description))
                mysql.connection.commit()
                return redirect("/planets")

    # Will populate the table for the planets 
    if request.method == "GET":
            # mySQL query to grab all the people in bsg_people
            query = "SELECT planet_id, planet_name, description, distance_from_hq FROM Planets;"
            cur = mysql.connection.cursor()
            cur.execute(query)
            data = cur.fetchall()

            # mySQL query to grab planet id/name data for our dropdown
            query2 = "SELECT planet_id, planet_name FROM Planets"
            cur = mysql.connection.cursor()
            cur.execute(query2)
            planet_data = cur.fetchall()

            # render edit_people page passing our query data and homeworld data to the edit_people template
            return render_template("planets.j2", data=data)


    
@app.route("/delete_planets/<int:id>")
def delete_planet(id):
    # mySQL query to delete the planet with our passed id
    query = "DELETE FROM Planets WHERE planet_id = %s;"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    # redirect back to planets page
    return redirect("/planets")

@app.route("/shipment_invoices", methods=["POST", "GET"])
def shipment_invoices():

    # Update a shipment invoice, not in html yet
    if request.method == "POST":
        if request.form.get("Update_Shipment_Invoice"):
            # gets the inputs from the form
            invoice_id = request.form["invoice_id"]
            cost = request.form["cost"]
            planet_id = request.form["planet_id"]
            customer_id = request.form["customer_id"]
            shipment_type_id = request.form["shipment_type_id"]

            if customer_id == 0:    
                query = "Update Shipment_invoices SET Shipment_invoices.cost = %s, Shipment_invoices.planet_id = %s, Shipment_invoices.customer_id = NULL , Shipment_invoices.shipment_type_id = %s WHERE Shipment_invoices.invoice_id = %s;"
                cur = mysql.connection.cursor()
                cur.execute(query, (cost, planet_id, shipment_type_id))
                mysql.connection.commit()
                return redirect("/shipment_invoices")

            else:
                query = "Update Shipment_invoices SET Shipment_invoices.cost = %s, Shipment_invoices.planet_id = %s, Shipment_invoices.customer_id = %s , Shipment_invoices.shipment_type_id = %s WHERE Shipment_invoices.invoice_id = %s;"
                cur = mysql.connection.cursor()
                cur.execute(query, (cost, planet_id, customer_id, shipment_type_id))
                mysql.connection.commit()
                return redirect("/shipment_invoices")

    # Will populate the table for the shipment Invoices
    if request.method == "GET":
            # mySQL query to grab all the people in bsg_people
            query = "SELECT invoice_id, cost, Planets.planet_name AS destination, Customers.customer_name AS sender, Shipment_types.shipment_time AS shipping FROM Shipment_invoices INNER JOIN Planets ON Shipment_invoices.planet_id = Planets.planet_id INNER JOIN Customers ON Shipment_invoices.customer_id = Customers.customer_id INNER JOIN Shipment_types ON Shipment_invoices.shipment_type_id = Shipment_types.shipment_type_id;"
            cur = mysql.connection.cursor()
            cur.execute(query)
            data = cur.fetchall()

            # mySQL query to grab planet id/name data for our dropdown
            query2 = "SELECT planet_id, planet_name FROM Planets"
            cur = mysql.connection.cursor()
            cur.execute(query2)
            planet_data = cur.fetchall()

            # mysql query for sender/customerid
            query2 = "SELECT customer_id, customer_name FROM Customers"
            cur = mysql.connection.cursor()
            cur.execute(query2)
            customer_data = cur.fetchall()

            #mysql query for shipment types
            query2 = "SELECT shipment_type_id, shipment_time FROM Shipment_types"
            cur = mysql.connection.cursor()
            cur.execute(query2)
            shipment_types_data = cur.fetchall()

            # render edit_people page passing our query data and homeworld data to the edit_people template
            return render_template("shipment_invoices.j2", data=data, planets=planet_data, customers=customer_data, shipment_types=shipment_types_data)

@app.route("/add_shipment_invoice", methods=["POST"])
def add_shipment_invoice():
    if request.form.get("Add_Shipment_Invoice"):
        # gets the inputs from the form
        cost = request.form["cost"]
        planet_id = request.form["planet_id"]
        customer_id = request.form["customer_id"]
        shipment_type_id = request.form["shipment_type_id"]

        if customer_id == 0:    
            query = "INSERT INTO Shipment_invoices(cost, planet_id, shipment_type_id) VALUES (%s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (cost, planet_id, shipment_type_id))
            mysql.connection.commit()
            return redirect("/shipment_invoices")

        else:
            query = "INSERT INTO Shipment_invoices(cost, planet_id, customer_id, shipment_type_id) VALUES (%s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (cost, planet_id, customer_id, shipment_type_id))
            mysql.connection.commit()
            return redirect("/shipment_invoices")
    
@app.route("/delete_shipment_invoice/<int:id>")
def delete_shipment_invoice(id):
    # mySQL query to delete the shipment invoice with our passed id
    query = "DELETE FROM Shipment_invoices WHERE invoice_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    # redirect back to people shipment invoice
    return redirect("/shipment_invoices")

@app.route("/packages", methods=["POST", "GET"])
def packages():

    # Will populate the table for the shipment Invoices
    if request.method == "GET":
            # mySQL query to grab all the people in bsg_people
            query = 'SELECT package_id, weight, hazards, Shipment_invoices.invoice_id, recipient FROM Packages INNER JOIN Shipment_invoices ON Packages.invoice_id = Shipment_invoices.invoice_id;'
            cur = mysql.connection.cursor()
            cur.execute(query)
            data = cur.fetchall()

            # mySQL query to grab planet id/name data for our dropdown
            query2 = "SELECT planet_id, planet_name FROM Planets"
            cur = mysql.connection.cursor()
            cur.execute(query2)
            planet_data = cur.fetchall()

            query3 = "SELECT invoice_id FROM Shipment_invoices WHERE invoice_id NOT IN (SELECT invoice_id FROM Packages)"
            cur = mysql.connection.cursor()
            cur.execute(query3)
            unused_invoices = cur.fetchall()

            # render edit_people page passing our query data and homeworld data to the edit_people template
            return render_template("packages.j2", data=data, unused_invoices=unused_invoices)
    
@app.route("/add_package", methods=["POST"])
def add_package():
    if request.form.get("Add_Package"):
        weight= request.form["weight"]
        hazards = request.form["hazards"]
        invoice_id = request.form["invoice_id"]
        recipient = request.form["recipient"]
        
        query = "INSERT INTO Packages(weight, hazards, invoice_id, recipient) VALUES (%s, %s, %s, %s)"
        cur = mysql.connection.cursor()
        cur.execute(query, (weight, hazards, invoice_id, recipient))
        mysql.connection.commit()
        return redirect("/packages")


@app.route("/customers", methods=["POST", "GET"])
def customers():

    # Will populate the table for the shipment Invoices
    if request.method == "GET":
            # mySQL query to grab all the people in bsg_people
            query = "SELECT Customers.customer_id, customer_name, customer_email, Planets.planet_name AS home FROM Customers LEFT JOIN Planets ON Customers.planet_id = Planets.planet_id ORDER BY customer_name ASC;"
            cur = mysql.connection.cursor()
            cur.execute(query)
            data = cur.fetchall()

            # mySQL query to grab planet id/name data for our dropdown
            query2 = "SELECT planet_id, planet_name FROM Planets"
            cur = mysql.connection.cursor()
            cur.execute(query2)
            planet_data = cur.fetchall()

            # render edit_people page passing our query data and homeworld data to the edit_people template
            return render_template("customers.j2", data=data, planets=planet_data)
    
    if request.method == "POST":
        if request.form.get("Update_Customer"):
            customer_id = request.form["customer_id"]
            customer_name = request.form["customer_name"]
            customer_email = request.form["customer_email"]
            planet_id = request.form["planet_id"]
        
        if planet_id == "0":
            query = "UPDATE Customers SET Customers.customer_name = %s, Customers.customer_email = %s, Customers.planet_id = NULL WHERE Customers.customer_id = %s;"
            cur = mysql.connection.cursor()
            cur.execute(query,(customer_name, customer_email, customer_id))
            mysql.connection.commit()
        
        else:
            query = "UPDATE Customers SET Customers.customer_name = %s, Customers.customer_email = %s, Customers.planet_id =%s WHERE Customers.customer_id = %s;"
            cur = mysql.connection.cursor()
            cur.execute(query,(customer_name, customer_email, planet_id, customer_id))
            mysql.connection.commit()

        return redirect("/customers")
    
@app.route("/add_customer", methods=["POST"])
def add_customer():
    if request.form.get("Add_Customer"):
        customer_name = request.form["customer_name"]
        customer_email = request.form["customer_email"]
        planet_id = request.form["planet_id"]
        
        if planet_id == "0":
            query = "INSERT INTO Customers(customer_name, customer_email, planet_id) VALUES (%s, %s, NULL)"
            cur = mysql.connection.cursor()
            cur.execute(query, (customer_name, customer_email))
            mysql.connection.commit()
            return redirect("/customers")
        else:
            query = "INSERT INTO Customers(customer_name, customer_email, planet_id) VALUES (%s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (customer_name, customer_email, planet_id))
            mysql.connection.commit()
            return redirect("/customers")

@app.route("/delete_customer/<int:id>")
def delete_customer(id):
    # mySQL query to delete the planet with our passed id
    query = "DELETE FROM Customers WHERE customer_id = %s;"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    # redirect back to customers page
    return redirect("/customers")

@app.route("/shipment_types", methods=["POST", "GET"])
def shipment_types():

    if request.method == "POST":
            if request.form.get("Add_Shipment_Type"):
                # gets the inputs from the form
                shipment_time = request.form["shipment_time"]
                is_active = request.form["is_active"]
                query = "INSERT INTO Shipment_types(shipment_time, is_active) VALUES (%s, %s);"
                cur = mysql.connection.cursor()
                cur.execute(query, (shipment_time, is_active))
                mysql.connection.commit()
                return redirect("/shipment_types")

    # Will populate the table for the shipment Invoices
    if request.method == "GET":
            # mySQL query to grab all the people in bsg_people
            query = "SELECT shipment_type_id, shipment_time, is_active FROM Shipment_types;"
            cur = mysql.connection.cursor()
            cur.execute(query)
            data = cur.fetchall()

            # mySQL query to grab planet id/name data for our dropdown
            query2 = "SELECT planet_id, planet_name FROM Planets"
            cur = mysql.connection.cursor()
            cur.execute(query2)
            planet_data = cur.fetchall()

            # render edit_people page passing our query data and homeworld data to the edit_people template
            return render_template("shipment_types.j2", data=data)

    

# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 15330)) 
    #                                 ^^^^
    #              You can replace this number with any valid port
    
    app.run(port=port, debug=True)
