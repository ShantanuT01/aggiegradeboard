from dashboard_constants import *
import streamlit as st
import json
import pandas as pd
import plotly.express as px
from pathlib import Path

def highlight_everyother(s):
    return ['background-color: maroon; color:white' if x%2==1 else ''
              for x in range(len(s))]
try:
    # loading in data
    if not Path("professor_course_terms.csv").is_file():
        download_kaggle_data()

    professor_course_terms = pd.read_csv("professor_course_terms.csv")
    professor_courses = pd.read_csv("professor_courses.csv")

    # configuration
    st.set_page_config(page_title='Aggie Grade Board',layout='wide')

    # headers
    st.title("Texas A&M Professor Dashboard")

    # input field
    selected_professor = st.selectbox(label='Professor by Name', options=professor_course_terms[PROF_NAME].unique())

    # show courses
    st.markdown("## Courses Taught")
    pc_frame = query_frame({PROF_NAME:selected_professor}, professor_courses)[PROFESSOR_COURSE_COLS]
    st.dataframe(pc_frame.style.apply(highlight_everyother).format(precision=3), hide_index=True)

    # fetch available courses
    courses_taught_frame = pc_frame[[SUBJECT_CODE,COURSE_NUMBER]]
    courses_taught = list()

    for i in range(len(courses_taught_frame)):
        subject_code = courses_taught_frame[SUBJECT_CODE].values[i]
        course_number = courses_taught_frame[COURSE_NUMBER].values[i]
        courses_taught.append(f"{subject_code} {course_number}")

    # allow user to select course
    st.header("Breakdown by Course")
    selected_course = st.selectbox(label="Select Course",options=courses_taught)

    # display course over time
    subject_code, course_number = selected_course.split(" ")
    if course_number.isnumeric():
        course_number = int(course_number)
    selected_course_terms = query_frame({SUBJECT_CODE: subject_code, COURSE_NUMBER: course_number, PROF_NAME: selected_professor}, professor_course_terms)
    display_course_terms = selected_course_terms[[SEMESTER_CODE, SEMESTER, YEAR]+PROFESSOR_COURSE_COLS].sort_values(SEMESTER_CODE)
    selected_course_terms[TERM] = selected_course_terms[SEMESTER] + " " + selected_course_terms[YEAR].astype(str)
    display_course_terms = display_course_terms.drop(labels=[SEMESTER_CODE],axis=1)
    st.dataframe(display_course_terms.style.apply(highlight_everyother).format(precision=3), column_config={YEAR:st.column_config.NumberColumn(format="%d")}, hide_index=True)

    st.markdown(f"### AEFIS Statistics for {selected_course}")

    st.write("Averages Across All Semesters")
    st.write("Note: The choice \"Not Applicable (score of 0)\" does not affect the mean_diverse score received.")
    aefis_course_total_frame = professor_courses[(professor_courses[PROF_NAME]==selected_professor)&(professor_courses[SUBJECT_CODE] == subject_code)&(professor_courses[COURSE_NUMBER] == course_number)]
    st.dataframe(aefis_course_total_frame[AEFIS_MEAN_COLS],hide_index=True)
    terms = list(selected_course_terms[TERM].unique())
    terms.insert(0, ALL_TIME)
    selected_term = st.selectbox(TERM,options=terms)
    if selected_term != ALL_TIME:
        season, year = selected_term.split(" ")
        year = int(year)

    # output pie charts for each survey question
    aefis_cols = st.columns([2,1,2])
    counter = 0
    for question in AEFIS_QUESTIONS_COLS:
        col_index = counter % 2
        if col_index == 1:
            col_index = 2
        aefis_cols[col_index].markdown(f"*{question}*")
        columns = AEFIS_QUESTIONS_COLS[question]
        choices = AEFIS_CHOICE_MAPPINGS[question]
        graph_data = list()
        if selected_term != ALL_TIME:
            aefis_question_frame = selected_course_terms[(selected_course_terms[TERM]==selected_term)][columns]
        else:
            aefis_question_frame = selected_course_terms[columns]
    
        columns.sort(key=lambda value: int(value.split("_")[-1]))
        total_students = 0
        color_map = dict()
        for column in columns:
            weight = int(column.split("_")[-1])
            for choice in choices:
                if choices[choice][VALUE] == weight:
                    row = {CHOICE: f"{choice} (score of {weight})", STUDENTS:aefis_question_frame[column].sum()}
                    graph_data.append((weight,row))
                    color_map[row[CHOICE]] = choices[choice][COLOR]
                    total_students += aefis_question_frame[column].sum()
       

        if total_students != 0: 
            graph_data.sort(key=lambda pair: pair[0])
            graph_data_frame = pd.DataFrame([pair[1] for pair in graph_data])
            fig = px.pie(graph_data_frame,values=STUDENTS,names=CHOICE, color=CHOICE, color_discrete_map=color_map)
            fig.update_traces(sort=False)
            aefis_cols[col_index].plotly_chart(fig,theme=None)
        else:
            aefis_cols[col_index].write("No data available.")
        counter += 1
except Exception as e:
    print(e)
    st.error("An error occurred. Please try again later.")
st.write("Developed by Shantanu Thorat, Texas A&M Class of 2024.")