import streamlit as st
import pickle
import pandas as pd


pipe = pickle.load(open('pipe4.pkl','rb'))
log_model = pickle.load(open('log_model4.pkl', 'rb'))

teams = ["Australia",
        "Pakistan",
        "New Zealand",
        "Bangladesh",
        "South Africa",
        "India",
        "England",
        "Sri Lanka",
        "Netherlands"]


st.set_page_config(page_title="ICC World Cup Score Prediction", page_icon="🏏")
st.sidebar.title("Cricket Predictor App")
st.sidebar.image(
    "https://img.cricketworld.com/images/f-127075/icc-cricket-world-cup-2023-logo-.jpg"
)

st.title("Welcome to ICC World Cup Predictor")
user_menu = st.sidebar.radio("Select an option", ("Score Prediction", "Winning Percentage"))


if user_menu == 'Score Prediction':
    st.header("ICC World Cup Score Prediction")
    col1, col2 = st.columns(2)

    with col1:
        batting_team = st.selectbox('Select batting team', sorted(teams))
    with col2:
        bowling_team = st.selectbox('Select bowling team', sorted(teams))

    current_score = st.number_input('Current Score')

    col3, col4 = st.columns(2)
    with col3:
        overs = st.number_input('Overs Completed (works for over > 15)')
    with col4:
        wickets = st.number_input('Wickets Out')

    last_five = st.number_input('Runs scored in last 5 Overs')

    if st.button('Predict Score'):
        if batting_team == bowling_team:
            st.error("Batting team and bowling team cannot be the same.")
        elif current_score == 0:
            st.error("Current score can't be 0.")
        elif overs < 15:
            st.error("Overs done cannot be less than 15.")
        elif last_five == 0:
            st.error("Runs scored in last 5 Overs can't be 0.")
        else:
            balls_left = 300 - (overs * 6)
            wickets_left = 10 - wickets
            crr = current_score / overs

            input_df = pd.DataFrame(
                {'batting_team': [batting_team], 'bowling_team': [bowling_team], 'current_score': [current_score],
                 'balls_left': [balls_left], 'wickets_left': [wickets_left], 'crr': [crr], 'last_five': [last_five]})
            result = pipe.predict(input_df)

            st.header("Predicted Score - " + str(int(result[0])))

if user_menu == "Winning Percentage":
    st.header('Winning Percentage Prediction')
    col1, col2 = st.columns(2)

    with col1:
        batting_team = st.selectbox('Select the batting team', sorted(teams))
    with col2:
        bowling_team = st.selectbox('Select the bowling team', sorted(teams))

    target = st.number_input('Target')

    col3, col4, col5 = st.columns(3)

    with col3:
        score = st.number_input('Score')
    with col4:
        overs = st.number_input('Overs Completed (works for over > 15)')
    with col5:
        wickets = st.number_input('Wickets out')

    if st.button('Predict Probability'):
        if batting_team == bowling_team:
            st.error("Batting team and bowling team cannot be the same.")
        elif target == 0:
            st.error("Target can't be 0.")
        elif score == 0 or score > target:
            st.error("Score must be greater than 0")
        elif score > target:
            st.error("Current score must be less than target")
        elif overs < 15:
            st.error("Overs done cannot be less than 15.")
        elif wickets > 10:
            st.error("wickets out cannot be more than 10")   

        else:
            runs_left = target - score
            balls_left = 300 - (overs * 6)
            wickets_left = 10 - wickets
            crr = score / overs
            rrr = (runs_left * 6) / balls_left

            input_df = pd.DataFrame(
                {'batting_team': [batting_team], 'bowling_team': [bowling_team], 'runs_left': [runs_left],
                 'balls_left': [balls_left], 'wickets_left': [wickets], 'runs_x': [target],
                 'crr': [crr], 'rrr': [rrr]})

            result = log_model.predict_proba(input_df)
            loss = result[0][0]
            win = result[0][1]
            st.header(batting_team + "- " + str(round(win * 100)) + "%")
            st.header(bowling_team + "- " + str(round(loss * 100)) + "%")


st.markdown("---")
st.write("Cricket Lover's Hub 🏏")
