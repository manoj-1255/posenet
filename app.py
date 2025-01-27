import streamlit as st
from login import login_page, register_page
from tracker import fitness_tracker
from users import delete_account, users

def main():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "exercise_complete" not in st.session_state:
        st.session_state.exercise_complete = False
    if "username" not in st.session_state:
        st.session_state.username = None  # Initialize username
    if "current_exercise" not in st.session_state:
        st.session_state.current_exercise = None

    if st.session_state.exercise_complete:
        st.title("Congratulations! 🎉")
        st.write("You’ve completed your fitness plan for today!")
        
        if st.button("Do it Again"):
            st.session_state.exercise_complete = False  # Reset exercise state
            st.session_state.current_exercise = None  # Reset current exercise

        st.sidebar.title("Actions")
        # Logout Button
        if st.sidebar.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.login_incremented = False
            st.session_state.exercise_complete = False  # Reset exercise state
            st.session_state.current_exercise = None  # Reset current exercise
            st.success("Logged out successfully.")
        
        # Delete Account Button
        if st.sidebar.button("Delete Account"):
            delete_account(st.session_state.username)
            st.session_state.authenticated = False
            st.session_state.login_incremented = False
            st.session_state.exercise_complete = False  # Reset exercise state
            st.session_state.current_exercise = None  # Reset current exercise
            st.success("Account deleted.")
            
    elif st.session_state.authenticated:
        # Increment day count only on first login per session
        if "login_incremented" not in st.session_state or not st.session_state.login_incremented:
            users[st.session_state.username]["day_count"] += 1
            st.session_state.login_incremented = True

        # Sidebar: Welcome, User Info, and Logout
        st.sidebar.title(f"Welcome, {st.session_state.username}!")
        user_info = users[st.session_state.username]

        st.sidebar.write(f"**BMI:** {user_info['bmi']}")
        st.sidebar.write(f"**Plan:** {user_info['plan']}")
        st.sidebar.write(f"**Repetitions:** {user_info['reps']} reps/day")
        st.sidebar.write(f"**Login Count:** {user_info['day_count']} days")

        # Logout Button
        if st.sidebar.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.login_incremented = False
            st.success("Logged out successfully.")

        # Start Exercise Button: Pass `bmi` and `age` to `fitness_tracker`
        if st.sidebar.button("Start Exercise"):
            user_bmi = user_info["bmi"]
            user_age = user_info["age"]
            user_day = user_info["day_count"]
            user_gender = user_info["gender"]
            fitness_tracker(user_bmi, user_age, user_gender, user_day)
            st.session_state.exercise_complete = True  # Mark completion

        # Delete Account Button
        if st.sidebar.button("Delete Account"):
            delete_account(st.session_state.username)
            st.session_state.authenticated = False
            st.session_state.login_incremented = False
            st.success("Account deleted.")
    else:
        # Login or Register Page
        choice = st.sidebar.radio("Login or Register", ("Login", "Register"))
        if choice == "Login":
            login_page()
        elif choice == "Register":
            register_page()

if __name__ == "__main__":
    main()
