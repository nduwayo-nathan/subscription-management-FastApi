import psycopg2
from faker import Faker
from io import StringIO
import time

# Initialize Faker
fake = Faker()

# Database configuration
DB_CONFIG = {
    "dbname": "fastApi_subscription",
    "user": "postgres",
    "password": "ABC123%%%",
    "host": "localhost",  # or your database host
    "port": 5432          # Default PostgreSQL port
}

# Function to generate a batch of unique users
def generate_unique_users(batch_size):
    users = set()
    while len(users) < batch_size:
        username = fake.unique.user_name()
        email = fake.unique.email()
        password = fake.password(length=12)
        users.add((username, email, password))
    return list(users)

# Function to insert users into the database using COPY
def bulk_insert_users(users, connection):
    try:
        with connection.cursor() as cursor:
            # Prepare data for COPY
            buffer = StringIO()
            for user in users:
                buffer.write(f"{user[0]}\t{user[1]}\t{user[2]}\n")
            buffer.seek(0)

            # Copy data to the database
            cursor.copy_from(buffer, "users", sep="\t", columns=("username", "email", "password"))
            connection.commit()
            print(f"Inserted {len(users)} users successfully.")
    except Exception as e:
        print(f"Error during bulk insert: {e}")
        connection.rollback()

# Main function to generate and insert users
def generate_users(batch_size, total_users):
    try:
        # Connect to the database
        connection = psycopg2.connect(**DB_CONFIG)
        print("Connected to the database.")

        total_inserted = 0
        while total_inserted < total_users:
            # Generate a batch of unique users
            batch_users = generate_unique_users(batch_size)
            # Insert the batch into the database
            bulk_insert_users(batch_users, connection)
            total_inserted += len(batch_users)
            print(f"Progress: {total_inserted}/{total_users} users inserted.")
        
        print("All users inserted successfully.")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        if connection:
            connection.close()
            print("Database connection closed.")

# Run the script
if __name__ == "__main__":
    # Generate 500,000 users in batches of 10,000
    start_time = time.time()
    generate_users(batch_size=10000, total_users=500000)
    print(f"Execution time: {time.time() - start_time:.2f} seconds")
