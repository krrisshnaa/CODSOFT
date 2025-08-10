def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return "Error: Cannot divide by zero."
    return x / y

print("Welcome to the Simple Calculator.")
print("You can perform operations: +  -  *  /")
print("To exit, type 'q' or 't' at any time.\n")

while True:
    num1_input = input("Enter the first number (or 'q'/'t' to quit): ")
    if num1_input.lower() in ['q', 't']:
        print("Exiting the calculator. Goodbye!")
        break

    num2_input = input("Enter the second number (or 'q'/'t' to quit): ")
    if num2_input.lower() in ['q', 't']:
        print("Exiting the calculator. Goodbye!")
        break

    try:
        num1 = float(num1_input)
        num2 = float(num2_input)
    except ValueError:
        print("Invalid input. Please enter valid numbers.\n")
        continue

    operation = input("Choose an operation (+, -, *, /): ")

    if operation == '+':
        result = add(num1, num2)
    elif operation == '-':
        result = subtract(num1, num2)
    elif operation == '*':
        result = multiply(num1, num2)
    elif operation == '/':
        result = divide(num1, num2)
    else:
        print("Invalid operation. Please choose one of +, -, *, /.\n")
        continue

    print(f"Result: {result}\n")
