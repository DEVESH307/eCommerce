from datetime import datetime

def after_12_pm_deny(func):
    def wrapper(*args, **kwargs):
        now = datetime.now().hour
        print(1)
        if now > 12:
            raise Exception("Access denied after 12 PM!")
        func(*args, **kwargs)
    return wrapper

def greet_decorator(func):
    def wrapper(*args, **kwargs):
        print(2)
        print("Hello, All!")
        func(*args, **kwargs)
        print("Bye, All!")
    return wrapper

@after_12_pm_deny
@greet_decorator
def greet(name):
    print("Hello, {}!".format(name))

def greet_eve():
    print("Hello, Eve!")

def greet_all():
    print("Hello, All!")
    greet_eve()

def greet_all_():
    print("Hello, All!")
    greet()

# 1. Replace return (*args, **kwargs) with actual function implementation
# 2. call the wrapper instated of actual method

# TO AVOID:
# def greet_all_():
#     print("Hello, All!")
#     greet()

if __name__ == "__main__":
    greet("Devesh")
