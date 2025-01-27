def calculate_bmi(weight, height):
    height_in_m = height / 100
    return round(weight / (height_in_m ** 2), 2)

def get_fitness_plan(bmi, age, gender):

    if gender.lower() == "male":
        if age < 18:
            return "Youth plan", {"Push-ups": 2, "Squats": 2, "Left Curl": 1, "Right Curl": 1}
        elif 18 <= age < 40:
            if bmi < 18.5:
                return "6-month bulking plan", {"Right Curl": 3, "Left Curl": 3, "Push-ups": 2, "Squats": 3}
            elif 18.5 <= bmi < 25:
                return "3-month maintenance plan", {"Right Curl": 4, "Left Curl": 4, "Push-ups": 3, "Squats": 3}
            elif 25 <= bmi < 30:
                return "9-month fitness plan", {"Push-ups": 3, "Squats": 3, "Left Curl": 3, "Right Curl": 3}
            else:
                return "12-month weight loss plan", {"Push-ups": 3, "Squats": 3, "Left Curl": 2, "Right Curl": 2}
        else:
            return "General fitness plan", {"Push-ups": 2, "Squats": 2, "Left Curl": 2, "Right Curl": 2}

    elif gender.lower() == "female":
        if age < 18:
            return "Youth plan", {"Push-ups": 1, "Squats": 2, "Left Curl": 1, "Right Curl": 1}
        elif 18 <= age < 40:
            if bmi < 18.5:
                return "6-month bulking plan", {"Right Curl": 2, "Left Curl": 2, "Push-ups": 1, "Squats": 3}
            elif 18.5 <= bmi < 25:
                return "3-month maintenance plan", {"Right Curl": 3, "Left Curl": 3, "Push-ups": 2, "Squats": 3}
            elif 25 <= bmi < 30:
                return "9-month fitness plan", {"Push-ups": 3, "Squats": 3, "Left Curl": 2, "Right Curl": 2}
            else:
                return "12-month weight loss plan", {"Push-ups": 3, "Squats": 3, "Left Curl": 2, "Right Curl": 2}
        else:
            return "General fitness plan", {"Push-ups": 2, "Squats": 2, "Left Curl": 1, "Right Curl": 1}

    else:
        return "Custom plan", {"Push-ups": 2, "Squats": 2, "Left Curl": 2, "Right Curl": 2}
