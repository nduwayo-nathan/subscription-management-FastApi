import psycopg2
from faker import Faker
from io import StringIO
import random
import time

# Initialize Faker instance
fake = Faker()

# Database connection settings
DB_CONFIG = {
    "dbname": "fastApi_subscription",
    "user": "postgres",
    "password": "ABC123%%%",
    "host": "localhost",
    "port": 5432
}

# Function to generate a batch of plans with unique names
def generate_plans(batch_size, start_id):
    plans = []
    for i in range(batch_size):
        # Generate a unique name using a counter or random number to ensure uniqueness
        name = f"{fake.bs()}_{start_id + i}"  # Append the index or unique id to make the name unique
        price = random.randint(1, 1000)  # Random price between 1 and 1000
        description = fake.sentence(nb_words=10)  # Generate a short description
        plans.append((name, price, description))
    return plans

# Function to perform bulk insert using COPY
def bulk_insert_plans(plans, connection):
    try:
        with connection.cursor() as cursor:
            buffer = StringIO()
            # Prepare each plan for insertion
            for plan in plans:
                buffer.write(f"{plan[0]}\t{plan[1]}\t{plan[2]}\n")
            buffer.seek(0)

            # Use COPY command to insert into the plans table
            cursor.copy_from(buffer, "plans", sep="\t", columns=("name", "price", "description"))
            connection.commit()  # Commit the transaction
            print(f"Inserted {len(plans)} plans successfully.")
    except Exception as e:
        print(f"Error during bulk insert: {e}")
        connection.rollback()

# Main function to generate and insert plans
def generate_and_insert_plans(batch_size, total_plans):
    try:
        # Connect to the database
        connection = psycopg2.connect(**DB_CONFIG)
        print("Connected to the database.")

        total_inserted = 0
        start_id = 0  # Start ID for unique names

        while total_inserted < total_plans:
            # Generate a batch of plans with unique names
            plans = generate_plans(batch_size, start_id)
            # Perform bulk insert
            bulk_insert_plans(plans, connection)

            total_inserted += len(plans)
            start_id += batch_size  # Increment the start_id for the next batch

            print(f"Progress: {total_inserted}/{total_plans} plans inserted.")
        
        print("All plans inserted successfully.")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        if connection:
            connection.close()
            print("Database connection closed.")

if __name__ == "__main__":
    # Generate and insert 500,000 plans in batches of 10,000
    start_time = time.time()
    generate_and_insert_plans(batch_size=10000, total_plans=500000)
    print(f"Execution time: {time.time() - start_time:.2f} seconds")
