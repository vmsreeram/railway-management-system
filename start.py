from datetime import time
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlalchemy
import datetime
from sqlalchemy.engine import create_engine
from sqlalchemy.sql import text

class PostgresqlDB:
    def __init__(self,user_name,password,host,port,db_name):
        self.user_name = user_name
        self.password = password
        self.host = host
        self.port = port
        self.db_name = db_name
        self.engine = self.create_db_engine()

    def create_db_engine(self):
        try:
            db_uri = f"postgresql+psycopg2://{self.user_name}:{self.password}@{self.host}:{self.port}/{self.db_name}"
            return create_engine(db_uri)
        except Exception as err:
            raise RuntimeError(f'Failed to establish connection -- {err}') from err

    def execute_dql_commands(self,stmnt,values=None):
        try:
            with self.engine.connect() as conn:
                if values is not None:
                    result = conn.execute(text(stmnt),values)
                else:
                    result = conn.execute(text(stmnt))
            return result
        except Exception as err:
            print(f'Failed to execute dql commands -- {err}')
    
    def execute_ddl_and_dml_commands(self,stmnt,values=None):
        connection = self.engine.connect()
        trans = connection.begin()
        try:
            if values is not None:

                result = connection.execute(text(stmnt),values)
            else:
                result = connection.execute(text(stmnt))
            trans.commit()
            connection.close()
            print('Command executed successfully.')
        except Exception as err:
            trans.rollback()
            print(f'Failed to execute ddl and dml commands -- {err}')

USER_NAME = 'postgres'
PASSWORD = 'postgres'
PORT = 5432
DATABASE_NAME = 'railwaymanagementsys'
HOST = 'localhost'

try:
    db = PostgresqlDB(user_name=USER_NAME,
                        password=PASSWORD,
                        host=HOST,port=PORT,
                        db_name=DATABASE_NAME)
    engine = db.engine
    # print('Arun')
except:
    print('Not working')
