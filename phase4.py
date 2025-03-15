from flask import Flask, jsonify, render_template, request, redirect , url_for
import mysql.connector
from flask_bcrypt import Bcrypt
from flask_session import Session
import hashlib
from datetime import date 
from flask import Flask, request, jsonify, redirect, url_for, render_template
import logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

import hashlib

hashed_password = hashlib.sha256('password123'.encode()).hexdigest()


app = Flask(__name__)
app.secret_key = '123'  # Replace 'your_secret_key' with a strong random value

bcrypt = Bcrypt(app)
con = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root1234',
    database='gym'
)
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='root1234',
        database='gym'
    )



@app.route('/', methods=['GET'])
def homepage():
    return render_template('index.html')  # Render the main homepage

@app.route('/trainers', methods=['GET'])
def trainers():
    try:
        con = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root1234',
            database='gym'
        )
        cursor = con.cursor(dictionary=True)

        # Fetch all trainers
        cursor.execute("SELECT Trainer_ID, First_Name, Last_Name, Specialty, PhoneNumber_Trainer, is_deleted FROM Trainer")
        trainers = cursor.fetchall()

        # Debugging: Print the fetched data
        print("Fetched Trainers:", trainers)

        # Render the trainers page
        return render_template('trainers.html', trainers=trainers)

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'con' in locals():
            con.close()


 



@app.route('/trainers/register', methods=['GET'])
def register_page():
    return render_template('register_trainer.html')  # Ensure this template matches your registration form



@app.route('/register_trainer', methods=['POST'])
def register_trainer():
    try:
        # Retrieve form data
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        address = request.form.get('address_trainers')
        phone_number = request.form.get('phone_number_trainer')
        ssn = request.form.get('snntrainer')
        salary = request.form.get('salary')
        age = request.form.get('agetrainer')
        specialties = request.form.getlist('specialty')
        email = request.form.get('email')
        password = request.form.get('password')

        # Validate mandatory fields
        if not all([first_name, last_name, address, phone_number, ssn, salary, age, email, password]):
            return render_template('register_trainer.html', error="All fields are required.")

        # Validate specialties limit
        if len(specialties) > 3:
            return render_template('register_trainer.html', error="You can select a maximum of three specialties.")
        specialty_str = ', '.join(specialties)

        # Establish database connection
        con = get_db_connection()
        cursor = con.cursor(dictionary=True)

        # Check for duplicate phone number
        cursor.execute("SELECT * FROM Trainer WHERE PhoneNumber_Trainer = %s", (phone_number,))
        if cursor.fetchone():
            return render_template('register_trainer.html', error="Phone number already exists.")

        # Check for duplicate SSN
        cursor.execute("SELECT * FROM Trainer WHERE SNNTrainer = %s", (ssn,))
        if cursor.fetchone():
            return render_template('register_trainer.html', error="SSN already exists.")

        # Check for duplicate email
        cursor.execute("SELECT * FROM Trainer WHERE Email = %s", (email,))
        if cursor.fetchone():
            return render_template('register_trainer.html', error="Email already exists.")

        # Hash the password before storing
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Retrieve the current maximum Trainer_ID
        cursor.execute("SELECT MAX(Trainer_ID) AS max_id FROM Trainer;")
        result = cursor.fetchone()
        max_id = result['max_id'] if result['max_id'] else 0
        trainer_id = max_id + 1

        # Insert the new trainer
        query = """
        INSERT INTO Trainer (Trainer_ID, First_Name, Last_Name, Address_trainers, PhoneNumber_Trainer, SNNTrainer, Salary, Specialty, AgeTrainer, Email, Password, is_deleted)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (trainer_id, first_name, last_name, address, phone_number, ssn, salary, specialty_str, age, email, hashed_password, False)
        cursor.execute(query, values)

        # Insert an initial payment record for the new trainer
        payment_query = """
        INSERT INTO Payment (Payment_ID, Trainer_ID, PaymentAmount, Payment_Date, PaymentDue_Date, PaymentStatus)
        VALUES (%s, %s, %s, NOW(), DATE_ADD(NOW(), INTERVAL 30 DAY), %s)
        """
        cursor.execute("SELECT MAX(Payment_ID) AS max_payment_id FROM Payment;")
        payment_result = cursor.fetchone()
        max_payment_id = payment_result['max_payment_id'] if payment_result['max_payment_id'] else 0
        payment_id = max_payment_id + 1
        payment_status = 'Pending'  # Or 'Unpaid', based on your logic
        cursor.execute(payment_query, (payment_id, trainer_id, salary, payment_status))

        # Commit the changes
        con.commit()

        # Redirect to success page with new Trainer ID
        return render_template('success.html', trainer_id=trainer_id)

    except mysql.connector.Error as db_err:
        # Handle database errors
        return render_template('register_trainer.html', error=f"Database Error: {db_err}")

    except Exception as e:
        # Handle unexpected errors
        return render_template('register_trainer.html', error=f"An unexpected error occurred: {e}")

    finally:
        # Close database connection
        if 'cursor' in locals():
            cursor.close()
        if 'con' in locals():
            con.close()







@app.route('/trainers/registerjoin', methods=['GET'])
def register_pagejoin():
    return render_template('regTrainerJoin.html')  # Ensure this template matches your registration form



@app.route('/register_trainerjoin', methods=['POST'])
def register_trainerjoin():
    try:
        # Retrieve form data
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        address = request.form.get('address_trainers')
        phone_number = request.form.get('phone_number_trainer')
        ssn = request.form.get('snntrainer')
        salary = request.form.get('salary')
        age = request.form.get('agetrainer')
        specialties = request.form.getlist('specialty')
        email = request.form.get('email')
        password = request.form.get('password')

        # Validate mandatory fields
        if not all([first_name, last_name, address, phone_number, ssn, salary, age, email, password]):
            return render_template('regTrainerJoin.html', error="All fields are required.")

        # Validate specialties limit
        if len(specialties) > 3:
            return render_template('regTrainerJoin.html', error="You can select a maximum of three specialties.")
        specialty_str = ', '.join(specialties)

        # Establish database connection
        con = get_db_connection()
        cursor = con.cursor(dictionary=True)

        # Check for duplicate phone number
        cursor.execute("SELECT * FROM Trainer WHERE PhoneNumber_Trainer = %s", (phone_number,))
        if cursor.fetchone():
            return render_template('regTrainerJoin.html', error="Phone number already exists.")

        # Check for duplicate SSN
        cursor.execute("SELECT * FROM Trainer WHERE SNNTrainer = %s", (ssn,))
        if cursor.fetchone():
            return render_template('regTrainerJoin.html', error="SSN already exists.")

        # Check for duplicate email
        cursor.execute("SELECT * FROM Trainer WHERE Email = %s", (email,))
        if cursor.fetchone():
            return render_template('regTrainerJoin.html', error="Email already exists.")

        # Hash the password before storing
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Retrieve the current maximum Trainer_ID
        cursor.execute("SELECT MAX(Trainer_ID) AS max_id FROM Trainer;")
        result = cursor.fetchone()
        max_id = result['max_id'] if result['max_id'] else 0
        trainer_id = max_id + 1

        # Insert the new trainer
        query = """
        INSERT INTO Trainer (Trainer_ID, First_Name, Last_Name, Address_trainers, PhoneNumber_Trainer, SNNTrainer, Salary, Specialty, AgeTrainer, Email, Password, is_deleted)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (trainer_id, first_name, last_name, address, phone_number, ssn, salary, specialty_str, age, email, hashed_password, False)
        cursor.execute(query, values)

        # Insert an initial payment record for the new trainer
        payment_query = """
        INSERT INTO Payment (Payment_ID, Trainer_ID, PaymentAmount, Payment_Date, PaymentDue_Date, PaymentStatus)
        VALUES (%s, %s, %s, NOW(), DATE_ADD(NOW(), INTERVAL 30 DAY), %s)
        """
        cursor.execute("SELECT MAX(Payment_ID) AS max_payment_id FROM Payment;")
        payment_result = cursor.fetchone()
        max_payment_id = payment_result['max_payment_id'] if payment_result['max_payment_id'] else 0
        payment_id = max_payment_id + 1
        payment_status = 'Pending'  # Or 'Unpaid', based on your logic
        cursor.execute(payment_query, (payment_id, trainer_id, salary, payment_status))

        # Commit the changes
        con.commit()

        # Redirect to success page with new Trainer ID
        return render_template('joinUs.html', trainer_id=trainer_id)

    except mysql.connector.Error as db_err:
        # Handle database errors
        return render_template('regTrainerJoin.html', error=f"Database Error: {db_err}")

    except Exception as e:
        # Handle unexpected errors
        return render_template('regTrainerJoin.html', error=f"An unexpected error occurred: {e}")

    finally:
        # Close database connection
        if 'cursor' in locals():
            cursor.close()
        if 'con' in locals():
            con.close()







