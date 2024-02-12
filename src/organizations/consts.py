from organizations.models import Department, Industry

INDUSTRY_DEPARTMENT_MAP = {
    Industry.IndustryChoice.ACCOUNTING: [
        Department.DepartmentChoices.ACCOUNTING,
        Department.DepartmentChoices.FINANCE,
        Department.DepartmentChoices.INTERNAL_AUDIT,
    ],
    Industry.IndustryChoice.AEROSPACE: [
        Department.DepartmentChoices.DATA_SCIENCE,
        Department.DepartmentChoices.RESEARCH_DEVELOPMENT,
    ],
    Industry.IndustryChoice.AGRICULTURE: [
        Department.DepartmentChoices.ACCOUNTING,
    ],
}

#
# Industry.IndustryChoice.AUTOMOTIVE
# Industry.IndustryChoice.BANKING
# Industry.IndustryChoice.BIOTECHNOLOGY
# Industry.IndustryChoice.CHEMICAL
# Industry.IndustryChoice.COMMUNICATIONS
# Industry.IndustryChoice.CONSTRUCTION
# Industry.IndustryChoice.CONSULTING
# Industry.IndustryChoice.EDUCATION
# Industry.IndustryChoice.ELECTRONICS
# Industry.IndustryChoice.ENERGY
# Industry.IndustryChoice.ENGINEERING
# Industry.IndustryChoice.ENTERTAINMENT
# Industry.IndustryChoice.ENVIRONMENTAL
# Industry.IndustryChoice.FINANCE
# Industry.IndustryChoice.FOOD_AND_BEVERAGE
# Industry.IndustryChoice.GOVERNMENT
# Industry.IndustryChoice.HEALTHCARE
# Industry.IndustryChoice.HOSPITALITY
# Industry.IndustryChoice.HUMAN RESOURCES
# Industry.IndustryChoice.INSURANCE
# Industry.IndustryChoice.INTERNET
# Industry.IndustryChoice.INVESTMENT BANKING
# Industry.IndustryChoice.JOURNALISM
# Industry.IndustryChoice.LAW ENFORCEMENT
# Industry.IndustryChoice.LEGAL
# Industry.IndustryChoice.MANUFACTURING
# Industry.IndustryChoice.MARKETING
# Industry.IndustryChoice.MEDIA
# Industry.IndustryChoice.NONPROFIT
# Industry.IndustryChoice.PHARMACEUTICAL
# Industry.IndustryChoice.REAL ESTATE
# Industry.IndustryChoice.RETAIL
# Industry.IndustryChoice.SALES
# Industry.IndustryChoice.TECHNOLOGY
# Industry.IndustryChoice.TELECOMMUNICATIONS
# Industry.IndustryChoice.TRANSPORTATION
# Industry.IndustryChoice.TRAVEL
