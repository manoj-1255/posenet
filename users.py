from plans import calculate_bmi, get_fitness_plan
import bcrypt

users = {}

def authenticate_user(username, password):
    if username in users and bcrypt.checkpw(password.encode(), users[username]["password"]):
        return True
    return False

def register_user(username, password, gender, height, weight, age):
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    bmi = calculate_bmi(weight, height)
    plan, reps = get_fitness_plan(bmi, age, gender)

    users[username] = {
        "password": hashed_pw,
        "gender": gender,
        "height": height,
        "weight": weight,
        "age": age,
        "bmi": bmi,
        "plan": plan,
        "reps": reps,
        "day_count": 0,  # Initialize day count
    }

def delete_account(username):
    if username in users:
        del users[username]
