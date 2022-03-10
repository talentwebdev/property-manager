
   
from django.views import View
from django.template import loader
from django.http import HttpResponse
from typing import List, Dict, Optional

import requests

class InvalidEmployeesUrlError(Exception):
    """ occurs when the employees url is invalid """
    pass


class InvalidNameError(Exception):
    """ occurs when invalid name is fetched """
    pass


class EmployeesView(View):
    template_name = 'employees.html'
    employees_url = "https://gist.githubusercontent.com/chancock09/6d2a5a4436dcd488b8287f3e3e4fc73d/raw/fa47d64c6d5fc860fabd3033a1a4e3c59336324e/employees.json"
    
    def get_employees(self) -> list:       
        
        r = requests.get(self.employees_url)
        
        if r.status_code != 200:
            raise InvalidEmployeesUrlError
        
        return r.json()
    
    
    def generate_employee_tree(self, employees: List[dict]) -> Dict[Optional[str], list]:
        """ generate employees tree """
        
        r = {}
        for employee in employees:
            manager_id = employee.get('manager_id')
            
            if r.get(manager_id) is None:
                r[manager_id] = []
                
            # add sort option
            i = len(r[manager_id])
            while i > 0:
                try:
                    curret_last_name = r[manager_id][i-1].get("name").split(" ")[-1]
                    last_name = employee.get("name").split(" ")[-1]
                except:
                    raise InvalidNameError
                
                if curret_last_name <= last_name:
                    break
                
                i = i - 1
                
            r[manager_id].insert(0 if i < 0 else i, employee)            

            
        return r
    
    def get_employees_list(self, employees_tree: Dict[Optional[str], list], root: Optional[str] = None) -> str:
        """ get employees list html text """
        
        html_view = "<ul>"
        employees = employees_tree.get(root)
        
        if employees is None:
            return ""
    
        for employee in employees:
            employee_html_view = f"<li><span>{employee['title']}: {employee['name']}</span>"
            
            employee_html_view = employee_html_view + self.get_employees_list(employees_tree, employee["id"])
            
            employee_html_view = employee_html_view + "</li>"
            
            html_view = html_view + employee_html_view
        
        html_view = html_view + "</ul>"
        return html_view            

    
    def get(self, request):
        template = loader.get_template("employees.html")
        employees = self.get_employees()
        employees_tree = self.generate_employee_tree(employees)
        
        return HttpResponse(template.render({
            "employees": self.get_employees_list(employees_tree)
        }, request))