@app.route('/trainers/edit/<int:trainer_id>', methods=['GET', 'POST'])
def edit_trainer(trainer_id):
    con = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root1234',
        database='gym'
    )
    cursor = con.cursor(dictionary=True)

    if request.method == 'GET':
        cursor.execute("SELECT * FROM Trainer WHERE Trainer_ID = %s", (trainer_id,))
        trainer = cursor.fetchone()
        cursor.close()
        con.close()
        return render_template('edit_trainer.html', trainer=trainer)

    elif request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        address = request.form['address_trainers']
        phone_number = request.form['phone_number_trainer']
        snn = request.form['snntrainer']
        salary = request.form['salary']
        age = request.form['agetrainer']
        specialties = request.form.getlist('specialty')
        email = request.form['email']
        password = request.form['password']
        is_deleted = request.form['is_deleted']

        # Initialize error messages
        phone_error = None
        ssn_error = None
        email_error = None

        # Validate specialties
        if len(specialties) > 3:
            specialty_error = "Error: You can select a maximum of three specialties."
            return render_template(
                'edit_trainer.html', trainer=trainer, phone_error=phone_error, ssn_error=ssn_error, specialty_error=specialty_error
            )
        specialty_str = ', '.join(specialties)

        # Check for duplicate phone number (excluding current trainer)
        cursor.execute(
            "SELECT * FROM Trainer WHERE PhoneNumber_Trainer = %s AND Trainer_ID != %s",
            (phone_number, trainer_id)
        )
        if cursor.fetchone():
            phone_error = "Phone number already exists."

        # Check for duplicate SSN (excluding current trainer)
        cursor.execute(
            "SELECT * FROM Trainer WHERE SNNTrainer = %s AND Trainer_ID != %s",
            (snn, trainer_id)
        )
        if cursor.fetchone():
            ssn_error = "SSN already exists."

        # Check for duplicate email (excluding current trainer)
        cursor.execute(
            "SELECT * FROM Trainer WHERE Email = %s AND Trainer_ID != %s",
            (email, trainer_id)
        )
        if cursor.fetchone():
            email_error = "Email already exists."

        # If there are errors, re-render the form with error messages
        if phone_error or ssn_error or email_error:
            cursor.execute("SELECT * FROM Trainer WHERE Trainer_ID = %s", (trainer_id,))
            trainer = cursor.fetchone()  # Re-fetch the trainer's data
            cursor.close()
            con.close()
            return render_template(
                'edit_trainer.html', trainer=trainer, phone_error=phone_error, ssn_error=ssn_error, email_error=email_error
            )

        # Hash the password if provided
        hashed_password = None
        if password:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Update the trainer record
        query = """
        UPDATE Trainer
        SET First_Name = %s, Last_Name = %s, Address_trainers = %s, PhoneNumber_Trainer = %s,
            SNNTrainer = %s, Salary = %s, Specialty = %s, AgeTrainer = %s, Email = %s
        """
        values = [first_name, last_name, address, phone_number, snn, salary, specialty_str, age, email]

        # Include password update only if provided
        if hashed_password:
            query += ", Password = %s"
            values.append(hashed_password)

        query += " WHERE Trainer_ID = %s"
        values.append(trainer_id)

        cursor.execute(query, tuple(values))
        con.commit()
        cursor.close()
        con.close()
        return redirect('/trainers')


@app.route('/check_unique', methods=['POST'])
def check_unique():
    data = request.json
    field = data.get('field')  # Either 'PhoneNumber_Trainer' or 'SNNTrainer'
    value = data.get('value')

    if not field or not value:
        return jsonify({'exists': False}), 400

    con = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root1234',
        database='gym'
    )
    cursor = con.cursor(dictionary=True)
    try:
        query = f"SELECT COUNT(*) AS count FROM Trainer WHERE {field} = %s"
        cursor.execute(query, (value,))
        result = cursor.fetchone()
        return jsonify({'exists': result['count'] > 0})
    finally:
        cursor.close()
        con.close()


@app.route('/trainers/delete/<int:trainer_id>', methods=['POST'])
def delete_trainer(trainer_id):
    try:
        con = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root1234',
            database='gym'
        )
        cursor = con.cursor()
        # Update `is_deleted` to True
        cursor.execute("UPDATE Trainer SET is_deleted = TRUE WHERE Trainer_ID = %s", (trainer_id,))
        con.commit()
        return redirect('/trainers')

    except Exception as e:
        return f"An error occurred: {e}"

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'con' in locals():
            con.close()

@app.route('/trainers/restore/<int:trainer_id>', methods=['POST'])
def restore_trainer(trainer_id):
    try:
        con = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root1234',
            database='gym'
        )
        cursor = con.cursor()

        # Update the is_deleted column to FALSE
        cursor.execute("UPDATE Trainer SET is_deleted = FALSE WHERE Trainer_ID = %s", (trainer_id,))
        con.commit()

        return redirect('/trainers')

    except Exception as e:
        return f"An error occurred: {e}"

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'con' in locals():
            con.close()




@app.route('/classes', methods=['GET'])
def get_classes():
    con = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root1234',
        database='gym'
    )
    cursor = con.cursor(dictionary=True)
    try:
        query = """
        SELECT Class.Class_Name, Class.Start_Time, Class.End_Time, Class.Capacity, 
               Trainer.First_Name AS Trainer_First_Name, Trainer.Last_Name AS Trainer_Last_Name
        FROM Class
        JOIN Trainer ON Class.Trainer_ID = Trainer.Trainer_ID;
        """
        cursor.execute(query)
        raw_classes = cursor.fetchall()

        days_mapping = {
            "Strength Training": ["Monday", "Wednesday"],
            "Crossfit": ["Tuesday", "Thursday"],
            "Yoga": ["Sunday", "Friday", "Saturday"],
            "Cardio": ["Monday", "Wednesday"],
            "Zumba": ["Tuesday", "Thursday"],
            "Pilates": ["Sunday", "Friday", "Saturday"]
        }

        # Use a dictionary to prevent duplicates in each day
        classes_by_day = {day: [] for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}
        seen_classes = {day: set() for day in classes_by_day.keys()}

        for cls in raw_classes:
            cls_name = cls['Class_Name']
            assigned_days = days_mapping.get(cls_name, [])
            for day in assigned_days:
                class_identifier = (cls_name, cls['Start_Time'], cls['End_Time'], cls['Trainer_First_Name'], cls['Trainer_Last_Name'])
                if class_identifier not in seen_classes[day]:
                    classes_by_day[day].append(cls)
                    seen_classes[day].add(class_identifier)

        return render_template('classes.html', classes_by_day=classes_by_day)
    finally:
        cursor.close()
        con.close()



@app.route('/schedules', methods=['GET'])
def get_trainer_schedules():
    con = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root1234',
        database='gym'
    )
    cursor = con.cursor(dictionary=True)
    try:
        # Fetch all classes with trainer details
        query = """
        SELECT Class.Class_Name, Class.Start_Time, Class.End_Time, Trainer.First_Name AS Trainer_First_Name, 
               Trainer.Last_Name AS Trainer_Last_Name, Trainer.Trainer_ID
        FROM Class
        JOIN Trainer ON Class.Trainer_ID = Trainer.Trainer_ID;
        """
        cursor.execute(query)
        classes = cursor.fetchall()

        # Days mapping based on class name
        days_mapping = {
            "Strength Training": ["Monday", "Wednesday"],
            "Crossfit": ["Tuesday", "Thursday"],
            "Yoga": ["Sunday", "Friday", "Saturday"],
            "Cardio": ["Monday", "Wednesday"],
            "Zumba": ["Tuesday", "Thursday"],
            "Pilates": ["Sunday", "Friday", "Saturday"]
        }

        # Organize schedules by trainer
        schedules = {}
        for cls in classes:
            trainer_id = cls["Trainer_ID"]
            trainer_name = f"{cls['Trainer_First_Name']} {cls['Trainer_Last_Name']}"
            cls_days = days_mapping.get(cls["Class_Name"], [])
            if trainer_id not in schedules:
                schedules[trainer_id] = {"Trainer_Name": trainer_name, "Classes": []}
            for day in cls_days:
                schedules[trainer_id]["Classes"].append({
                    "Class_Name": cls["Class_Name"],
                    "Day": day,
                    "Start_Time": cls["Start_Time"],
                    "End_Time": cls["End_Time"]
                })

        return render_template('schedules.html', schedules=schedules)
    finally:
        cursor.close()
        con.close()

@app.route('/schedules', methods=['GET'])
def get_all_schedules():
    con = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root1234',
        database='gym'
    )
    cursor = con.cursor(dictionary=True)
    try:
        # Fetch all classes and trainers
        query = """
        SELECT Class.Class_Name, Class.Start_Time, Class.End_Time, Trainer.First_Name AS Trainer_First_Name, 
               Trainer.Last_Name AS Trainer_Last_Name, Trainer.Trainer_ID
        FROM Class
        JOIN Trainer ON Class.Trainer_ID = Trainer.Trainer_ID;
        """
        cursor.execute(query)
        classes = cursor.fetchall()

        # Group schedules by trainer
        schedules = {}
        for cls in classes:
            trainer_id = cls["Trainer_ID"]
            trainer_name = f"{cls['Trainer_First_Name']} {cls['Trainer_Last_Name']}"
            if trainer_id not in schedules:
                schedules[trainer_id] = {"Trainer_Name": trainer_name, "Classes": []}
            schedules[trainer_id]["Classes"].append({
                "Class_Name": cls["Class_Name"],
                "Start_Time": cls["Start_Time"],
                "End_Time": cls["End_Time"]
            })

        return render_template('schedules.html', schedules=schedules)
    finally:
        cursor.close()
        con.close()

@app.route('/schedules/view', methods=['GET'])
def view_trainer_schedule():
    trainer_id = request.args.get('trainer_id')  # Get trainer ID from the query parameters
    if not trainer_id:
        return "Trainer ID is required", 400

    con = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root1234',
        database='gym'
    )
    cursor = con.cursor(dictionary=True)
    try:
        # Query to get the trainer's details and schedule
        query = """
        SELECT Trainer.First_Name AS Trainer_First_Name, Trainer.Last_Name AS Trainer_Last_Name,
               Trainer.Trainer_ID, Class.Class_Name, Class.Start_Time, Class.End_Time
        FROM Trainer
        JOIN Class ON Trainer.Trainer_ID = Class.Trainer_ID
        WHERE Trainer.Trainer_ID = %s
        """
        cursor.execute(query, (trainer_id,))
        schedule = cursor.fetchall()

        if not schedule:
            return f"No schedule found for Trainer ID {trainer_id}", 404

        # Get trainer name from the first record
        trainer_name = f"{schedule[0]['Trainer_First_Name']} {schedule[0]['Trainer_Last_Name']}"

        return render_template('schedule_by_id.html', schedule=schedule, trainer_name=trainer_name)
    finally:
        cursor.close()
        con.close()

