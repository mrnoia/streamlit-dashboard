import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import altair as alt
import numpy as np

# configuration
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

# read in css
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("American Fruit Consumption from 1984 to 2016")

# get data
@st.cache
def read_data():
    df = pd.read_csv("https://query.data.world/s/meatifotcvhwenlvshvouskf54iv4d")
    return df


# read data into dataframe and clean
df = read_data()
df = df.dropna()
df.replace("      na", 0, inplace=True)
df["Year"] = df["Year"].astype("int64")
df["Year"] = df["Year"].astype("string")
df["Type"] = df["Type"].astype("string")
df["Category"] = df["Fruit"].astype("string")
df["Fruit"] = df["Category"].astype("string")
df["Pounds Consumed Per Capita"] = df["Pounds Consumed Per Capita"].astype("float")
df["Year"] = df["Year"].astype("string")  # this is for the chart to work

# convert df to json
df_json = df.to_json(orient="records")
st.caption("table built using tabulator")
# diplay json using tabulator note {{ for object is f method
tabulator_html = f"""
<div id="tabulator"> </div>
 <link href="https://cdnjs.cloudflare.com/ajax/libs/tabulator/5.4.2/css/tabulator_bulma.min.css" rel="stylesheet">
 <script type="text/javascript" src="https://unpkg.com/tabulator-tables/dist/js/tabulator.min.js"></script>   
 <script>
var df2={df_json}
var table = new Tabulator("#tabulator", {{
    data:df2, //set initial table data
     autoColumns:true,
     layout:"fitColumns",
    pagination:"local",
    paginationSize:10,
    movableColumns:true,
    paginationCounter:"rows",
}});
 </script>
"""
components.html(
    tabulator_html,
    height=450,
)

# create a pivot table
df_pivot = pd.pivot_table(
    df,
    values="Pounds Consumed Per Capita",
    index="Year",
    columns="Fruit",
    aggfunc=np.sum,
)
# df_pivot

# get list of unique fruit
fruits = df.Fruit.unique()

# sidebar
st.sidebar.header("Parameters")
select_fruit = st.sidebar.selectbox("Select Fruit", fruits)

st.caption("charts built using altair")
st.write(select_fruit)
# create a df based on dropdown selection
select_fruit_filter = df["Fruit"] == select_fruit
fruit_df = df[select_fruit_filter]
fruit_df.sort_values(by=["Year"])
fruit_df = fruit_df.drop("Fruit", axis=1)
fruit_df = fruit_df.drop("Category", axis=1)
fruit_df = fruit_df.drop("Type", axis=1)
fruit_df["Year"] = df["Year"].astype("string")
# first chart
c = alt.Chart(fruit_df).mark_line().encode(x="Year", y="Pounds Consumed Per Capita")
st.altair_chart(c, use_container_width=True)

# wip create df based on list (need to create widget for it)
st.write("selection of fruit wip")
fruit_list = ["Apples", "Oranges", "Limes", "Pears", "Pineapples"]
source = df[df["Fruit"].isin(fruit_list)]

# wip second chart
chart = (
    alt.Chart(source)
    .mark_line()
    .encode(
        y=alt.Y("Pounds Consumed Per Capita:Q", title="Pounds Consumed Per Capita"),
        x="Year:N",
        color="Fruit:N",
    )
    # .properties(height=1500)
)
st.altair_chart(chart, use_container_width=True)
