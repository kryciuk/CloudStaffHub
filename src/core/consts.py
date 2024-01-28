from enum import Enum


class GROUPS(str, Enum):
    GROUP__OWNER = "Owner"
    GROUP__RECRUITER = "Recruiter"
    GROUP__MANAGER = "Manager"
    GROUP__EMPLOYEE = "Employee"
    GROUP__CANDIDATE = "Candidate"