@app.route('/add_class', methods=['GET', 'POST'])
def add_class():
    con = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root1234',
        database='gym'
    )
    cursor = con.cursor(dictionary=True)

    # Define the days mapping for each class type
    days_mapping = {
        "Strength Training": ["Monday", "Wednesday"],
        "Crossfit": ["Tuesday", "Thursday"],
        "Yoga": ["Sunday", "Friday", "Saturday"],
        "Cardio": ["Monday", "Wednesday"],
        "Zumba": ["Tuesday", "Thursday"],
        "Pilates": ["Sunday", "Friday", "Saturday"]
    }

    if request.method == 'GET':
        try:
            # Fetch all trainers for dropdown
            cursor.execute("SELECT Trainer_ID, First_Name, Last_Name FROM Trainer WHERE is_deleted = FALSE")
            trainers = cursor.fetchall()
            return render_template('add_class.html', trainers=trainers, days_mapping=days_mapping)
        finally:
            cursor.close()
            con.close()

    elif request.method == 'POST':
        try:
            # Fetch all trainers for error handling in POST request
            cursor.execute("SELECT Trainer_ID, First_Name, Last_Name FROM Trainer WHERE is_deleted = FALSE")
            trainers = cursor.fetchall()

            # Retrieve form data
            trainer_id = request.form.get('trainer_id')
            class_days = request.form.get('class_days')  # Selected class type and days
            start_time = request.form.get('start_time')
            end_time = request.form.get('end_time')
            capacity = request.form.get('capacity')

            # Debug: Print inputs
            print(f"Trainer ID: {trainer_id}")
            print(f"Class Days: {class_days}")
            print(f"Start Time: {start_time}, End Time: {end_time}")
            print(f"Capacity: {capacity}")

            # Validate inputs
            if not all([trainer_id, class_days, start_time, end_time, capacity]):
                return render_template('add_class.html', error="All fields are required.", trainers=trainers, days_mapping=days_mapping)

            # Extract class type and days from the selected value
            class_type, days = class_days.split('|')
            days = days.split(', ')  # Convert days string back to a list
            print(f"Class Type: {class_type}, Days: {days}")

            # Insert classes for the selected days
            for day in days:
                query = """
                INSERT INTO Class (Class_Name, Start_Time, End_Time, Capacity, Trainer_ID, Day)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                values = (class_type, start_time, end_time, capacity, trainer_id, day)
                print(f"Executing Query: {query} with values {values}")
                cursor.execute(query, values)

            con.commit()

            # Redirect to the admin dashboard
            return redirect('/admin_dashboard')

        except Exception as e:
            print(f"Error occurred: {e}")  # Debug the exact error
            return render_template('add_class.html', error=f"Error: {e}", trainers=trainers, days_mapping=days_mapping)

        finally:
            cursor.close()
            con.close()



@app.route('/trainers_by_specialty', methods=['GET'])
def get_trainers_by_specialty():
    specialty = request.args.get('specialty')
    con = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root1234',
        database='gym'
    )
    cursor = con.cursor(dictionary=True)
    try:
        query = "SELECT Trainer_ID, First_Name, Last_Name FROM Trainer WHERE Specialty LIKE %s AND is_deleted = FALSE"
        cursor.execute(query, (f"%{specialty}%",))
        trainers = cursor.fetchall()
        return jsonify({'trainers': trainers})
    finally:
        cursor.close()
        con.close()

@app.route('/get_days', methods=['GET'])
def get_days():
    class_type = request.args.get('class_type')  # Get class type from the request

    cursor = con.cursor(dictionary=True)
    
    try:
        # Query to fetch days for the given class type
        query = "SELECT Day FROM ClassTypeDays WHERE ClassType = %s"
        cursor.execute(query, (class_type,))
        days = [row['Day'] for row in cursor.fetchall()]
        return jsonify({'days': days})  # Return days as JSON response
    finally:
        cursor.close()
        con.close()


@app.route('/plans', methods=['GET'])
def view_plans():
    return render_template('plans.html')


@app.route('/about', methods=['GET'])
def about_page():
    return render_template('about.html')



@app.route('/trainee/<int:trainee_id>/bills', methods=['GET'])
def trainee_bills(trainee_id):
    con = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root1234',
        database='gym'
    )
    cursor = con.cursor(dictionary=True)

    try:
        query = """
        SELECT plans.Plan_Name AS plan_name, bills.Bill_Amount AS bill_amount, 
               bills.Paid_Amount AS paid_amount,
               (bills.Bill_Amount - bills.Paid_Amount) AS pending_amount,
               bills.Due_Date AS due_date, 
               bills.Status AS status
        FROM bills
        JOIN plans ON bills.Plan_ID = plans.Plan_ID
        WHERE bills.Trainee_ID = %s
        """
        cursor.execute(query, (trainee_id,))
        bills = cursor.fetchall()

        return render_template('bill.html', bills=bills)
    finally:
        cursor.close()
        con.close()


@app.route('/trainers/profile/<int:trainer_id>', methods=['GET'])
def trainer_profile(trainer_id):
    con = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root1234',
        database='gym'
    )
    cursor = con.cursor(dictionary=True)
    try:
        # Fetch trainer details
        cursor.execute("SELECT * FROM Trainer WHERE Trainer_ID = %s AND is_deleted = FALSE", (trainer_id,))
        trainer = cursor.fetchone()
        if not trainer:
            return f"No trainer found with ID {trainer_id}", 404

        # Fetch classes conducted by this trainer
        cursor.execute("""
            SELECT Class.Class_Name, Class.Start_Time, Class.End_Time, Class.Capacity
            FROM Class
            WHERE Class.Trainer_ID = %s
        """, (trainer_id,))
        classes = cursor.fetchall()

        return render_template('trainer_profile.html', trainer=trainer, classes=classes)
    finally:
        cursor.close()
        con.close()

@app.route('/food_subscriptions', methods=['GET'])
def get_food_subscriptions():
    con = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root1234',
        database='gym'
    )
    cursor = con.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Food_Subscription")
        subscriptions = cursor.fetchall()
        
        return render_template('food_subscriptions.html', subscriptions=subscriptions)
    finally:
        cursor.close()
        con.close()



@app.route('/trainees', methods=['GET'])
def show_trainees():
    search_query = request.args.get('q', '').lower()
    
    con = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root1234',
        database='gym'
    )
    cursor = con.cursor(dictionary=True)
    try:
        if search_query:
            query = """
                SELECT Trainee_ID, First_Name, Last_Name, Phone_Number, SNN
                FROM Trainee
                WHERE (LOWER(First_Name) LIKE %s OR LOWER(Last_Name) LIKE %s)
                AND is_deleted = FALSE
            """
            cursor.execute(query, (f"%{search_query}%", f"%{search_query}%"))
        else:
            query = "SELECT Trainee_ID, First_Name, Last_Name, Phone_Number, SNN FROM Trainee WHERE is_deleted = FALSE"
            cursor.execute(query)
        
        trainees = cursor.fetchall()
        return render_template('trainees.html', trainees=trainees)
    finally:
        cursor.close()
        con.close()




@app.route('/trainees/register', methods=['GET'])
def register_trainee_page():
    # Get the role from the query parameters (default to 'not_admin')
    role = request.args.get('role', 'not_admin')
    return render_template('register_trainee.html', role=role)



@app.route('/register_trainee', methods=['POST'])
def register_trainee():
    try:
        # Retrieve form data
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone_number = request.form.get('phone_number')
        ssn = request.form.get('snn')
        address = request.form.get('address')
        age = request.form.get('age')
        email = request.form.get('email')  # Add email retrieval
        password = request.form.get('password')  # Add password retrieval

        # Validate mandatory fields
        if not all([first_name, last_name, phone_number, ssn, address, age, email, password]):
            return render_template('register_trainee.html', error="All fields are required.")

        # Establish database connection
        con = get_db_connection()
        cursor = con.cursor(dictionary=True)

        # Validate unique fields
        cursor.execute("SELECT * FROM Trainee WHERE Phone_Number = %s", (phone_number,))
        if cursor.fetchone():
            return render_template('register_trainee.html', error="Phone number already exists.")

        cursor.execute("SELECT * FROM Trainee WHERE SNN = %s", (ssn,))
        if cursor.fetchone():
            return render_template('register_trainee.html', error="SSN already exists.")

        cursor.execute("SELECT * FROM Trainee WHERE Email = %s", (email,))
        if cursor.fetchone():
            return render_template('register_trainee.html', error="Email already exists.")

        # Retrieve the current maximum Trainee_ID
        cursor.execute("SELECT MAX(Trainee_ID) AS max_id FROM Trainee;")
        result = cursor.fetchone()
        max_id = result['max_id'] if result['max_id'] else 0
        trainee_id = max_id + 1

        # Hash the password before storing it
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Insert the new trainee
        query = """
        INSERT INTO Trainee (Trainee_ID, First_Name, Last_Name, Phone_Number, SNN, AddressTrainee, AgeTrainee, Email, Password, Registration_Date, is_deleted)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (trainee_id, first_name, last_name, phone_number, ssn, address, age, email, hashed_password, date.today(), False)
        cursor.execute(query, values)
        con.commit()

        # Generate a bill for the new trainee
        cursor.execute("""
    SELECT SUM(price) AS total_amount
    FROM (
        SELECT price FROM Membership
        JOIN Member_Membership ON Membership.membership_id = Member_Membership.membership_id
        WHERE Member_Membership.member_id = %s
        UNION ALL
        SELECT price FROM Food_Subscription
        JOIN member_food_subscription ON Food_Subscription.Subscription_ID = member_food_subscription.plan_id
        WHERE member_food_subscription.member_id = %s
    ) AS combined
""", (trainee_id, trainee_id))
        
        

        result = cursor.fetchone()
        total_amount = result['total_amount'] if result['total_amount'] else 0.0

        if total_amount > 0.0:
            bill_date = date.today()
            due_date = bill_date + timedelta(days=30)
            cursor.execute("""
                INSERT INTO Bill (Trainee_ID, BillAmount, Bill_Date, Due_Date, BillStatus, BillMethod)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (trainee_id, total_amount, bill_date, due_date, False, "Pending"))
            con.commit()

        # Render success page with new Trainee ID
        return render_template('success_trainee_notadmin.html', trainee_id=trainee_id)

    except mysql.connector.Error as db_err:
        # Handle database errors
        return render_template('register_trainee.html', error=f"Database Error: {db_err}")

    except Exception as e:
        # Handle unexpected errors
        return render_template('register_trainee.html', error=f"An unexpected error occurred: {e}")

    finally:
        # Close database connection
        if 'cursor' in locals():
            cursor.close()
        if 'con' in locals():
            con.close()









@app.route('/trainees/registerjoin', methods=['GET'])
def register_trainee_pagejoin():
    return render_template('regTraineeJoin.html')



@app.route('/register_traineejoin', methods=['POST'])
def register_traineejoin():
    try:
        # Retrieve form data
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone_number = request.form.get('phone_number')
        ssn = request.form.get('snn')
        address = request.form.get('address')
        age = request.form.get('age')
        email = request.form.get('email')  # Add email retrieval
        password = request.form.get('password')  # Add password retrieval

        # Validate mandatory fields
        if not all([first_name, last_name, phone_number, ssn, address, age, email, password]):
            return render_template('regTraineeJoin.html', error="All fields are required.")

        # Establish database connection
        con = get_db_connection()
        cursor = con.cursor(dictionary=True)

        # Validate unique fields
        cursor.execute("SELECT * FROM Trainee WHERE Phone_Number = %s", (phone_number,))
        if cursor.fetchone():
            return render_template('regTraineeJoin.html', error="Phone number already exists.")

        cursor.execute("SELECT * FROM Trainee WHERE SNN = %s", (ssn,))
        if cursor.fetchone():
            return render_template('regTraineeJoin.html', error="SSN already exists.")

        cursor.execute("SELECT * FROM Trainee WHERE Email = %s", (email,))
        if cursor.fetchone():
            return render_template('regTraineeJoin.html', error="Email already exists.")

        # Retrieve the current maximum Trainee_ID
        cursor.execute("SELECT MAX(Trainee_ID) AS max_id FROM Trainee;")
        result = cursor.fetchone()
        max_id = result['max_id'] if result['max_id'] else 0
        trainee_id = max_id + 1

        # Hash the password before storing it
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Insert the new trainee
        query = """
        INSERT INTO Trainee (Trainee_ID, First_Name, Last_Name, Phone_Number, SNN, AddressTrainee, AgeTrainee, Email, Password, Registration_Date, is_deleted)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (trainee_id, first_name, last_name, phone_number, ssn, address, age, email, hashed_password, date.today(), False)
        cursor.execute(query, values)
        con.commit()

        # Generate a bill for the new trainee
        cursor.execute("""
    SELECT SUM(price) AS total_amount
    FROM (
        SELECT price FROM Membership
        JOIN Member_Membership ON Membership.membership_id = Member_Membership.membership_id
        WHERE Member_Membership.member_id = %s
        UNION ALL
        SELECT price FROM Food_Subscription
        JOIN member_food_subscription ON Food_Subscription.Subscription_ID = member_food_subscription.plan_id
        WHERE member_food_subscription.member_id = %s
    ) AS combined
""", (trainee_id, trainee_id))
        
        

        result = cursor.fetchone()
        total_amount = result['total_amount'] if result['total_amount'] else 0.0

        if total_amount > 0.0:
            bill_date = date.today()
            due_date = bill_date + timedelta(days=30)
            cursor.execute("""
                INSERT INTO Bill (Trainee_ID, BillAmount, Bill_Date, Due_Date, BillStatus, BillMethod)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (trainee_id, total_amount, bill_date, due_date, False, "Pending"))
            con.commit()

        # Render success page with new Trainee ID
        return render_template('joinUS.html', trainee_id=trainee_id)

    except mysql.connector.Error as db_err:
        # Handle database errors
        return render_template('regTraineeJoin.html', error=f"Database Error: {db_err}")

    except Exception as e:
        # Handle unexpected errors
        return render_template('regTraineeJoin.html', error=f"An unexpected error occurred: {e}")

    finally:
        # Close database connection
        if 'cursor' in locals():
            cursor.close()
        if 'con' in locals():
            con.close()


@app.route('/trainees/edit/<int:trainee_id>', methods=['GET', 'POST'])
def edit_trainee(trainee_id):
    con = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root1234',
        database='gym'
    )
    cursor = con.cursor(dictionary=True)

    if request.method == 'GET':
        cursor.execute("SELECT * FROM Trainee WHERE Trainee_ID = %s", (trainee_id,))
        trainee = cursor.fetchone()
        cursor.close()
        con.close()
        return render_template('edit_trainee.html', trainee=trainee)

    elif request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        address = request.form['address']
        phone_number = request.form['phone_number']
        ssn = request.form['snn']
        age = request.form['age']

        # Initialize error messages
        phone_error = None
        ssn_error = None

        # Check for duplicate phone number (excluding current trainee)
        cursor.execute(
            "SELECT * FROM Trainee WHERE Phone_Number = %s AND Trainee_ID != %s",
            (phone_number, trainee_id)
        )
        if cursor.fetchone():
            phone_error = "Phone number already exists."

        # Check for duplicate SSN (excluding current trainee)
        cursor.execute(
            "SELECT * FROM Trainee WHERE SNN = %s AND Trainee_ID != %s",
            (ssn, trainee_id)
        )
        if cursor.fetchone():
            ssn_error = "SSN already exists."

        # If there are errors, re-render the form with error messages
        if phone_error or ssn_error:
            cursor.execute("SELECT * FROM Trainee WHERE Trainee_ID = %s", (trainee_id,))
            trainee = cursor.fetchone()
            cursor.close()
            con.close()
            return render_template(
                'edit_trainee.html', trainee=trainee, phone_error=phone_error, ssn_error=ssn_error
            )

        # Update the trainee record
        query = """
        UPDATE Trainee
        SET First_Name = %s, Last_Name = %s, AddressTrainee = %s, Phone_Number = %s,
            SNN = %s, AgeTrainee = %s
        WHERE Trainee_ID = %s
        """
        values = (first_name, last_name, address, phone_number, ssn, age, trainee_id)
        cursor.execute(query, values)
        con.commit()
        cursor.close()
        con.close()
        return redirect('/trainees')


@app.route('/trainees/delete/<int:trainee_id>', methods=['POST'])
def delete_trainee(trainee_id):
    con = get_db_connection()
    cursor = con.cursor()

    try:
        # Perform a soft delete
        query = "UPDATE Trainee SET is_deleted = TRUE WHERE Trainee_ID = %s"
        cursor.execute(query, (trainee_id,))
        con.commit()

        return jsonify({"status": "success", "message": "Trainee disabled successfully."})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error: {e}"})
    finally:
        cursor.close()
        con.close()


@app.route('/trainees/restore/<int:trainee_id>', methods=['POST'])
def restore_trainee(trainee_id):
    con = get_db_connection()
    cursor = con.cursor()

    try:
        # Restore the trainee
        query = "UPDATE Trainee SET is_deleted = FALSE WHERE Trainee_ID = %s"
        cursor.execute(query, (trainee_id,))
        con.commit()

        return jsonify({"status": "success", "message": "Trainee restored successfully."})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error: {e}"})
    finally:
        cursor.close()
        con.close()




######################################################################

@app.route('/trainer/<int:trainer_id>/payments', methods=['GET'])
def trainer_payments(trainer_id):
    if 'trainer_id' not in session or session['trainer_id'] != trainer_id:
        return "Unauthorized access", 403

    con = get_db_connection()
    cursor = con.cursor(dictionary=True)

    try:
        # Verify trainer exists
        cursor.execute("SELECT First_Name, Last_Name, Salary FROM Trainer WHERE Trainer_ID = %s", (trainer_id,))
        trainer = cursor.fetchone()
        if not trainer:
            return f"No trainer found with ID {trainer_id}", 404

        trainer_name = f"{trainer['First_Name']} {trainer['Last_Name']}"
        salary = trainer['Salary']

        # Fetch payments for this trainer
        cursor.execute("""
            SELECT Payment_ID, PaymentAmount, Payment_Date, PaymentDue_Date, PaymentStatus
            FROM Payment
            WHERE Trainer_ID = %s and Exists
            ORDER BY PaymentDue_Date ASC
        """, (trainer_id,))
        payments = cursor.fetchall()

        return render_template(
            'trainer_payments.html',
            trainer_name=trainer_name,
            salary=salary,
            payments=payments
        )
    finally:
        cursor.close()
        con.close()
######################################################################

# Route for rendering the admin payment schedule template
@app.route('/admin')
def admin_dashboard():
    return render_template('admin_dashboard.html')



@app.route('/join_us', methods=['GET'])
def join_us():
    return render_template('joinUS.html')


@app.route('/trainer/<int:trainer_id>/profile', methods=['GET'])
def view_trainer_profile(trainer_id):
    try:
        # Establish database connection
        con = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root1234',
            database='gym'
        )
        cursor = con.cursor(dictionary=True)

        # Fetch the trainer's details using their ID
        cursor.execute("SELECT * FROM Trainer WHERE Trainer_ID = %s", (trainer_id,))
        trainer = cursor.fetchone()

        # If the trainer is not found, display an error
        if not trainer:
            return "Trainer not found", 404

        # Fetch classes conducted by the trainer
        cursor.execute("""
            SELECT Class.Class_Name, Class.Start_Time, Class.End_Time, Class.Capacity
            FROM Class
            WHERE Class.Trainer_ID = %s
        """, (trainer_id,))
        classes = cursor.fetchall()

        # Render the trainer's profile page
        return render_template('trainer_profile.html', trainer=trainer, classes=classes)

    except mysql.connector.Error as db_err:
        return f"Database Error: {db_err}", 500

    except Exception as e:
        return f"An unexpected error occurred: {e}", 500

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'con' in locals():
            con.close()


@app.route('/trainee/<int:trainee_id>/profile', methods=['GET'])
def view_trainee_profile(trainee_id):
    con = get_db_connection()
    cursor = con.cursor(dictionary=True)

    try:
        # Fetch trainee details
        cursor.execute("SELECT * FROM Trainee WHERE Trainee_ID = %s", (trainee_id,))
        trainee = cursor.fetchone()

        if not trainee:
            return f"No trainee found with ID {trainee_id}", 404

        # Render the profile page
        return render_template('trainee_profile.html', trainee=trainee)

    finally:
        cursor.close()
        con.close()


@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect('/')


from flask import request, redirect, url_for, render_template, session

@app.route('/trainer/login', methods=['POST'])
def trainer_login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    con = get_db_connection()
    cursor = con.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM Trainer WHERE Email = %s", (email,))
        trainer = cursor.fetchone()
        
        if not trainer:
            return render_template('joinUS.html', error="Trainer not found. Please sign up.")
        
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if trainer['Password'] != hashed_password:
            return render_template('joinUS.html', error="Invalid credentials.")
        
        session['trainer_id'] = trainer['Trainer_ID']
        return redirect(url_for('trainer_classes', trainer_id=trainer['Trainer_ID']))
    finally:
        cursor.close()
        con.close()




@app.route('/trainer/<int:trainer_id>/classes', methods=['GET'])
def trainer_classes(trainer_id):
    con = get_db_connection()
    cursor = con.cursor(dictionary=True)
    try:
        # Fetch classes assigned to the trainer
        query = """
        SELECT Class.Class_Name, Class.Start_Time, Class.End_Time, Class.Capacity, 
               Class.Class_ID,
               (SELECT COUNT(*) FROM Enrollment WHERE Enrollment.Class_ID = Class.Class_ID) AS Trainee_Count
        FROM Class
        WHERE Class.Trainer_ID = %s
        """
        cursor.execute(query, (trainer_id,))
        raw_classes = cursor.fetchall()

        # Map classes to days of the week (if needed)
        days_mapping = {
            "Monday": ["Strength Training", "Cardio"],
            "Tuesday": ["Crossfit", "Zumba"],
            "Wednesday": ["Strength Training", "Cardio"],
            "Thursday": ["Crossfit", "Zumba"],
            "Friday": ["Yoga", "Pilates"],
            "Saturday": ["Yoga", "Pilates"],
            "Sunday": ["Yoga", "Pilates"]
        }

        # Organize classes by day
        schedule = {day: [] for day in days_mapping.keys()}
        for cls in raw_classes:
            for day, class_names in days_mapping.items():
                if cls['Class_Name'] in class_names:
                    schedule[day].append(cls)

        # Pass the schedule and trainer_id to the template
        return render_template(
            'trainer_classes.html',
            schedule=schedule,
            trainer_id=trainer_id
        )
    finally:
        cursor.close()
        con.close()




@app.route('/trainee/login', methods=['POST'])
def trainee_login():
    email = request.form.get('email')
    password = request.form.get('password')

    con = get_db_connection()
    cursor = con.cursor(dictionary=True)

    try:
        # Log the email being used
        app.logger.info("Trainee login attempt with email: %s", email)

        # Check if trainee exists
        cursor.execute("SELECT * FROM Trainee WHERE LOWER(Email) = %s AND is_deleted = FALSE", (email.lower(),))

        trainee = cursor.fetchone()

        if not trainee:
            app.logger.error("Trainee not found for email: %s", email)
            return render_template('joinUS.html', error="Trainee not found. Please sign up.")

        # Verify password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if trainee['Password'] != hashed_password:
            app.logger.error("Invalid password for email: %s", email)
            return render_template('joinUS.html', error="Invalid credentials.")

        # Save session and redirect to dashboard
        session['trainee_id'] = trainee['Trainee_ID']
        app.logger.info("Trainee logged in successfully: %s", trainee['Trainee_ID'])
        return redirect(url_for('trainee_dashboard', trainee_id=trainee['Trainee_ID']))

    finally:
        cursor.close()
        con.close()


@app.route('/trainee/<int:trainee_id>/dashboard', methods=['GET'])
def trainee_dashboard(trainee_id):
    # Ensure the logged-in trainee is accessing their own dashboard
    if 'trainee_id' not in session or session['trainee_id'] != trainee_id:
        app.logger.error("Unauthorized access attempt for Trainee ID: %s", trainee_id)
        return "Unauthorized access", 403
    print(f"Accessing dashboard for trainee ID: {trainee_id}")

    con = get_db_connection()
    cursor = con.cursor(dictionary=True)

    try:
        # Fetch trainee details
        cursor.execute("SELECT * FROM Trainee WHERE Trainee_ID = %s", (trainee_id,))
        trainee = cursor.fetchone()

        if not trainee:
            app.logger.error("No trainee found with ID: %s", trainee_id)
            return f"No trainee found with ID {trainee_id}", 404

        # Fetch trainee's gym memberships
        cursor.execute("""
            SELECT Membership.membership_type, Membership.price, Member_Membership.start_date, Member_Membership.end_date 
            FROM Member_Membership
            JOIN Membership ON Member_Membership.membership_id = Membership.membership_id
            WHERE Member_Membership.member_id = %s
        """, (trainee_id,))
        gym_memberships = cursor.fetchall()

        # Fetch trainee's food subscriptions
        cursor.execute("""
            SELECT Food_Subscription.Subscription_Type, Food_Subscription.price, member_food_subscription.start_date, member_food_subscription.end_date
            FROM member_food_subscription
            JOIN Food_Subscription ON member_food_subscription.plan_id = Food_Subscription.Subscription_ID
            WHERE member_food_subscription.member_id = %s
        """, (trainee_id,))
        food_subscriptions = cursor.fetchall()

        # Prepare data for the dashboard
        dashboard_data = {
            "Gym_Memberships": gym_memberships,
            "Food_Subscriptions": food_subscriptions,
        }

        # Render the dashboard
        return render_template(
            'trainee_dashboard.html',
            trainee=trainee,
            dashboard_data=dashboard_data
        )
    finally:
        cursor.close()
        con.close()

from flask import Flask, render_template, redirect, url_for, request, flash
from flask_mysqldb import MySQL
import datetime

@app.route('/trainee/<int:trainee_id>/plans', methods=['GET'])
def plans(trainee_id):
    con = get_db_connection()
    cur = con.cursor(dictionary=True)
    
    try:
        # Fetch trainee details
        cur.execute("SELECT * FROM Trainee WHERE Trainee_ID = %s", (trainee_id,))
        trainee = cur.fetchone()
        if not trainee:
            return "Unauthorized access!", 403

        # Fetch gym plans
        cur.execute("SELECT * FROM Membership")
        plans = cur.fetchall()

        return render_template('plans.html', trainee=trainee, plans=plans)
    finally:
        cur.close()
        con.close()

@app.route('/trainee/<int:trainee_id>/subscribe/<int:membership_id>', methods=['POST'])
def subscribe_plan(trainee_id, membership_id):
    con = get_db_connection()
    cur = con.cursor(dictionary=True)

    try:
        # Validate trainee
        cur.execute("SELECT * FROM Trainee WHERE Trainee_ID = %s", (trainee_id,))
        trainee = cur.fetchone()
        if not trainee:
            return redirect(url_for('plans', trainee_id=trainee_id, message="Unauthorized access!"))

        # Validate membership plan
        cur.execute("SELECT * FROM Membership WHERE membership_id = %s", (membership_id,))
        plan = cur.fetchone()
        if not plan:
            return redirect(url_for('plans', trainee_id=trainee_id, message="Plan not found!"))

        # Check if already subscribed
        cur.execute("""
            SELECT * FROM Member_Membership 
            WHERE member_id = %s AND membership_id = %s
        """, (trainee_id, membership_id))
        existing_subscription = cur.fetchone()

        if existing_subscription:
            return redirect(url_for('plans', trainee_id=trainee_id, message="You are already subscribed to this plan!"))

        # Insert subscription into Member_Membership
        start_date = datetime.date.today()
        end_date = start_date + datetime.timedelta(days=30)  # Assuming a 1-month plan
        cur.execute("""
            INSERT INTO Member_Membership (member_id, membership_id, start_date, end_date, status)
            VALUES (%s, %s, %s, %s, 'active')
        """, (trainee_id, membership_id, start_date, end_date))

        # Generate or update a bill
        price = float(plan['price'])  # Assuming 'price' column exists in Membership table
        cur.execute("""
            SELECT Bill_ID, BillAmount FROM Bill 
            WHERE Trainee_ID = %s AND BillStatus = 0
        """, (trainee_id,))
        existing_bill = cur.fetchone()

        # Check if both gym and food subscriptions exist
        if has_food_and_gym(trainee_id, cur):
            price *= 0.85  # Apply 15% discount

        if existing_bill:
            # Check if the plan has already been added to the bill
            cur.execute("""
                SELECT * FROM member_food_subscription
                WHERE member_id = %s
            """, (trainee_id,))
            all_food_subscriptions = cur.fetchall()

            # Calculate only the new subscription amount to add
            new_amount = float(existing_bill['BillAmount']) + price
            cur.execute("""
                UPDATE Bill 
                SET BillAmount = %s
                WHERE Bill_ID = %s
            """, (new_amount, existing_bill['Bill_ID']))
            flash("Your bill has been updated with the new subscription!", 'success')
        else:
            # Create a new bill
            bill_date = datetime.date.today()
            due_date = bill_date + datetime.timedelta(days=30)
            cur.execute("""
                INSERT INTO Bill (Trainee_ID, BillAmount, Bill_Date, Due_Date, BillStatus, BillMethod)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (trainee_id, price, bill_date, due_date, False, "Pending"))
            flash("A new bill has been generated for your subscription!", 'success')

        # Commit changes
        con.commit()
        return redirect(url_for('plans', trainee_id=trainee_id, message="Subscription successful!"))

    except mysql.connector.Error as err:
        logging.error(f"Database error: {err}")
        return redirect(url_for('plans', trainee_id=trainee_id, message=f"Error updating subscription and bill: {err}"))
    finally:
        cur.close()
        con.close()

def has_food_and_gym(trainee_id, cur):
    # Check for active food subscription
    cur.execute("""
        SELECT COUNT(*) as count FROM member_food_subscription
        WHERE member_id = %s AND end_date >= CURDATE()
    """, (trainee_id,))
    food_count = cur.fetchone()['count']

    # Check for active gym subscription
    cur.execute("""
        SELECT COUNT(*) as count FROM member_membership
        WHERE member_id = %s AND end_date >= CURDATE()
    """, (trainee_id,))
    gym_count = cur.fetchone()['count']

    # Return True if both are active
    return food_count > 0 and gym_count > 0


@app.route('/trainee/<int:trainee_id>/food_subscriptions', methods=['GET'])
def view_food_subscriptions(trainee_id):
    con = get_db_connection()
    cur = con.cursor(dictionary=True)

    try:
        # Validate trainee
        cur.execute("SELECT * FROM Trainee WHERE Trainee_ID = %s", (trainee_id,))
        trainee = cur.fetchone()
        if not trainee:
            return "Unauthorized access!", 403

        # Fetch all food subscriptions
        cur.execute("SELECT * FROM Food_Subscription")
        subscriptions = cur.fetchall()

        return render_template('food_subscriptions.html', trainee=trainee, subscriptions=subscriptions)
    finally:
        cur.close()
        con.close()


@app.route('/trainee/<int:trainee_id>/subscribe_food/<int:subscription_id>', methods=['POST'])
def subscribe_food_plan(trainee_id, subscription_id):
    con = get_db_connection()
    cur = con.cursor(dictionary=True)

    try:
        # Validate trainee
        cur.execute("SELECT * FROM Trainee WHERE Trainee_ID = %s", (trainee_id,))
        trainee = cur.fetchone()
        if not trainee:
            return redirect(url_for('view_food_subscriptions', trainee_id=trainee_id, message="Unauthorized access!"))

        # Validate food subscription
        cur.execute("SELECT * FROM Food_Subscription WHERE Subscription_ID = %s", (subscription_id,))
        subscription = cur.fetchone()
        if not subscription:
            return redirect(url_for('view_food_subscriptions', trainee_id=trainee_id, message="Subscription plan not found!"))

        # Check if the trainee is already subscribed to the same plan
        cur.execute("""
            SELECT * FROM member_food_subscription 
            WHERE member_id = %s AND plan_id = %s
        """, (trainee_id, subscription_id))
        existing_subscription = cur.fetchone()
        if existing_subscription:
            return redirect(url_for('view_food_subscriptions', trainee_id=trainee_id, message="You are already subscribed to this plan!"))

        # Add new subscription
        start_date = datetime.date.today()
        end_date = start_date + datetime.timedelta(days=30)
        cur.execute("""
            INSERT INTO member_food_subscription (member_id, plan_id, start_date, end_date)
            VALUES (%s, %s, %s, %s)
        """, (trainee_id, subscription_id, start_date, end_date))

        # Generate or update a bill
        price = float(subscription['price'])
        cur.execute("""
            SELECT Bill_ID, BillAmount FROM Bill 
            WHERE Trainee_ID = %s AND BillStatus = 0
        """, (trainee_id,))
        existing_bill = cur.fetchone()

        # Check if both gym and food subscriptions exist
        if has_food_and_gym(trainee_id, cur):
            price *= 0.85  # Apply 15% discount

        if existing_bill:
            # Avoid recalculating the price of existing subscriptions
            cur.execute("""
                SELECT SUM(Food_Subscription.price) AS total_food_price
                FROM member_food_subscription
                JOIN Food_Subscription ON member_food_subscription.plan_id = Food_Subscription.Subscription_ID
                WHERE member_food_subscription.member_id = %s
            """, (trainee_id,))
            total_food_price = cur.fetchone()['total_food_price'] or 0.0

            # Calculate the additional price to add
            additional_price = price - total_food_price if price > total_food_price else 0.0
            new_amount = float(existing_bill['BillAmount']) + additional_price

            cur.execute("""
                UPDATE Bill 
                SET BillAmount = %s
                WHERE Bill_ID = %s
            """, (new_amount, existing_bill['Bill_ID']))
        else:
            # Create a new bill
            bill_date = datetime.date.today()
            due_date = bill_date + datetime.timedelta(days=30)
            cur.execute("""
                INSERT INTO Bill (Trainee_ID, BillAmount, Bill_Date, Due_Date, BillStatus, BillMethod)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (trainee_id, price, bill_date, due_date, False, "Pending"))

        con.commit()
        return redirect(url_for('view_food_subscriptions', trainee_id=trainee_id, message="Subscription successful!"))

    except mysql.connector.Error as err:
        return redirect(url_for('view_food_subscriptions', trainee_id=trainee_id, message=f"An error occurred: {err}"))
    finally:
        cur.close()
        con.close()


# @app.route('/trainer/<int:trainer_id>/classes', methods=['GET'])
# def trainer_classes(trainer_id):
#     con = get_db_connection()
#     cursor = con.cursor(dictionary=True)
#     try:
#         # Fetch classes assigned to the trainer
#         query = """
#         SELECT Class.Class_Name, Class.Start_Time, Class.End_Time, Class.Capacity, 
#                Class.Class_ID,
#                (SELECT COUNT(*) FROM Enrollment WHERE Enrollment.Class_ID = Class.Class_ID) AS Trainee_Count
#         FROM Class
#         WHERE Class.Trainer_ID = %s
#         """
#         cursor.execute(query, (trainer_id,))
#         raw_classes = cursor.fetchall()

#         # Map classes to days of the week (if needed)
#         days_mapping = {
#             "Monday": ["Strength Training", "Cardio"],
#             "Tuesday": ["Crossfit", "Zumba"],
#             "Wednesday": ["Strength Training", "Cardio"],
#             "Thursday": ["Crossfit", "Zumba"],
#             "Friday": ["Yoga", "Pilates"],
#             "Saturday": ["Yoga", "Pilates"],
#             "Sunday": ["Yoga", "Pilates"]
#         }

#         # Organize classes by day
#         schedule = {day: [] for day in days_mapping.keys()}
#         for cls in raw_classes:
#             for day, class_names in days_mapping.items():
#                 if cls['Class_Name'] in class_names:
#                     schedule[day].append(cls)

#         # Pass the schedule and trainer_id to the template
#         return render_template(
#             'trainer_classes.html',
#             schedule=schedule,
#             trainer_id=trainer_id
#         )
#     finally:
#         cursor.close()
#         con.close()

@app.route('/class/<int:class_id>/trainees', methods=['GET'])
def view_class_trainees(class_id):
    con = get_db_connection()
    cursor = con.cursor(dictionary=True)

    try:
        # Fetch class details
        cursor.execute("""
            SELECT Class_Name, Start_Time, End_Time 
            FROM Class 
            WHERE Class_ID = %s
        """, (class_id,))
        class_details = cursor.fetchone()
        if not class_details:
            return "Class not found!", 404

        # Fetch enrolled trainees
        cursor.execute("""
            SELECT Trainee.First_Name, Trainee.Last_Name, Trainee.Phone_Number 
            FROM Enrollment
            JOIN Trainee ON Enrollment.Trainee_ID = Trainee.Trainee_ID
            WHERE Enrollment.Class_ID = %s
        """, (class_id,))
        trainees = cursor.fetchall()

        # Render the page to display trainees
        return render_template(
            'view_trainees.html',
            class_details=class_details,
            trainees=trainees
        )
    finally:
        cursor.close()
        con.close()









@app.route('/food_plans', methods=['GET'])
def food_plans():
    # Render the food plans page. No login required.
    return render_template('food_plans.html')

@app.route('/gym_plans', methods=['GET'])
def gym_plans():
    # Render the food plans page. No login required.
    return render_template('gym_plans.html')



@app.route('/admin/login', methods=['POST'])
def admin_login():
    email = request.form.get('email')
    password = request.form.get('password')

    # Hardcoded admin credentials
    admin_credentials = {
        "malakmoqbel@gmail.com": "malak123",
        "leenahmad@gmail.com": "leen123"
    }

    # Check if the email exists in the hardcoded credentials
    if email in admin_credentials and password == admin_credentials[email]:
        # If credentials are correct, redirect to the admin dashboard
        return redirect('/admin_dashboard')
    else:
        # If credentials are incorrect, render the login page with an error
        error_message = "Invalid email or password. Access restricted to authorized admins."
        return render_template('joinUS.html', error=error_message)


# R# Route 1: Admin Dashboard
@app.route('/admin_dashboard', methods=['GET'])
def admin_dashboard_view():  # Renamed the function to avoid conflicts
    return render_template('admin_dashboard.html')

# Route 2: Admin Settings
@app.route('/admin_settings', methods=['GET'])
def admin_settings_view():  # Another unique function name
    return render_template('admin_settings.html')


@app.route('/trainee/profile/<int:trainee_id>', methods=['GET'])
def view_trainee_profileadmin(trainee_id):
    con = get_db_connection()
    cursor = con.cursor(dictionary=True)

    try:
        # Fetch trainee details
        cursor.execute("SELECT * FROM Trainee WHERE Trainee_ID = %s AND is_deleted = FALSE", (trainee_id,))

        trainee = cursor.fetchone()

        if not trainee:
            return f"No trainee found with ID {trainee_id}", 404

        # Render the profile page
        return render_template('profiletrainee.html', trainee=trainee)

    finally:
        cursor.close()
        con.close()


@app.route('/trainee/<int:trainee_id>/classes', methods=['GET'])
def trainee_classes(trainee_id):
    # Ensure the logged-in trainee is accessing their own classes
    if 'trainee_id' not in session or session['trainee_id'] != trainee_id:
        return "Unauthorized access", 403

    con = get_db_connection()
    cursor = con.cursor(dictionary=True)

    try:
        # Fetch classes grouped by day
        cursor.execute("""
            SELECT Class.Class_ID, Class.Class_Name, Class.Start_Time, Class.End_Time, 
                   Class.Capacity, Trainer.First_Name AS Trainer_First_Name, 
                   Trainer.Last_Name AS Trainer_Last_Name, Class.Day
            FROM Class
            JOIN Trainer ON Class.Trainer_ID = Trainer.Trainer_ID
        """)
        classes = cursor.fetchall()

        # Organize classes by day
        classes_by_day = {day: [] for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}
        for cls in classes:
            # Ensure Day is treated as a string key, not a set
            day = cls['Day']
            if isinstance(day, set):
                day = list(day)[0]  # Convert to a string (if it's a set, take the first item)
            if day in classes_by_day:
                classes_by_day[day].append(cls)

        # Render the classes page
        return render_template(
            'classes.html',
            trainee_id=trainee_id,
            classes_by_day=classes_by_day
        )
    finally:
        cursor.close()
        con.close()




# Function to get a database connection
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='root1234',
        database='gym'
    )

# Route for all trainees' schedules
@app.route('/trainee_schedules', methods=['GET'])
def all_trainees_schedules():
    search_name = request.args.get('search_name', '').lower()
    search_course = request.args.get('search_course', '').lower()
    search_time = request.args.get('search_time', '')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Base query
    query = '''
        SELECT 
            Trainee.Trainee_ID,
            Trainee.First_Name,
            Trainee.Last_Name,
            Class.Class_Name,
            Trainer.First_Name AS Trainer_First_Name,
            Trainer.Last_Name AS Trainer_Last_Name,
            Class.Start_Time,
            Class.End_Time,
            Enrollment.Date_Enrollment
        FROM Enrollment
        INNER JOIN Trainee ON Enrollment.Trainee_ID = Trainee.Trainee_ID
        INNER JOIN Class ON Enrollment.Class_ID = Class.Class_ID
        INNER JOIN Trainer ON Class.Trainer_ID = Trainer.Trainer_ID
    '''
    conditions = []
    values = []

    # Add conditions based on search inputs
    if search_name:
        conditions.append("(LOWER(Trainee.First_Name) LIKE %s OR LOWER(Trainee.Last_Name) LIKE %s)")
        values.extend([f"%{search_name}%", f"%{search_name}%"])
    if search_course:
        conditions.append("LOWER(Class.Class_Name) LIKE %s")
        values.append(f"%{search_course}%")
    if search_time:
        conditions.append("Class.Start_Time <= %s AND Class.End_Time >= %s")
        values.extend([search_time, search_time])

    # Combine conditions into the query
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " ORDER BY Trainee.Trainee_ID, Enrollment.Date_Enrollment"

    cursor.execute(query, values)
    schedules = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('all_trainees_schedules.html', schedules=schedules)

@app.route('/trainer/profile/<int:trainer_id>', methods=['GET'])
def view_trainer_profileadmin(trainer_id):
    try:
        # Establish database connection
        con = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root1234',
            database='gym'
        )
        cursor = con.cursor(dictionary=True)

        # Fetch the trainer's details using their ID
        cursor.execute("SELECT * FROM Trainer WHERE Trainer_ID = %s", (trainer_id,))
        trainer = cursor.fetchone()

        # If the trainer is not found, display an error
        if not trainer:
            return "Trainer not found", 404

        # Fetch classes conducted by the trainer
        cursor.execute("""
            SELECT Class.Class_Name, Class.Start_Time, Class.End_Time, Class.Capacity
            FROM Class
            WHERE Class.Trainer_ID = %s
        """, (trainer_id,))
        classes = cursor.fetchall()

        # Render the trainer's profile page
        return render_template('profiletrainer.html', trainer=trainer, classes=classes)

    except mysql.connector.Error as db_err:
        return f"Database Error: {db_err}", 500

    except Exception as e:
        return f"An unexpected error occurred: {e}", 500

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'con' in locals():
            con.close()


