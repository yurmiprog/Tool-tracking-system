
from json import tool

import mysql.connector
from abc import ABC, abstractmethod
from datetime import datetime
import time


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="tool_tracker_system"
    )


class toolItem:
    def __init__(self, id, name, tool, time):
        self.__id = id
        self.__name = name
        self.__tool = tool
        self.__time = time

    # Getters
    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_tool(self):
        return self.__tool

    def get_time(self):
        return self.__time

    # Setters
    def set_name(self, name):
        self.__name = name

    def set_tool(self, tool):
        self.__tool = tool

    def set_time(self, time):
        self.__time = time

class tooltracker:
    def add_tool(self, tool):
        
        cursor = db.cursor()

        sql = """
        INSERT INTO tools (id, tool_name, time_started, time_returned)
        VALUES (%s, %s, %s, %s)
        """

        val = (
            tool.get_id(),
            tool.get_tool(),
            tool.get_time(),
            None
        )

        cursor.execute(sql, val)
        db.commit()
        cursor.close()

        print("Tool added successfully!")

    def return_tool(self, id):
        cursor = db.cursor()

        sql = """
        UPDATE tools
        SET time_returned = %s
        WHERE id = %s AND time_returned IS NULL
        """

        cursor.execute(sql, (datetime.now(), id))
        db.commit()

        if cursor.rowcount > 0:
            print("Tool returned successfully!")
        else:
            print("Tool not found or already returned.")

        cursor.close()


    def update_tool(self, id, name, tool, time):   
        cursor = db.cursor()

        sql = """
        UPDATE tools
        SET tool_name = %s, time_started = %s
        WHERE id = %s
        """

        cursor.execute(sql, (tool, time, id))
        db.commit()

        if cursor.rowcount > 0:
            print("Tool updated successfully!")
        else:
            print("Tool not found.")

        cursor.close()

    def return_tool(self, id):#
        cursor = db.cursor()
        sql = "SELECT * FROM tools WHERE id = %s"
        val = (id,)
        cursor.execute(sql, val)
        result = cursor.fetchone()
        cursor.close()

        if result:
            return result
        else:
            print('tool not found')
            return None
        
    def Choices(self, choice):
        if choice == '1':
            id = input("Enter tool ID: ")
            name = input("Enter tool name: ")
            tool_name = input("Enter tool type: ")
            time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_tool = toolItem(id, name, tool_name, time)
            self.add_tool(new_tool)
        elif choice == '2':
            id = input("Enter tool ID to remove: ")
            self.remove_tool(id)
        elif choice == '3':
            id = input("Enter tool ID to update: ")
            name = input("Enter new tool name: ")
            tool_name = input("Enter new tool type: ")
            time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.update_tool(id, name, tool_name, time)
        elif choice == '4':
            id = input("Enter tool ID to return: ")
            result = self.return_tool(id)
            if result:
                print(f"Tool ID: {result[0]}, Name: {result[1]}, Type: {result[2]}, Time: {result[3]}")
        elif choice == '5':
            print("Exiting the Tool Tracking System.")
            exit()
        else:
            print("Invalid choice. Please try again.")
tracker = tooltracker()

while True:
    print("\nWelcome to the Tool Tracking System")
    print("1. Add Tool")
    print("2. Remove Tool")
    print("3. Update Tool")
    print("4. View Tool")
    print("5. Exit")

    choice = input("Enter your choice: ")

    try:
        if not tracker.Choices(choice):
            break

    except ValueError:
        print("Please enter a valid tool ID.")

    except mysql.connector.Error as error:
        db.rollback()
        print("Database error:", error)

db.close()


