# -*- coding: utf-8 -GPK*-

{
    'name': 'Surya Sarpam',
    'version': '1.0',
    "author": 'Yali Technologies',
    "website": 'http://www.yalitechnologies.com/',
    'category': 'Hospital',
    'sequence': 15,
    'summary': 'Hospital Management',
    'description': 'Hospital Management',
    'depends': ['base', 'mail'],
    'data': [
        'data/access_rights.xml',
        'menu/main_menu.xml',

        # 'views/hr_employee.xml',
        # 'menu/product_menu.xml',
        'views/year.xml',
        'views/month.xml',
        'views/week.xml',        
        'views/day.xml',
        'views/employee/hr_employee.xml',
        'views/employee/hr_attachment.xml',
        'views/employee/hr_contact.xml',
        'views/employee/hr_department.xml',
        'views/employee/hr_employee.xml',
        'views/employee/hr_employee_category.xml',
        'views/employee/hr_employee_designation.xml',
        'views/employee/hr_experience.xml',
        'views/employee/hr_leave.xml',
        'views/employee/hr_leave_detail.xml',
        'views/employee/hr_qualification.xml',
        'views/employee/res_language.xml',
        'views/employee/res_religion.xml',
        'menu/calender_menu.xml',
        'menu/employee_menu.xml',
        'menu/hr.xml',
        'views/time_management/shift.xml',
        'views/time_management/attendance.xml',
        'views/time_management/month_attendance.xml',
        'views/time_management/time_schedule.xml',
        'views/time_management/time_configuration.xml',
        'views/time_management/time_machine.xml',
        'views/time_management/time_sheet.xml',
        'menu/time_management.xml',
        'views/leave_management/leave_application.xml',
        'views/leave_management/compoff_application.xml',
        'views/leave_management/permission_application.xml',
        'views/leave_management/leave_configuration.xml',
        'views/leave_management/overtime_application.xml',
        'menu/leave_management.xml',
        'views/payroll/employee_salary.xml',
        'views/payroll/pay_slip.xml',
        'views/payroll/payroll_generation.xml',
        'views/payroll/payroll_policy.xml',
        'views/payroll/salary_rule.xml',
        'views/payroll/salary_structure.xml',
        'menu/payroll_management.xml',
        'views/product/product.xml',
        'views/product/stock.xml',
        'views/product/stock_location.xml',
        'views/product/product_configuration.xml',
        'menu/product_menu.xml',
        'data/product.xml',
        'views/purchase/indent.xml',
        'views/purchase/vendor_selection.xml',
        'views/purchase/quotation.xml',
        'views/purchase/purchase_order.xml',
        'views/purchase/direct_purchase_order.xml',
        'views/purchase/material_receipt.xml',
        'menu/purchase_management.xml',
        'views/mat/mat_schedule.xml',
        'menu/mat_management.xml',
        '/home/sarpam/Documents/project/surya_sarpam/views/reporting/report.xml',
        'menu/report_management.xml',
    ],
    'demo': [

    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