@app.route('/classes_admin', methods=['GET', 'POST'])
def classes_admin():
    con = get_db_connection()
    cursor = con.cursor(dictionary=True)

    query = """
        SELECT Class.Class_ID, Class.Class_Name, Class.Start_Time, Class.End_Time, Class.Capacity, Class.Day,
               Trainer.First_Name AS Trainer_First_Name, Trainer.Last_Name AS Trainer_Last_Name
        FROM Class
        INNER JOIN Trainer ON Class.Trainer_ID = Trainer.Trainer_ID
    """

    if request.method == 'POST':  # Handle search functionality
        search_query = request.form.get('search_query', '').strip()
        start_time = request.form.get('start_time', '').strip()
        end_time = request.form.get('end_time', '').strip()

        filters = []
        params = []

        if search_query:
            # Search by trainer or class name
            filters.append("(Class.Class_Name LIKE %s OR CONCAT(Trainer.First_Name, ' ', Trainer.Last_Name) LIKE %s)")
            params.extend([f"%{search_query}%", f"%{search_query}%"])

        if start_time and end_time:
            # Filter by time range
            filters.append("(Class.Start_Time >= %s AND Class.End_Time <= %s)")
            params.extend([start_time, end_time])

        if filters:
            query += " WHERE " + " AND ".join(filters)

        query += " ORDER BY Trainer.First_Name ASC, Trainer.Last_Name ASC"

        cursor.execute(query, params)
    else:
        # Default behavior (GET request)
        query += " ORDER BY Trainer.First_Name ASC, Trainer.Last_Name ASC"
        cursor.execute(query)

    classes = cursor.fetchall()
    cursor.close()
    con.close()

    return render_template('classes_admin.html', classes=classes)