class RailwayManagementSystemGUI:
    def __init__(self, master):
        # Initialize the GUI window
        self.master = master
        self.master.title("Railway Management System")
        
        self.main_page()
    
    def main_page(self):
        
        # Create a frame for the main menu
        self.main_menu_frame = Frame(self.master)
        self.main_menu_frame.pack(pady=50)
        Label(self.main_menu_frame, text="Welcome to Railway Management System", font=("Helvetica", 20)).pack(side=TOP, pady=20)

        # Button to login page
        Button(self.main_menu_frame, text="Login", font=("Helvetica", 16), command=self.login_page).pack(pady=10)

        #Button to add a reservation page
        Button(self.main_menu_frame, text="Reserve Seat", font=("Helvetica", 16), command=self.reserve_tickets_page).pack(pady=10)
        
        # Button to display trains between stations
        Button(self.main_menu_frame, text="Trains Between Stations", font=("Helvetica", 16), command=self.trains_between_stations).pack(pady=10)
        
        # Button to display trains between stations
        # Button(self.main_menu_frame, text="Availability", font=("Helvetica", 16), command=self.num_avail).pack(pady=10)

        #Button to add a cancellation page
        Button(self.main_menu_frame, text="Cancel Seat", font=("Helvetica", 16), command=self.cancel_seat_page).pack(pady=10)

    def trains_between_stations(self):
        # Clear the main menu frame
        self.main_menu_frame.destroy()

        # Create a frame to hold the input widgets
        self.input_frame = Frame(self.master)
        self.input_frame.pack(side=LEFT, padx=10, pady=10)

        # Create labels and entry boxes for the source and destination stations
        self.source_station_label = Label(self.input_frame, text="Source Station:")
        self.source_station_label.grid(row=0, column=0)
        self.source_station_entry = Entry(self.input_frame)
        self.source_station_entry.grid(row=0, column=1)

        self.destination_station_label = Label(self.input_frame, text="Destination Station:")
        self.destination_station_label.grid(row=1, column=0)
        self.destination_station_entry = Entry(self.input_frame)
        self.destination_station_entry.grid(row=1, column=1)

        # Create a label and dropdown menu for the day of the week
        self.day_of_week_label = Label(self.input_frame, text="Day of Week:")
        self.day_of_week_label.grid(row=2, column=0)
        self.day_of_week = StringVar()
        self.day_of_week_dropdown = OptionMenu(self.input_frame, self.day_of_week, *["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        self.day_of_week_dropdown.grid(row=2, column=1)

        # Create a button to execute the query
        self.execute_button = Button(self.input_frame, text="Find Trains", command=self.display_trains)
        self.execute_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Create a frame to hold the output widget
        self.output_frame = Frame(self.master)
        self.output_frame.pack(side=RIGHT, padx=10, pady=10)

        # Create a label for the output widget
        self.train_list_label = Label(self.output_frame, text="Trains Between Stations:")
        self.train_list_label.pack()

        # Create a button to go back to the home page
        self.reserve_button = Button(self.input_frame, text="Go Back", command=lambda: (self.input_frame.destroy(),self.output_frame.destroy(), self.main_page()))
        self.reserve_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Create a Treeview widget for the output
        self.train_treeview = ttk.Treeview(self.output_frame, columns=(0, 1, 2, 3, 4, 5,6,7,8), show='headings', height=15)
        self.train_treeview.pack()
        self.train_treeview.heading(0, text='Train Number')
        self.train_treeview.heading(3, text='Days of week')
        self.train_treeview.heading(1, text='Source Station')
        self.train_treeview.heading(2, text='Destination Station')
        self.train_treeview.heading(4, text='Source Arrival Time')
        self.train_treeview.heading(5, text='Source Dept Time')
        self.train_treeview.heading(6, text='Dest Arrival Time')
        self.train_treeview.heading(7, text='Dest Dept Time')
        self.train_treeview.heading(8, text='Day Number')

        # Bind a function to the Train Number column to execute the num_available query
        def on_train_click(event):
            selection = self.train_treeview.selection()
            if selection:
                # print('Inside num')
                train_num = self.train_treeview.item(selection[0])['values'][0]
                source_station = self.source_station_entry.get()
                dest_station = self.destination_station_entry.get()
                day_of_week = self.day_of_week.get()
                query = f"SELECT num_available({train_num}, '{source_station}', '{dest_station}', '06-05-2023', 'CC')"
                # Execute the query and display the result
                results = db.execute_dql_commands(query)
                x=list(results)
                value = x[0][0]
                messagebox.showinfo("Available Seats", f"Number of available seats on train {train_num}: {value}")

        self.train_treeview.bind("<Button-1>", on_train_click)


    # # works well, but o/p in terminal
    # def display_trains(self):
    #     # Get the values from the entry boxes and dropdown menu
    #     source_station = self.source_station_entry.get()
    #     destination_station = self.destination_station_entry.get()
    #     day_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"].index(self.day_of_week.get())

    #     # Execute the query and display the results
    #     query = f"SELECT * FROM TrainsBtwStns('{source_station}', '{destination_station}', {day_of_week});"
    #     results = db.execute_dql_commands(query)
    #     for row in results:
    #         row_list = list(row)
    #         for i in range(4, 8):
    #             if isinstance(row_list[i], time):
    #                 row_list[i] = row_list[i].strftime("%H:%M")
    #             elif row_list[i] is None:
    #                 row_list[i] = 'N/A'
    #         print(tuple(row_list))
    
    def display_trains(self):
        # Get the values from the entry boxes and dropdown menu
        source_station = self.source_station_entry.get()
        destination_station = self.destination_station_entry.get()
        day_of_week = ["Sunday", "Saturday", "Friday","Thursday","Wednesday","Tuesday","Monday"   ].index(self.day_of_week.get())

        # Execute the query and display the results
        try:
            query = f"SELECT * FROM TrainsBtwStns('{source_station}', '{destination_station}', {day_of_week});"
            results = db.execute_dql_commands(query)
            self.train_treeview.delete(*self.train_treeview.get_children())
            for row in results:
                row_list = list(row)
                for i in range(4, 9):
                    if isinstance(row_list[i], time):
                        row_list[i] = row_list[i].strftime("%H:%M")
                    elif row_list[i] is None:
                        row_list[i] = 'N/A'
                #print(type(row_list[3]))
                # Convert integer to binary and pad to 7 digits
                binary = bin(row_list[3])[2:].zfill(7)

                # Create a list of days of the week in order
                days_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

                # Create a list of selected days based on the binary string
                selected_days = [days_of_week[i] for i in range(7) if binary[i] == '1']

                # Join the selected days into a comma-separated string
                days_string = ', '.join(selected_days)
                if binary=='1111111':
                    days_string='All days'
                row_list[3]=days_string
                # Print the string of selected days
                #print(days_string)
                self.train_treeview.insert('', END, values=row_list)
        except:
            print('NO')


    def login_page(self):
        # Clear the main menu frame
        self.main_menu_frame.destroy()

        # Create a frame for the login page
        self.login_frame = Frame(self.master)
        self.login_frame.pack(pady=50)
        Label(self.login_frame, text="Login Page", font=("Helvetica", 20)).pack(side=TOP, pady=20)

        # Create a username label and entry box
        Label(self.login_frame, text="Username", font=("Helvetica", 16)).pack(pady=10)
        self.username_entry = Entry(self.login_frame, font=("Helvetica", 16))
        self.username_entry.pack(pady=10)

        # Create a password label and entry box
        Label(self.login_frame, text="Password", font=("Helvetica", 16)).pack(pady=10)
        self.password_entry = Entry(self.login_frame, font=("Helvetica", 16), show="*")
        self.password_entry.pack(pady=10)

        # Create a button to submit the login information
        Button(self.login_frame, text="Login", font=("Helvetica", 16), command=self.login).pack(pady=10)

        #Button to go back to the home page
        Button(self.login_frame, text="Go Back", font=("Helvetica", 16), command=lambda: (self.login_frame.destroy(), self.main_page())).pack(pady=10)
        
    def login(self):
        # Get the values from the entry boxes
        username = self.username_entry.get()
        password = self.password_entry.get()

        # TODO: Implement login functionality

        # Show a message box to indicate successful login
        messagebox.showinfo("Success", "Login successful.")
        
    def reserve_tickets_page(self):

        # Clear the main menu frame
        self.main_menu_frame.destroy()

        # Create a frame to hold the input widgets
        self.input_frame = Frame(self.master)
        self.input_frame.pack(side=LEFT, padx=10, pady=10)

        # Create labels and entry boxes for all the required information
        self.tno_label = Label(self.input_frame, text="Train Number:")
        self.tno_label.grid(row=0, column=0)
        self.tno_entry = Entry(self.input_frame)
        self.tno_entry.grid(row=0, column=1)

        self.src_label = Label(self.input_frame, text="Source Station Code:")
        self.src_label.grid(row=1, column=0)
        self.src_entry = Entry(self.input_frame)
        self.src_entry.grid(row=1, column=1)

        self.dst_label = Label(self.input_frame, text="Destination Station Code:")
        self.dst_label.grid(row=2, column=0)
        self.dst_entry = Entry(self.input_frame)
        self.dst_entry.grid(row=2, column=1)
        
        self.doj_label= Label(self.input_frame, text="Date of journey (DD-MM-YYYY):")
        self.doj_label.grid(row=3, column=0)
        self.doj_entry = Entry(self.input_frame)
        self.doj_entry.grid(row=3, column=1)
        
        # Create a label and dropdown menu for the day of the week
        self.ctyp_entry_label = Label(self.input_frame, text="Coach Type:")
        self.ctyp_entry_label.grid(row=4, column=0)
        self.ctyp_entry = StringVar()
        self.ctyp_entry_rolldown = OptionMenu(self.input_frame, self.ctyp_entry, *["CC", "3AC"])
        self.ctyp_entry_rolldown.grid(row=4, column=1)
        
        self.uid_label= Label(self.input_frame, text="User ID:")
        self.uid_label.grid(row=5, column=0)
        self.uid_entry = Entry(self.input_frame)
        self.uid_entry.grid(row=5, column=1)
        
        self.txn_label= Label(self.input_frame, text="Transaction ID:")
        self.txn_label.grid(row=6, column=0)
        self.txn_entry = Entry(self.input_frame)
        self.txn_entry.grid(row=6, column=1)
        
        self.pass_label= Label(self.input_frame, text="Passenger IDs (comma-separated):")
        self.pass_label.grid(row=7, column=0)
        self.pass_entry = Entry(self.input_frame)
        self.pass_entry.grid(row=7, column=1)
        
        # Create a button to execute the query
        self.reserve_button = Button(self.input_frame, text="Reserve Seats", command=self.reserve_seat)
        self.reserve_button.grid(row=8, column=0, columnspan=2, pady=10)
        
        self.result_label= Label(self.input_frame, text="PNR No:")
        self.result_label.grid(row=9, column=0)
        self.result_output = Entry(self.input_frame)
        self.result_output.grid(row=9, column=1)
        
        #Button to go back to the home page
        self.reserve_button = Button(self.input_frame, text="Go Back", command=lambda: (self.input_frame.destroy(),self.main_page()))
        self.reserve_button.grid(row=10, column=0, columnspan=2, pady=10)
        
        
    def reserve_seat(self):
        tno = self.tno_entry.get()
        src = self.src_entry.get()
        dst = self.dst_entry.get()
        doj = self.doj_entry.get()
        c_typ = self.ctyp_entry.get()
        usr_id = self.uid_entry.get()
        trxn_id = self.txn_entry.get()
        pass_ids = self.pass_entry.get()
        
        if not tno or not src or not dst or not doj or not c_typ or not usr_id or not trxn_id or not pass_ids:
            messagebox.showerror("Error", "Please enter all required fields")
            return
        try:
            doj = datetime.datetime.strptime(doj, "%d-%m-%Y")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use DD-MM-YYYY")
            return
        query1 = f"CALL reserve_seat('{tno}', '{src}', '{dst}', '{doj}', '{c_typ}', {usr_id}, {trxn_id}, '{pass_ids}');"
        values = {"tno": tno, "src": src, "dst": dst, "doj": doj, "c_typ": c_typ, "usr_id": usr_id, "trxn_id": trxn_id, "pass_ids": pass_ids}
        try:
            db.execute_ddl_and_dml_commands(query1, values)
            messagebox.showinfo("Success", "Reservation successful.")
            query = "SELECT pnr_no FROM pass_tkt WHERE pass_id = :pass_id;"
            values = {"pass_id": pass_ids[0]}
            results = db.execute_dql_commands(query, values)
            print(results[0])
            self.result_output.config(text=f"PNR: {results[0][0]}")
        except Exception as e:
            self.result_output.config(text="Reservation failed. Error: " + str(e))
    
    
    def cancel_seat_page(self):

        # Clear the main menu frame
        self.main_menu_frame.destroy()

        # Create a frame to hold the input widgets
        self.input_frame = Frame(self.master)
        self.input_frame.pack(side=LEFT, padx=10, pady=10)
        
        self.pnr_no_label= Label(self.input_frame, text="PNR No:")
        self.pnr_no_label.grid(row=0, column=0)
        self.pnr_no_entry = Entry(self.input_frame)
        self.pnr_no_entry.grid(row=0, column=1)
        
        self.uid_label= Label(self.input_frame, text="User ID:")
        self.uid_label.grid(row=1, column=0)
        self.uid_entry = Entry(self.input_frame)
        self.uid_entry.grid(row=1, column=1)
        
        self.pass_label= Label(self.input_frame, text="Passenger IDs (comma-separated):")
        self.pass_label.grid(row=2, column=0)
        self.pass_entry = Entry(self.input_frame)
        self.pass_entry.grid(row=2, column=1)
        
        # Create a button to execute the query
        self.cancel_button = Button(self.input_frame, text="Cancel seats", command=self.cancel_seat)
        self.cancel_button.grid(row=3, column=0, columnspan=2, pady=10)
        
        self.result_label= Label(self.input_frame, text="Cancellation status:")
        self.result_label.grid(row=4, column=0)
        self.result_output = Entry(self.input_frame)
        self.result_output.grid(row=4, column=1)
        
        #Button to go back to the home page
        self.reserve_button = Button(self.input_frame, text="Go Back", command=lambda: (self.input_frame.destroy(), self.main_page()))
        self.reserve_button.grid(row=5, column=0, columnspan=2, pady=10)
        
        
    def cancel_seat(self):
        pnr_no = self.pnr_no_entry.get()
        usr_id = self.uid_entry.get()
        pass_ids = self.pass_entry.get()
        
        if not pnr_no or not usr_id or not pass_ids:
            messagebox.showerror("Error", "Please enter all required fields")
            return
        query1 = f"CALL cancel_seat('{pnr_no}', {usr_id}, '{pass_ids}');"
        values = {"pnr_no": pnr_no,"usr_id": usr_id, "pass_ids": pass_ids}
        try:
            db.execute_ddl_and_dml_commands(query1, values)
            # Show a message box to indicate successful reservation
            messagebox.showinfo("Success", "Cancellation successful.")
            self.result_output.config(text="Cancellation successful. Refunded: " )
        except:
            self.result_output.config(text="Cancellation failed. Error")
        

def main():
    root=Tk()
    root.title("railway-management-system")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    scrSizeStr=str(int(screen_width))+'x'+str(int(screen_height))
    root.geometry(scrSizeStr)
    app = RailwayManagementSystemGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
