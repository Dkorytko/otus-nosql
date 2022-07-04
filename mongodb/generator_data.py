from faker import Faker
import json
fake = Faker()

def generate_data(records):
    employees = []
    for i in range(0, records):
        employee = {
            'table_number': fake.random_number(digits=5),
            'age': fake.random_number(digits=2),
            'name': fake.name(),
            'email': str(fake.email()),
            'phone': str(fake.phone_number())
        }

        employees.append(employee)

    with open('employees.json', 'w') as fp:
        json.dump(employees, fp)

    print("Файл создан.")

num = int(input("Введите количество записей:"))
generate_data(num)