@app.route('/edit_class/<int:class_id>', methods=['GET', 'POST'])
def edit_class(class_id):
    con = get_db_connection()
    cursor = con.cursor(dictionary=True)

    if request.method == 'POST':  # Handle form submission
        if 'cancel' in request.form:  # Handle cancel action
            cursor.close()
            con.close()
            return redirect('/classes_admin')

        # Update logic
        class_name = request.form['class_name']
        trainer_id = request.form['trainer_id']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        capacity = request.form['capacity']

        # Update the class in the database
        query = """
            UPDATE Class
            SET Class_Name = %s, Trainer_ID = %s, Start_Time = %s, End_Time = %s, Capacity = %s
            WHERE Class_ID = %s
        """
        cursor.execute(query, (class_name, trainer_id, start_time, end_time, capacity, class_id))
        con.commit()

        cursor.close()
        con.close()

        # Redirect to the admin classes page after successful update
        return redirect('/classes_admin')

    # Fetch class details for the GET request
    cursor.execute("SELECT * FROM Class WHERE Class_ID = %s", (class_id,))
    cls = cursor.fetchone()

    # Fetch all trainers
    cursor.execute("SELECT Trainer_ID, First_Name, Last_Name FROM Trainer")
    trainers = cursor.fetchall()

    cursor.close()
    con.close()

    return render_template('edit_class.html', cls=cls, trainers=trainers)


