import csv
import os
from datetime import datetime, date

pri_order = {"High": 1, "Medium": 2, "Low": 3}

def clear_terminal() -> None:
    if (os.name == "nt"):
        os.system("cls")
    else:
        os.system("clear")
clear_terminal()

def save_tasks(tasks):
    with open("sample.csv", "w", newline="") as file:
      writer = csv.DictWriter(file, fieldnames=["name", "course", "deadline", "priority", "completed"])
      writer.writeheader()
      writer.writerows(tasks)
tasks = []
if os.path.exists("sample.csv"):
    with open("sample.csv", "r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            row["completed"] = (row["completed"] == "True")
            tasks.append(row)

#for task in tasks:
#    print(task["name"], "-", task["course"], "- due", task["deadline"])

def add_task(tasks):
   clear_terminal()
   name = ""
   course = ""
   deadline = ""
   priority = ""
   while (True):
      all_fields_added = True
      choice = input(
            "Select action:\n"+
            "1: Enter task name\n"+
            "2: Enter course name\n"+
            "3: Enter Deadline date\n"+
            "4: Enter priority level\n"+
            "5: Cancel adding task and exit\n"+
            "6: Save task and exit\n"+
            "Action: ")
      match choice:
         case "1":
            name = input("Task name: ")
            clear_terminal()
         case "2":
            course = input("Course name: ")
            clear_terminal()
         case "3":
            while True:
               deadline = input("Deadline (YYYY-MM-DD): ")
               try:
                  datetime.strptime(deadline, "%Y-%m-%d")
                  break
               except ValueError:
                  print("Incorrect format, try again!")
            clear_terminal()
         case "4":
            while True:
               priority = input("Priority (High-Medium-Low): ").capitalize()
               if priority not in pri_order:
                  print("Enter a valid priority order (High-Medium-Low): ")
               else:
                  break
            clear_terminal()
         case "5":
            clear_terminal()
            return "Task not added."
         case "6":
            clear_terminal()
            count = 0
            for i in [name,course,deadline,priority]:
               count += 1
               if (not i):
                  match count:
                     case 1:
                        all_fields_added = False
                        print("Missing name")
                     case 2:
                        all_fields_added = False
                        print("Missing course")
                     case 3:
                        all_fields_added = False
                        print("Missing deadline")
                     case 4:
                        all_fields_added = False
                        print("Missing priority")
            if (all_fields_added):
               task = {
                   "name": name,
                   "course": course,
                   "deadline": deadline,
                   "priority": priority,
                   "completed": False
                }  
               tasks.append(task)
               save_tasks(tasks)
               clear_terminal()
               return "Task added!"

def view_task(tasks):
   for task in tasks:
      print(task["name"], " - ", task["course"], "- ", task["deadline"])
   print("")

def complete_task(tasks):
   name = input("Enter task name: ")
   for task in tasks:
      if task["name"] == name:
         task["completed"] = True
         save_tasks(tasks)
         print("Task completed! ")
         return
   print("Task not found!")
    
def overdue_task(tasks):
   found = False
   for task in tasks:
      if task["completed"]:
         continue
      deadline = datetime.strptime(task["deadline"], "%Y-%m-%d").date()
      days = (deadline - date.today()).days
      if days < 0:
         print("Overdue: ", task["name"], "- was due", -days, "days ago")
         found = True
   if (not found):
      print("No overdue tasks found!\n")
   else:
      print("")

def check_deadline(tasks):
   name = input("Enter task name: ")
   for task in tasks: 
      if task["name"] == name:
         deadline = datetime.strptime(task["deadline"], "%Y-%m-%d").date()
         days = (deadline - date.today()).days
         if days < 0:
             print("Overdue: ", task["name"], "- was due", -days, "days ago")
         else: 
             print(task["name"], "- ", days, "days until deadline")
         return
   print("Task not found!")

def summary(tasks):

   done = 0
   total = len(tasks)
   overdue = 0
   for task in tasks:
      deadline = datetime.strptime(task["deadline"], "%Y-%m-%d").date()
      if deadline < date.today() and not task["completed"]:
         overdue += 1 
   for task in tasks:
      if task["completed"]:
         done += 1
   print("--- Summary ---")
   print("Total:     ", total)
   print("Completed:     ", done)
   print("Pending:     ", total - done)
   print("Overdue:     ", overdue)

def delete_task(tasks):
   name = input("Enter task name to delete: ")
   for task in tasks:
      if task["name"] == name:
         tasks.remove(task)
         save_tasks(tasks)
         print("Task deleted!")
         return
   print("Task not found!")

def completed_task(tasks):
   found = False
   for task in tasks:
      if task["completed"]:
         print(task["name"], "-", task["deadline"])
         found = True
   if not found:
      print("No tasks found!")

while True:
   print("1. Add tasks")
   print("2. View tasks")
   print("3. Remove tasks")
   print("4. Mark as completed")
   print("5. Check overdue tasks")
   print("6. Show Summary")
   print("7. Check completed tasks")
   print("8. Check task deadline")
   print("9. Quit")
   choice = input("Enter a choice: ")

   match choice:
      case "1":
         clear_terminal()
         print(add_task(tasks))
         print("")
      case "2":
         clear_terminal()
         view_task(tasks)
      case "3":
         clear_terminal()
         delete_task(tasks)
         print("")
      case "4":
         clear_terminal()
         complete_task(tasks)
         print("")
      case "5":
         clear_terminal()
         overdue_task(tasks)
      case "6":
         clear_terminal()
         summary(tasks)
         print("")
      case "7":
         clear_terminal()
         completed_task(tasks)
         print("")
      case "8":
         clear_terminal()
         check_deadline(tasks)
         print("")
      case "9":
         clear_terminal()
         break
      case _:
         clear_terminal()
         print("Invalid Option")
