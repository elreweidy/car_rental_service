from flask import Flask, request, jsonify
import mysql.connector
import datetime 


# Connect to MySQL DB
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Transporter@021",
    database="car_rental_system"
)

app = Flask(__name__)

# Endpoint to add new customer
@app.route('/customers', methods=['POST'])
def add_customer():
    data = request.get_json()
    name = data['name']
    email = data['email']
    phone = data['phone']
    address = data['address']
    
    cursor = db.cursor()
    query = "INSERT INTO customer (name, email, phone, address) VALUES (%s, %s, %s, %s)"
    values = (name, email, phone, address)
    cursor.execute(query, values)
    db.commit()
    
    return jsonify({'message': 'Customer added successfully'}), 201

# Endpoint to update customer
@app.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    data = request.get_json()
    name = data['name']
    email = data['email']
    phone = data['phone']
    address = data['address']
    
    cursor = db.cursor()
    query = "UPDATE customer SET name=%s, email=%s, phone=%s, address=%s WHERE customer_id=%s"
    values = (name, email, phone, address, id)
    cursor.execute(query, values)
    db.commit()
    
    return jsonify({'message': 'Customer updated successfully'})

# Endpoint to delete customer
@app.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    cursor = db.cursor()
    query = "DELETE FROM customers WHERE customer_id=%s"
    values = (id,)
    cursor.execute(query, values)
    db.commit()
    
    return jsonify({'message': 'Customer deleted successfully'})

# Endpoint to get customer
@app.route('/customers/<int:id>', methods=['GET'])
def get_customer(id):
    cursor = db.cursor()
    query = "SELECT * FROM customers WHERE customer_id=%s"
    values = (id,)
    cursor.execute(query, values)
    result = cursor.fetchone()
    if result:
        customer = {
            'id': result[0],
            'name': result[1],
            'email': result[2],
            'phone': result[3],
            'address': result[4]
        }
        return jsonify(customer)
    else:
        return jsonify({'message': 'Customer not found'}), 404


@app.route('/bookings', methods=['POST'])
def add_booking():
    data = request.get_json()
    customer_id = data['customer_id']
    vehicle_id = data['vehicle_id']
    hire_date = data['hire_date']
    return_date = data['return_date']
    
    # Check if the customer has any existing bookings
    cursor = db.cursor()
    query = "SELECT * FROM bookings WHERE customer_id=%s"
    values = (customer_id,)
    cursor.execute(query, values)
    existing_bookings = cursor.fetchall()
    if len(existing_bookings) > 0:
        # Check if the customer has any current bookings
        current_date = datetime.datetime.now()
        for booking in existing_bookings:
            booking_return_date = datetime.datetime.strptime(str(booking[4]), '%Y-%m-%d')
            if booking_return_date >= current_date:
                return jsonify({'message': 'Customer already has a current bookings'}), 400
    
    # Check vehicle availability
    query = "SELECT * FROM vehicles WHERE vehicle_id=%s AND available='Yes'"
    values = (vehicle_id,)
    cursor.execute(query, values)
    available_vehicles = cursor.fetchall()
    if len(available_vehicles) == 0:
        return jsonify({'message': 'Selected vehicles not available'}), 400
    
    # Make new booking
    query = "INSERT INTO bookings (customer_id, vehicle_id, hire_date, return_date) VALUES (%s, %s, %s, %s)"
    values = (customer_id, vehicle_id, hire_date, return_date)
    cursor.execute(query, values)
    db.commit()
    
    # Update vehicle availability
    query = "UPDATE vehicles SET available='No' WHERE vehicle_id=%s"
    values = (vehicle_id,)
    cursor.execute(query, values)
    db.commit()
    
    # Create invoice
    query = "SELECT * FROM customers WHERE customer_id=%s"
    values = (customer_id,)
    cursor.execute(query, values)
    customer = cursor.fetchone()
    query = "SELECT * FROM vehicles WHERE customer_id=%s"
    values = (vehicle_id,)
    cursor.execute(query, values)
    vehicle = cursor.fetchone()
    vehicle_type = vehicle[1]
    vehicle_rental_rate = vehicle[2]
    rental_days = (datetime.datetime.strptime(return_date, '%Y-%m-%d') - datetime.datetime.strptime(hire_date, '%Y-%m-%d')).days
    total_rental_amount = vehicle_rental_rate * rental_days
    invoice_data = {
        'customer_name': customer[1],
        'customer_email': customer[2],
        'vehicle_type': vehicle_type,
        'hire_date': hire_date,
        'return_date': return_date,
        'rental_days': rental_days,
        'vehicle_rental_rate': vehicle_rental_rate,
        'total_rental_amount': total_rental_amount
    }
    query = "INSERT INTO invoice (customer_id, vehicle_id, hire_date, return_date, rental_days, vehicle_rental_rate, total_rental_amount) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (customer_id, vehicle_id, hire_date, return_date, rental_days, vehicle_rental_rate, total_rental_amount)
    cursor.execute(query, values)
    db.commit()
    
    return jsonify({'message': 'Booking added successfully', 'invoice_data': invoice_data}), 201