@app.route('/delete_class/<int:class_id>', methods=['POST'])
def delete_class(class_id):
    try:
        print(f"Deleting class with ID: {class_id}")  # Debugging info
        con = get_db_connection()
        cursor = con.cursor()

        # Delete associated records in Enrollment first
        delete_enrollment_query = "DELETE FROM Enrollment WHERE Class_ID = %s"
        cursor.execute(delete_enrollment_query, (class_id,))

        # Delete the class itself
        delete_class_query = "DELETE FROM Class WHERE Class_ID = %s"
        cursor.execute(delete_class_query, (class_id,))
        con.commit()

        cursor.close()
        con.close()

        return jsonify({"status": "success", "message": "Class deleted successfully."})

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({"status": "error", "message": f"Database error: {err}"})

    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"status": "error", "message": f"Unexpected error: {e}"})









@app.route('/trainer_payments', methods=['GET'])
def admintrainer_payments():
    con = get_db_connection()
    cursor = con.cursor(dictionary=True)

    query = """
        SELECT Payment.Payment_ID, Payment.PaymentAmount, Payment.Payment_Date, Payment.PaymentDue_Date, 
               Payment.PaymentStatus, Trainer.First_Name AS Trainer_First_Name, Trainer.Last_Name AS Trainer_Last_Name
        FROM Payment
        INNER JOIN Trainer ON Payment.Trainer_ID = Trainer.Trainer_ID
    """
    cursor.execute(query)
    payments = cursor.fetchall()

    cursor.close()
    con.close()

    return render_template('adminTrainerPayment.html', payments=payments)


