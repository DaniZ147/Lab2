import streamlit as st
import info
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="The profitability of of movies that have thore", page_icon=":popcorn:")
st.header("How profitable is the thor character to the MCU?")
df = pd.read_json("WebDevLab02/data.json")
st.dataframe(df)
df["profit"] = df['box_office'] - df['budget']
st.write("---")
start, end = st.columns(2)
df["year"] = pd.to_datetime(df["year"])
startdate = pd.to_datetime(df["year"]).min()#NEW
endtdate = pd.to_datetime(df["year"]).max()#NEW
with start:
    d1 = pd.to_datetime(st.date_input("Start Date", startdate)) #NEW
with end:
    d2 = pd.to_datetime(st.date_input("End Date", endtdate)) #NEW

df= df[(df["year"] >= d1) & (df["year"] <= d2 )].copy()

st.write("---")
st.sidebar.header("Filter")
movie = st.sidebar.multiselect(
    "Do you want to filter by movie:",
    options=df["movie"].unique(), default=df["movie"].unique()
)#NEW
movie_type = st.sidebar.multiselect(
    "Do you want to filter by movie type:",
    options=df["movie_type"].unique(), default=df["movie_type"].unique()
)

def net(): #NEW
    sel = df.query(
        "movie == @movie & movie_type == @movie_type"
    )
    a = int(sel["profit"].sum())
    b = int(sel["box_office"].sum())
    c = int(sel["budget"].sum())

    L, C, R = st.columns(3)
    with L:
        st.subheader("Net profit")
        st.write(f"${a:,}")
    with C:
        st.subheader("Net budget")
        st.write(f"${c:,}")
    with R:
        st.subheader("Total box office")
        st.write(f"${b:,}")
net()

st.write("---")

def data_table(): #NEW

    sel = df.query(
        "movie == @movie & movie_type == @movie_type"
    )
    
    st.dataframe(sel)

def graph():#NEW
    sel = df.query(
        "movie == @movie & movie_type == @movie_type"
    )
    sp =sel.sort_values(by="profit")
    gp = px.bar(sp, x="profit", y="movie", title= "Profit by Movie")
    st.plotly_chart(gp)

    sb = sel.sort_values(by="budget")
    gb = px.bar(sb, x="budget", y="movie", title= "Budget by Movie")
    st.plotly_chart(gb)

    so = sel.sort_values(by="box_office")
    go = px.bar(so, x="box_office", y="movie", title= "Box office by Movie")
    st.plotly_chart(go)

def chart(): #NEW
    sel = df.query(
        "movie == @movie & movie_type == @movie_type"
    )
    ch = px.pie(sel, values="profit", names="movie", title= "Profit by Movie", hole=0.5 )
    st.plotly_chart(ch)

    cb = px.pie(sel, values="budget", names="movie", title= "Budget by Movie", hole=0.5 )
    st.plotly_chart(cb)

    co = px.pie(sel, values="box_office", names="movie", title= "Box office by Movie", hole=0.5 )
    st.plotly_chart(co)

def separater(): 
    st.header("Interactive data")
    t1, t2, t3 = st.tabs(["Data table", "Chart", "Graph"])

    with t1:
        st.subheader("Data table")
        data_table()
    
    with t2:
        st.subheader("Chart")
        chart()

    with t3:
        st.subheader("Graph")
        graph()

separater()





