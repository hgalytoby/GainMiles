import asyncio
import os
import sys

import httpx
import openpyxl

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from app.exceptions.base import AppException
from app.services.employee.validator import EmployeeValidator

URL = "http://localhost:8000/api/employees"


async def main():
    excel_path = os.path.join(PROJECT_ROOT, "docs", "interview_employee_data.xlsx")
    if not os.path.exists(excel_path):
        print(f"Error: Excel file not found at {excel_path}")
        return

    try:
        wb = openpyxl.load_workbook(excel_path)
        sheet = wb["Employee Data"]
    except Exception as e:
        print(f"Error loading Excel workbook/sheet: {e}")
        return

    # Skip header
    rows = list(sheet.iter_rows(values_only=True))
    if not rows:
        print("Excel file is empty.")
        return

    data_rows = rows[1:]

    seen_employee_ids = set()
    success_count = 0
    validation_failures = []
    api_failures = []

    print(f"Starting import of {len(data_rows)} rows...")

    async with httpx.AsyncClient() as client:
        for idx, row in enumerate(
            data_rows, start=2
        ):  # Excel is 1-indexed, so row 2 is the first data row
            if all(cell is None for cell in row):
                # Skip completely empty rows
                continue

            # Ensure row has enough cells
            row_data = list(row) + [None] * (7 - len(row))

            raw_emp_id = row_data[0]
            raw_name = row_data[1]
            raw_email = row_data[2]
            raw_dept = row_data[3]
            raw_salary = row_data[4]
            raw_join_date = row_data[5]

            emp_id = "" if raw_emp_id is None else str(raw_emp_id)
            name = "" if raw_name is None else str(raw_name)
            email = "" if raw_email is None else str(raw_email)
            dept = "" if raw_dept is None else str(raw_dept)
            join_date = "" if raw_join_date is None else str(raw_join_date)

            try:
                # Step 1: Validate Employee ID (Must be unique and required)
                if not emp_id:
                    raise ValueError("employee_id is required.")

                if emp_id in seen_employee_ids:
                    raise ValueError("employee_id must be unique.")

                seen_employee_ids.add(emp_id)

                # Step 2: Validate Name, Email, Department, Join Date
                EmployeeValidator.validate_name(name)
                EmployeeValidator.validate_email(email)
                EmployeeValidator.validate_department(dept)
                EmployeeValidator.validate_join_date(join_date)

                # Step 3: Validate Salary
                if raw_salary is None:
                    raise ValueError("salary is required.")
                if not isinstance(raw_salary, int):
                    raise ValueError("salary must be a positive integer (> 0).")
                try:
                    salary = int(raw_salary)
                except ValueError:
                    raise ValueError

                EmployeeValidator.validate_salary(raw_salary)

            except (AppException, ValueError, TypeError) as e:
                # Record validation failure
                validation_failures.append(
                    {
                        "row": idx,
                        "employee_id": emp_id,
                        "msg": e.msg if isinstance(e, AppException) else str(e),
                    }
                )
                continue
            except Exception as e:
                # Catch-all validation/parsing failure
                validation_failures.append(
                    {
                        "row": idx,
                        "employee_id": emp_id,
                        "error_code": "UNKNOWN_ERROR",
                        "msg": str(e),
                    }
                )
                continue

            # Submit valid row to API
            payload = {
                "employee_id": emp_id,
                "name": name,
                "email": email,
                "department": dept,
                "salary": salary,
                "join_date": join_date,
            }

            try:
                response = await client.post(URL, json=payload)
                if response.status_code == 201:
                    success_count += 1
                else:
                    api_failures.append(
                        {
                            "row": idx,
                            "employee_id": emp_id,
                            "status_code": response.status_code,
                            "response": response.text,
                        }
                    )
            except Exception as e:
                api_failures.append(
                    {
                        "row": idx,
                        "employee_id": emp_id,
                        "status_code": None,
                        "response": f"Network Error: {e}",
                    }
                )

    # Summary Report
    print("\n" + "=" * 50)
    print("             IMPORT SUMMARY REPORT")
    print("=" * 50)
    print(f"Total Rows Processed: {len(data_rows)}")
    print(f"Successfully Imported: {success_count}")
    print(f"Validation Failures:  {len(validation_failures)}")
    print(f"API Submission Failures: {len(api_failures)}")
    print("=" * 50)

    if validation_failures:
        print("\n[Validation Failures Details]")
        for f in validation_failures:
            print(f"- Row {f['row']} (ID: {f['employee_id'] or 'N/A'}): {f['msg']}")

    if api_failures:
        print("\n[API Submission Failures Details]")
        for f in api_failures:
            status_str = f"Status {f['status_code']}" if f["status_code"] else "No Response"
            print(f"- Row {f['row']} (ID: {f['employee_id']}): [{status_str}] {f['response']}")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