@app.route('/update_payment_status/<int:payment_id>', methods=['POST'])
def update_payment_status(payment_id):
    new_status = request.form['status']

    try:
        con = get_db_connection()
        cursor = con.cursor()

        query = "UPDATE Payment SET PaymentStatus = %s WHERE Payment_ID = %s"
        cursor.execute(query, (new_status, payment_id))
        con.commit()

        cursor.close()
        con.close()

        return redirect('/trainer_payments')
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return f"Error: {err}", 500


@app.route('/trainee/<int:trainee_id>/cart', methods=['GET'])
def view_cart(trainee_id):
    con = get_db_connection()
    cursor = con.cursor(dictionary=True)
    try:
        # Validate trainee
        cursor.execute("SELECT * FROM Trainee WHERE Trainee_ID = %s", (trainee_id,))
        trainee = cursor.fetchone()
        if not trainee:
            return "Unauthorized access!", 403

        # Fetch reserved classes
        cursor.execute("""
            SELECT Class.Class_Name, Class.Start_Time, Class.End_Time, 
                   Trainer.First_Name AS Trainer_First_Name, Trainer.Last_Name AS Trainer_Last_Name,
                   Class.Capacity, 
                   (SELECT COUNT(*) FROM Enrollment WHERE Enrollment.Class_ID = Class.Class_ID) AS enrolled_count
            FROM Enrollment
            JOIN Class ON Enrollment.Class_ID = Class.Class_ID
            JOIN Trainer ON Class.Trainer_ID = Trainer.Trainer_ID
            WHERE Enrollment.Trainee_ID = %s
        """, (trainee_id,))
        reserved_classes = cursor.fetchall()

  

        # Fetch subscribed food plans
        cursor.execute("""
            SELECT Food_Subscription.Subscription_Type, Food_Subscription.price, 
                   member_food_subscription.start_date, member_food_subscription.end_date
            FROM member_food_subscription
            JOIN Food_Subscription ON member_food_subscription.plan_id = Food_Subscription.Subscription_ID
            WHERE member_food_subscription.member_id = %s
        """, (trainee_id,))
        food_subscriptions = cursor.fetchall()

        # Fetch subscribed gym plans
        cursor.execute("""
            SELECT Membership.membership_type, Membership.price, Member_Membership.start_date, 
                   Member_Membership.end_date
            FROM Member_Membership
            JOIN Membership ON Member_Membership.membership_id = Membership.membership_id
            WHERE Member_Membership.member_id = %s
        """, (trainee_id,))
        gym_plans = cursor.fetchall()

        # Calculate total amounts
        total_food_price = sum(float(plan['price']) for plan in food_subscriptions)
        total_gym_price = sum(float(plan['price']) for plan in gym_plans)
        total_amount = total_food_price + total_gym_price

        # Check if discount is applicable
        has_discount = total_food_price > 0 and total_gym_price > 0
        discounted_amount = total_amount * 0.85 if has_discount else total_amount

        # Render the cart template
        return render_template(
            'cart.html',
            trainee=trainee,
            reserved_classes=reserved_classes,
            food_subscriptions=food_subscriptions,
            gym_plans=gym_plans,
            total_amount=total_amount,
            has_discount=has_discount,
            discounted_amount=discounted_amount
        )
    finally:
        cursor.close()
        con.close()




