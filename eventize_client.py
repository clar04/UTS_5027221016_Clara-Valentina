import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import mysql.connector

class EventScheduler:
    def __init__(self): #koneksi db
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="clar",
            password="ngantuqbgd44",
            database="eventize"
        )
        self.cursor = self.db_connection.cursor()

    def create_event(self, event_data):
        query = "INSERT INTO events (event_name, description, date, location) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(query, event_data)
        self.db_connection.commit()
        return "Event created successfully"

    def read_events(self):
        query = "SELECT id, event_name, description, date, location FROM events"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def update_event(self, event_id, event_data):
        query = "UPDATE events SET event_name = %s, description = %s, date = %s, location = %s WHERE id = %s"
        self.cursor.execute(query, (*event_data, event_id))
        self.db_connection.commit()
        return "Event updated successfully"

    def delete_event(self, event_id):
        query = "DELETE FROM events WHERE id = %s"
        self.cursor.execute(query, (event_id,))
        self.db_connection.commit()
        return "Event deleted successfully"

    def search_events(self, search_query):
        query = "SELECT id, event_name, description, date, location FROM events WHERE event_name LIKE %s OR description LIKE %s OR location LIKE %s"
        self.cursor.execute(query, (f"%{search_query}%", f"%{search_query}%", f"%{search_query}%"))
        return self.cursor.fetchall()

event_manager = EventScheduler()

def create_event_clicked(): #dijalankan saat button create diklik, ngambil input
    event_name = event_name_entry.get()
    event_date = event_date_entry.get_date()
    event_description = event_description_entry.get("1.0", tk.END).strip()
    event_location = event_location_entry.get()

    if event_name and event_date and event_description and event_location:
        try:
            response = event_manager.create_event((event_name, event_description, event_date, event_location))
            messagebox.showinfo("Info", response)
            clear_inputs()
            retrieve_events_clicked()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error occurred: {err}")
    else:
        messagebox.showerror("Error", "Please fill in all fields")

def retrieve_events_clicked():
    try:
        events = event_manager.read_events()
        if events:
            event_list.delete(0, tk.END)
            for event in events:
                event_list.insert(tk.END, f"ID: {event[0]} | Name: {event[1]} | Date: {event[3]} | Location: {event[4]} | Description: {event[2]}")
        else:
            messagebox.showinfo("Info", "No events found")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error occurred: {err}")

def update_event_clicked():
    event_name = event_name_entry.get()
    event_date = event_date_entry.get_date()
    event_description = event_description_entry.get("1.0", tk.END).strip()
    event_location = event_location_entry.get()
    event_id = event_id_entry.get()

    if event_name and event_date and event_description and event_location and event_id:
        try:
            response = event_manager.update_event(event_id, (event_name, event_description, event_date, event_location))
            messagebox.showinfo("Info", response)
            retrieve_events_clicked()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error occurred: {err}")
    else:
        messagebox.showerror("Error", "Please fill in all fields")

def delete_event_clicked():
    event_id = event_id_entry.get()
    if event_id:
        try:
            response = event_manager.delete_event(event_id)
            messagebox.showinfo("Info", response)
            clear_inputs()
            retrieve_events_clicked()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error occurred: {err}")
    else:
        messagebox.showerror("Error", "Please select an event to delete")

def search_events_clicked():
    search_query = search_entry.get()
    if search_query:
        try:
            events = event_manager.search_events(search_query)
            if events:
                event_list.delete(0, tk.END)
                for event in events:
                    event_list.insert(tk.END, f"ID: {event[0]} | Name: {event[1]} | Date: {event[3]} | Location: {event[4]} | Description: {event[2]}")
            else:
                messagebox.showinfo("Info", "No events found")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error occurred: {err}")
    else:
        messagebox.showerror("Error", "Please enter search query")

def clear_inputs():
    event_id_entry.config(state=tk.NORMAL)
    event_id_entry.delete(0, tk.END)
    event_name_entry.delete(0, tk.END)
    event_date_entry.set_date("")
    event_description_entry.delete("1.0", tk.END)
    event_location_entry.delete(0, tk.END)
    search_entry.delete(0, tk.END)
    event_list.delete(0, tk.END)

def on_event_select(event): #dijalankan saat event dipilih di list box
    try:
        selected_index = event_list.curselection()[0]
        selected_event = event_list.get(selected_index)
        event_details = selected_event.split(" | ")
        event_id = event_details[0].replace("ID: ", "")
        event_name = event_details[1].replace("Name: ", "")
        event_date = event_details[2].replace("Date: ", "")
        event_location = event_details[3].replace("Location: ", "")
        event_description = event_details[4].replace("Description: ", "")

        clear_inputs()
        event_id_entry.insert(0, event_id)
        event_name_entry.insert(0, event_name)
        event_date_entry.set_date(event_date)
        event_location_entry.insert(0, event_location)
        event_description_entry.insert("1.0", event_description)
    except IndexError:
        pass

root = tk.Tk()
root.title("Event Scheduler")

# Labels and Entries
tk.Label(root, text="Event ID:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
event_id_entry = tk.Entry(root)
event_id_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Event Name:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
event_name_entry = tk.Entry(root)
event_name_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Date:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
event_date_entry = DateEntry(root, date_pattern="yyyy-mm-dd")
event_date_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="Location:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
event_location_entry = tk.Entry(root)
event_location_entry.grid(row=3, column=1, padx=5, pady=5)

tk.Label(root, text="Description:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
event_description_entry = tk.Text(root, height=4, width=30)
event_description_entry.grid(row=4, column=1, padx=5, pady=5)

# Buttons
create_button = tk.Button(root, text="Create Event", command=create_event_clicked)
create_button.grid(row=5, column=0, padx=5, pady=5)

retrieve_button = tk.Button(root, text="Retrieve Events", command=retrieve_events_clicked)
retrieve_button.grid(row=5, column=1, padx=5, pady=5)

update_button = tk.Button(root, text="Update Event", command=update_event_clicked)
update_button.grid(row=5, column=2, padx=5, pady=5)

delete_button = tk.Button(root, text="Delete Event", command=delete_event_clicked)
delete_button.grid(row=5, column=3, padx=5, pady=5)

# Search Entry
tk.Label(root, text="Search Events:").grid(row=6, column=0, padx=5, pady=5, sticky="e")
search_entry = tk.Entry(root)
search_entry.grid(row=6, column=1, padx=5, pady=5)

# Search Button
search_button = tk.Button(root, text="Search", command=search_events_clicked)
search_button.grid(row=6, column=2, padx=5, pady=5)

# Listbox
event_list = tk.Listbox(root, width=80)
event_list.grid(row=7, column=0, columnspan=4, padx=5, pady=5)
event_list.bind('<<ListboxSelect>>', on_event_select)

# Reload Button
reload_button = tk.Button(root, text="Clear", command=clear_inputs)
reload_button.grid(row=8, column=0, columnspan=4, padx=5, pady=5)

root.mainloop()
