import grpc
from concurrent import futures
import tkinter as tk
from tkinter import messagebox
import mysql.connector
import logging

import eventize_pb2
import eventize_pb2_grpc

class EventScheduler(eventize_pb2_grpc.EventServiceServicer):
    #logging database
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        try:
            self.db_connection = mysql.connector.connect(
                host="localhost",
                user="clar",
                password="ngantuqbgd44",
                database="eventize"
            )
            self.cursor = self.db_connection.cursor()
            self.logger.info("Database connection successful")
        except Exception as e:
            self.logger.error("Failed to connect to database: %s", e)

# handle rpc create event, bikin query sql buat input tabel event
    def CreateEvent(self, request, context):
        try:
            query = "INSERT INTO events (name, description, date) VALUES (%s, %s, %s)"
            self.cursor.execute(query, (request.event_name, request.event_description, request.event_date))
            self.db_connection.commit()
            return eventize_pb2.CreateItemResponse(success=True, message="Event created successfully")
        except mysql.connector.Error as err:
            self.logger.error("Failed to create event: %s", err)
            return eventize_pb2.CreateItemResponse(success=False, message=f"Failed to create event: {err}")

# jalanin server grpc
def serve():
    try:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        eventize_pb2_grpc.add_EventServiceServicer_to_server(EventScheduler(), server)
        server.add_insecure_port('[::]:50051')
        server.start()
        server.wait_for_termination()
    except Exception as e:
        logging.error("Server error: %s", e)

if __name__ == '__main__':
    serve()