@app.route('/reserve_class/<int:class_id>/<int:trainee_id>', methods=['POST'])
def reserve_class(class_id, trainee_id):
    con = get_db_connection()
    cursor = con.cursor(dictionary=True)

    try:
        # Check if the class is already reserved by the trainee
        cursor.execute("""
            SELECT * FROM Enrollment 
            WHERE Class_ID = %s AND Trainee_ID = %s
        """, (class_id, trainee_id))
        existing_reservation = cursor.fetchone()

        if existing_reservation:
            return jsonify({
                "status": "error",
                "message": "You have already reserved this class."
            })

        # Check class capacity
        cursor.execute("""
            SELECT Capacity FROM Class WHERE Class_ID = %s
        """, (class_id,))
        class_info = cursor.fetchone()

        if not class_info or class_info['Capacity'] <= 0:
            return jsonify({
                "status": "error",
                "message": "This class is full or does not exist."
            })

        # Add the reservation
        cursor.execute("""
            INSERT INTO Enrollment (Trainee_ID, Class_ID, Date_Enrollment)
            VALUES (%s, %s, %s)
        """, (trainee_id, class_id, date.today()))

        # Update the class capacity
        cursor.execute("""
            UPDATE Class SET Capacity = Capacity - 1 WHERE Class_ID = %s
        """, (class_id,))
        con.commit()

        return jsonify({
            "status": "success",
            "message": "Class reserved successfully!",
            "redirect_url": url_for('reservation_success', trainee_id=trainee_id, class_id=class_id)
        })

    except mysql.connector.Error as err:
        return jsonify({
            "status": "error",
            "message": f"Database error: {err}"
        })

    finally:
        cursor.close()
        con.close()


@app.route('/reservation_success/<int:trainee_id>/<int:class_id>', methods=['GET'])
def reservation_success(trainee_id, class_id):
    con = get_db_connection()
    cursor = con.cursor(dictionary=True)

    try:
        # Fetch class details
        cursor.execute("""
            SELECT Class.Class_Name, Trainer.First_Name AS Trainer_First_Name, Trainer.Last_Name AS Trainer_Last_Name
            FROM Class
            JOIN Trainer ON Class.Trainer_ID = Trainer.Trainer_ID
            WHERE Class.Class_ID = %s
        """, (class_id,))
        cls = cursor.fetchone()

        if not cls:
            return f"Class with ID {class_id} not found.", 404

        return render_template(
            'reservation_success.html',
            trainee_id=trainee_id,
            class_id=class_id,
            class_name=cls["Class_Name"],
            trainer_name=f"{cls['Trainer_First_Name']} {cls['Trainer_Last_Name']}"
        )
    finally:
        cursor.close()
        con.close()


@app.route('/delete_reservation/<int:trainee_id>/<int:class_id>', methods=['POST'])
def delete_reservation(trainee_id, class_id):
    con = get_db_connection()
    cursor = con.cursor(dictionary=True)

    try:
        # Delete reservation
        cursor.execute("""
            DELETE FROM Enrollment
            WHERE Trainee_ID = %s AND Class_ID = %s
        """, (trainee_id, class_id))
        con.commit()
        return redirect(url_for('trainee_classes', trainee_id=trainee_id))
    finally:
        cursor.close()
        con.close()




@app.route('/admin/trainee_bills', methods=['GET'])
def view_trainee_bills():
    con = get_db_connection()
    cursor = con.cursor(dictionary=True)

    try:
        # Fetch all bills with trainee details
        query = """
        SELECT Bill.Bill_ID, Bill.BillAmount, Bill.Bill_Date, Bill.Due_Date, Bill.BillStatus, 
               Bill.BillMethod, Trainee.First_Name, Trainee.Last_Name
        FROM Bill
        JOIN Trainee ON Bill.Trainee_ID = Trainee.Trainee_ID
        ORDER BY Bill.Due_Date ASC;
        """
        cursor.execute(query)
        bills = cursor.fetchall()
        logging.debug(f"Fetched bills for admin view: {bills}")

        return render_template('admin_trainee_bills.html', bills=bills)
    finally:
        cursor.close()
        con.close()



@app.route('/update_bill_status/<int:bill_id>', methods=['POST'])
def update_bill_status(bill_id):
    new_status = request.form.get('bill_status') == 'on'  # Checkbox returns 'on' if checked
    con = get_db_connection()
    cursor = con.cursor()

    try:
        query = "UPDATE Bill SET BillStatus = %s WHERE Bill_ID = %s"
        cursor.execute(query, (new_status, bill_id))
        con.commit()

        return redirect(url_for('view_trainee_bills'))
    finally:
        cursor.close()
        con.close()


from datetime import date, timedelta
from flask import request, jsonify

@app.route('/generate_bill/<int:trainee_id>', methods=['POST'])
def generate_bill(trainee_id):
    con = get_db_connection()
    cursor = con.cursor(dictionary=True)

    try:
        # Calculate total bill amount
        cursor.execute("""
            SELECT SUM(price) AS total_amount
            FROM (
                SELECT price FROM GymPlans WHERE Trainee_ID = %s
                UNION ALL
                SELECT price FROM FoodSubscriptions WHERE Trainee_ID = %s
            ) AS combined
        """, (trainee_id, trainee_id))
        result = cursor.fetchone()
        total_amount = result['total_amount'] if result['total_amount'] else 0.0

        if total_amount == 0.0:
            return jsonify({
                "status": "error",
                "message": "No plans or subscriptions found for this trainee."
            })

        # Create a new bill entry
        bill_date = date.today()
        due_date = bill_date + timedelta(days=30)  # Example: due in 30 days
        cursor.execute("""
            INSERT INTO Bill (Trainee_ID, BillAmount, Bill_Date, Due_Date, BillStatus, BillMethod)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (trainee_id, total_amount, bill_date, due_date, False, "Pending"))

        con.commit()

        return jsonify({
            "status": "success",
            "message": "Bill generated successfully.",
            "bill_amount": total_amount,
            "bill_date": bill_date.strftime('%Y-%m-%d'),
            "due_date": due_date.strftime('%Y-%m-%d')
        })

    except mysql.connector.Error as err:
        return jsonify({
            "status": "error",
            "message": f"Database error: {err}"
        })
    finally:
        cursor.close()
        con.close()



@app.route('/admin/report', methods=['GET'])
def admin_report():
    con = get_db_connection()
    cur = con.cursor(dictionary=True)
    try:
        # 1. Most Popular Class
        cur.execute("""
            SELECT Class_Name, COUNT(*) AS total_enrollments
            FROM Enrollment
            JOIN Class ON Enrollment.Class_ID = Class.Class_ID
            GROUP BY Class_Name
            ORDER BY total_enrollments DESC
            LIMIT 1;
        """)
        most_popular_class = cur.fetchone()

        # 2. Revenue Generated
        cur.execute("""
            SELECT SUM(BillAmount) AS total_revenue FROM Bill WHERE BillStatus = 1;
        """)
        revenue_generated = cur.fetchone()

        # 3. Inactive Trainees
        cur.execute("""
            SELECT COUNT(*) AS inactive_trainees
            FROM Trainee
            WHERE Trainee_ID NOT IN (
                SELECT DISTINCT Trainee_ID FROM Enrollment
            );
        """)
        inactive_trainees = cur.fetchone()

        # 4. Busiest Day
        cur.execute("""
            SELECT Day, COUNT(*) AS total_classes
            FROM Class
            GROUP BY Day
            ORDER BY total_classes DESC
            LIMIT 1;
        """)
        busiest_day = cur.fetchone()

        # 5. Total Number of Trainers
        cur.execute("SELECT COUNT(*) AS total_trainers FROM Trainer where Trainer.is_deleted = False;")
        total_trainers = cur.fetchone()

        # 6. Total Number of Trainees
        cur.execute("SELECT COUNT(*) AS total_trainees FROM Trainee;")
        total_trainees = cur.fetchone()

        # 7. Average Class Size
        cur.execute("""
            SELECT round(AVG(enrollment_count)) AS average_class_size
            FROM (
                SELECT Class_ID, COUNT(*) AS enrollment_count
                FROM Enrollment
                GROUP BY Class_ID
            ) AS enrollment_stats;
        """)
        average_class_size = cur.fetchone()

        # 8. Paid vs. Unpaid Bills
        cur.execute("""
            SELECT 
                SUM(CASE WHEN BillStatus = 1 THEN 1 ELSE 0 END) AS paid,
                SUM(CASE WHEN BillStatus = 0 THEN 1 ELSE 0 END) AS unpaid
            FROM Bill;
        """)
        bills_status = cur.fetchone()

        # 9. Trainer Engagement
        cur.execute("""
            SELECT 
                CONCAT(Trainer.First_Name, ' ', Trainer.Last_Name) AS trainer_name,
                COUNT(Class.Class_ID) AS classes_count
            FROM Trainer
            JOIN Class ON Trainer.Trainer_ID = Class.Trainer_ID
            WHERE Trainer.is_deleted = FALSE
            GROUP BY Trainer.Trainer_ID, Trainer.First_Name, Trainer.Last_Name
            ORDER BY classes_count DESC;
        """)
        trainer_engagement = cur.fetchall() or []

# 10. Trainee Growth Over Time
        cur.execute("""
            SELECT 
                DATE_FORMAT(Registration_Date, '%Y-%m') AS month,
                COUNT(Trainee_ID) AS total_trainees
            FROM Trainee
             GROUP BY month
             ORDER BY month;
        """)
        trainee_growth = cur.fetchall() or []
        cur.execute("""
            SELECT 
                (SELECT SUM(BillAmount) FROM Bill WHERE BillStatus = 1) AS total_revenue,
                (SELECT SUM(PaymentAmount) FROM Payment WHERE PaymentStatus like "%paid%") AS total_expenses
        """)
        finance_data = cur.fetchone()
        print(trainer_engagement)  # Should output a list of dictionaries
        print(trainee_growth)
        print(busiest_day)
        print(finance_data)

        # Pass the data to the template
        return render_template(
            'admin_report.html',
            most_popular_class=most_popular_class,
            revenue_generated=revenue_generated,
            inactive_trainees=inactive_trainees,
            busiest_day=busiest_day,
            total_trainers=total_trainers,
            total_trainees=total_trainees,
            average_class_size=average_class_size,
            bills_status=bills_status,
            trainer_engagement=trainer_engagement,
            trainee_growth=trainee_growth,
            finance_data=finance_data 
        )
    finally:
        cur.close()
        con.close()



if __name__ == '__main__':
    print("connection to DB...")
    app.run(debug=True)
