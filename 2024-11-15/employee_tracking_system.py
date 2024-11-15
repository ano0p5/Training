import json
from datetime import datetime

class EmployeeTracker:
    task_list = []

    def __init__(self, emp_name, emp_id):
        self.emp_name = emp_name
        self.emp_id = emp_id
        self.login_time = None
        self.logout_time = None
        self.current_task = None
        self.tasks = []

    def login(self):
        self.login_time = datetime.now()    
        print(f"{self.emp_name} logged in at {self.login_time}")

    def add_task(self, task_title, task_description):
        self.current_task = {
            "task_title": task_title,
            "task_description": task_description,
            "start_time": datetime.now().strftime('%Y-%m-%d %H:%M'),
            "end_time": None,
            "task_success": None
        }    
        print(f"Task '{task_title}' started")

    def end_task(self, task_success):
        if self.current_task:
            self.current_task["end_time"] = datetime.now().strftime('%Y-%m-%d %H:%M')
            self.current_task["task_success"] = task_success
            self.tasks.append(self.current_task)
            EmployeeTracker.task_list.append(self.current_task)
            self.current_task = None
            print("Task ended.")
        else:
            print("No task is currently active.")

    def logout(self):
        self.logout_time = datetime.now()
        data_employee = {
            "emp_name": self.emp_name,
            "emp_id": self.emp_id,
            "login_time": self.login_time.strftime('%Y-%m-%d %H:%M'),
            "logout_time": self.logout_time.strftime('%Y-%m-%d %H:%M'),
            "tasks": self.tasks
        }   

        file_name = f"{datetime.now().strftime('%Y-%m-%d')}_{self.emp_name.replace(' ', '_')}.json"
        with open(file_name, 'w') as file:
            json.dump(data_employee, file, indent=4)
        print(f"Data for {self.emp_name} saved to {file_name}")
        
if __name__ == "__main__":
    employee1 = EmployeeTracker("Anoop", 1)
    employee1.login()
    employee1.add_task("Task 1", "Finished the Employee Tracking Task")
    employee1.end_task(True)
    employee1.logout()