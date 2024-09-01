import tkinter as tk
from tkinter import messagebox
import cx_Oracle
import tkinter.ttk as ttk

class TrainStationApp:
    def __init__(self, root):
        print("Initializing App")
        self.root = root
        self.root.title("Train Station App")
        self.create_gui()

        # Connect to the Oracle database
        self.connection = cx_Oracle.connect(
            user='system',
            password='hr',
            dsn='localhost:1521/xe'
        )
        self.cursor = self.connection.cursor()



    def create_gui(self):
        print("Creating GUI")
        # Set a colorful background
        self.root.configure(bg='#3498db')

        # Create Home Window
        self.home_frame = tk.Frame(self.root, bg='#2c3e50', padx=20, pady=20, borderwidth=5, relief='ridge')
        self.home_frame.pack(padx=20, pady=20)

        label = tk.Label(self.home_frame, text="Train Station", font=("Helvetica", 18, "bold"), bg='#2c3e50', fg='white')
        label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        tk.Button(self.home_frame, text="Reserve Ticket", command=self.reserve_ticket, width=20, bg='#3498db', fg='white').grid(row=1, column=0, pady=10)
        tk.Button(self.home_frame, text="Manage Database", command=self.manage_database, width=20, bg='#3498db', fg='white').grid(row=1, column=1, pady=10)

    def reserve_ticket(self):
        print("Reserving Ticket")
        # Create Reservation Window
        reservation_window = tk.Toplevel(self.root)
        reservation_window.title("Reservation")

        # Add widgets for destination, time, train number, etc.
        # You can use Entry, Combobox, etc., for user input.

        tk.Button(reservation_window, text="Generate Ticket", command=self.generate_ticket, width=20, bg='#3498db', fg='white').pack(pady=10)

    def generate_ticket(self):
        print("Generating Ticket")
        # Create Ticket Window
        ticket_window = tk.Toplevel(self.root)
        ticket_window.title("Ticket")

        tk.Label(ticket_window, text="Ticket Information Goes Here", font=("Helvetica", 14), bg='#2ecc71', fg='white').pack(pady=10)

        # Display the selected information for the ticket
        # You can use labels to display the ticket details.
    def get_tables(self):
            # Retrieve the list of tables from the data dictionary view ALL_TABLES
            self.cursor.execute(
                "SELECT table_name FROM ALL_TABLES WHERE owner = 'ADMIN'")  # Replace 'ADMIN' with your schema name
            tables = [row[0] for row in self.cursor.fetchall()]
            return tables

    def manage_database(self):
        # Create Database Management Window
        database_window = tk.Toplevel(self.root)
        database_window.title("Database Management")

        # Get the list of tables from the database
        tables = self.get_tables()

        # Create a Combobox to select the table
        table_combobox = ttk.Combobox(database_window, values=tables)
        table_combobox.set("Select Table")
        table_combobox.pack(pady=10)

        # Buttons for actions
        tk.Button(database_window, text="Insert Record", command=lambda: self.insert_record_window(table_combobox.get()), width=20, bg='#3498db', fg='white').pack(pady=10)
        tk.Button(database_window, text="Update Record", command=lambda: self.update_record_window(table_combobox.get()), width=20, bg='#3498db', fg='white').pack(pady=10)
        tk.Button(database_window, text="Delete Record", command=lambda: self.delete_record_window(table_combobox.get()), width=20, bg='#3498db', fg='white').pack(pady=10)
        tk.Button(database_window, text="Select Table", command=lambda: self.select_table_info(table_combobox.get()), width=20, bg='#3498db', fg='white').pack(pady=10)

    def get_table_data(self, table_name, columns):
        # Retrieve data for the selected table
        self.cursor.execute(f"SELECT {', '.join(columns)} FROM ADMIN.{table_name} ORDER BY {columns[0]} ASC")
        data = [row for row in self.cursor.fetchall()]
        return data

    def select_table_info(self, selected_table):
        # Create Select Table Information Window
        select_info_window = tk.Toplevel(self.root)
        select_info_window.title(f"Table Information for {selected_table}")

        # Get the column names and data for the selected table
        columns = self.get_table_columns(selected_table)
        data = self.get_table_data(selected_table, columns)

        # Display column names
        tk.Label(select_info_window, text="Column Names:", font=("Helvetica", 12, "bold")).pack(pady=5)
        tk.Label(select_info_window, text=", ".join(columns)).pack(pady=5)

        # Display data in a table
        tree = ttk.Treeview(select_info_window, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
        for row in data:
            tree.insert("", "end", values=row)
        tree.pack(pady=10)

    def insert_record_window(self, selected_table):
        # Create Insert Record Window
        insert_window = tk.Toplevel(self.root)
        insert_window.title(f"Insert Record into {selected_table}")

        # Get the column names for the selected table
        columns = self.get_table_columns(selected_table)

        # Add Entry widgets for each column in the selected table
        entry_widgets = []
        for column in columns:
            tk.Label(insert_window, text=f"{column}:").pack()
            entry = tk.Entry(insert_window)
            entry.pack()
            entry_widgets.append(entry)

        tk.Button(insert_window, text="Insert",
                  command=lambda: self.insert_record(selected_table, *[entry.get() for entry in entry_widgets]),
                  width=20, bg='#3498db', fg='white').pack(pady=10)

    def update_record_window(self, selected_table):
        # Create Update Record Window
        update_window = tk.Toplevel(self.root)
        update_window.title(f"Update Record in {selected_table}")

        # Get the column names for the selected table
        columns = self.get_table_columns(selected_table)

        # Add Entry widgets for each column in the selected table
        entry_widgets = []
        for column in columns:
            tk.Label(update_window, text=f"{column}:").pack()
            entry = tk.Entry(update_window)
            entry.pack()
            entry_widgets.append(entry)

        # Button to select record for updating
        tk.Button(update_window, text="Select Record",
                  command=lambda: self.select_record_for_update(selected_table, entry_widgets),
                  width=20, bg='#3498db', fg='white').pack(pady=10)

    def delete_record_window(self, selected_table):
        # Create Delete Record Window
        delete_window = tk.Toplevel(self.root)
        delete_window.title(f"Delete Record from {selected_table}")

        # Get the column names for the selected table
        columns = self.get_table_columns(selected_table)

        # Add Entry widget for the primary key
        tk.Label(delete_window, text=f"{columns[0]}:").pack()  # Assuming the first column is the primary key
        primary_key_entry = tk.Entry(delete_window)
        primary_key_entry.pack()

        tk.Button(delete_window, text="Delete",
                  command=lambda: self.delete_record(selected_table, primary_key_entry.get()),
                  width=20, bg='#3498db', fg='white').pack(pady=10)

    def insert_record(self, selected_table, *values):
        # Insert record into the selected table
        try:
            columns = self.get_table_columns(selected_table)
            columns_str = ', '.join(columns)
            values_str = ', '.join([':' + str(i + 1) for i in range(len(values))])

            # Use placeholders for column names and values dynamically
            query = f"INSERT INTO ADMIN.{selected_table} ({columns_str}) VALUES ({values_str})"
            self.cursor.execute(query, values)
            self.connection.commit()

            messagebox.showinfo("Success", "Record inserted successfully.")
        except cx_Oracle.Error as e:
            print(e)  # Print the Oracle error for debugging purposes
            messagebox.showerror("Error", f"Error inserting record: {e}")

    def select_record_for_update(self, selected_table, entry_widgets):
            try:
                # Retrieve the primary key column name
                primary_key_column = self.get_table_columns(selected_table)[0]

                # Get the values from entry widgets
                values = [entry.get() for entry in entry_widgets]

                # Use the primary key value for selection
                primary_key_value = values[0]

                # Retrieve the selected record for updating
                query = f"SELECT * FROM ADMIN.{selected_table} WHERE {primary_key_column} = :1"
                self.cursor.execute(query, (primary_key_value,))
                record = self.cursor.fetchone()

                # Populate entry widgets with the current values
                for i, value in enumerate(record):
                    entry_widgets[i].insert(0, value)

                # Button to execute the update
                tk.Button(entry_widgets[0].master, text="Update",
                            command=lambda: self.update_record(selected_table, primary_key_value,
                                                                *[entry.get() for entry in entry_widgets[1:]]),
                            width=20, bg='#3498db', fg='white').pack(pady=10)

            except cx_Oracle.Error as e:
                print(e)  # Print the Oracle error for debugging purposes
                messagebox.showerror("Error", f"Error selecting record for update: {e}")

    def update_record(self, selected_table, primary_key_value, *values):
        try:
            columns = self.get_table_columns(selected_table)

            # Exclude primary key from the set_clause
            set_clause = ', '.join([f"{col} = :{i + 1}" for i, col in enumerate(columns) if col != columns[0]])

            # Use primary key in the criteria_clause
            criteria_clause = f"{columns[0]} = :{len(values) + 1}"

            print("Update Values:", values)  # Add this line for debugging

            query = f"UPDATE ADMIN.{selected_table} SET {set_clause} WHERE {criteria_clause}"
            print("SQL Query:", query)  # Add this line for debugging

            # Include primary key in the values for criteria
            self.cursor.execute(query, (*values, primary_key_value))
            self.connection.commit()

            messagebox.showinfo("Success", "Record updated successfully.")
        except cx_Oracle.Error as e:
            print(e)  # Print the Oracle error for debugging purposes
            messagebox.showerror("Error", f"Error updating record: {e}")

    def delete_record(self, selected_table, primary_key_value):
        # Delete record from the selected table
        try:
            columns = self.get_table_columns(selected_table)

            # Use placeholders for column names and values dynamically
            query = f"DELETE FROM ADMIN.{selected_table} WHERE {columns[0]} = :1"
            self.cursor.execute(query, (primary_key_value,))
            self.connection.commit()

            messagebox.showinfo("Success", "Record deleted successfully.")
        except cx_Oracle.Error as e:
            print(e)  # Print the Oracle error for debugging purposes
            messagebox.showerror("Error", f"Error deleting record: {e}")

    def get_table_columns(self, table_name):
                # Retrieve the column names for the selected table
                self.cursor.execute(
                    f"SELECT column_name FROM all_tab_columns WHERE table_name = '{table_name.upper()}'")
                columns = [row[0] for row in self.cursor.fetchall()]
                return columns

    def __del__(self):
            # Close the cursor and connection when the application is closed
            self.cursor.close()
            self.connection.close()

# Start the Tkinter application
print("Starting Tkinter application")
root = tk.Tk()
app = TrainStationApp(root)
root.mainloop()
