import streamlit as st
import requests
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import pandas as pd

########################################################
# Loading images to the website
########################################################
icon = Image.open("images/favicon.ico")
image = Image.open("images/pret-a-depenser.png")


########################################################
# Loading dataset
########################################################
df_current_clients = pd.read_csv("datasets/df_current_clients_reduced.csv",
                        usecols = ["AMT_INCOME_TOTAL", "TARGET"], low_memory=True)


########################################################
# General settings
########################################################
st.set_page_config(
    page_title="Prêt à dépenser - Default Risk",
    page_icon=icon,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Report a bug" : None,
        "Get help" : "https://github.com/samirhinojosa/OC-P7-implement-a-scoring-model",
        "About" : 
        '''
        Made with ❤️ by [@samirhinojosa](https://www.samirhinojosa.com/) 
        in OpenClassRooms Data Scientist Training.

        For more information visit the following 
        [link](https://github.com/samirhinojosa/OC-P7-implement-a-scoring-model).
        '''
    }
)


########################################################
# General styles
########################################################
padding = 0
st.markdown(f""" <style>
    .block-container.css-18e3th9.egzxvld2{{
            padding: 20px 60px;
    }}
    .css-v3ay09.edgvbvh1{{
        margin-right: 0;
        margin-left: auto;
        display: block;
    }}
    .css-4yfn50.e1fqkh3o1{{
            padding: 4rem 1rem;
    }}
    #data, #repository{{
        padding: 0px;
    }}
    .css-1kyxreq.etr89bj0{{
        justify-content: center;
    }}
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """, unsafe_allow_html=True
)

hide_menu_style = """
        <style>
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

config = {
    "displayModeBar": False,
    "displaylogo": False
}


########################################################
# Page information
########################################################
st_title = '<h1 style="color:#262730; margin-bottom:0; padding: 1.25rem 0px 0rem;">Prêt à dépenser - Default Risk</h1>'
st_title_hr = '<hr style="background-color:#F0F2F6; width:60%; text-align:left; margin-left:0; margin-top:0">'
st.markdown(st_title, unsafe_allow_html=True)
st.markdown(st_title_hr, unsafe_allow_html=True)


########################################################
# Session for the API
########################################################
def fetch(session, url):

    try:
        result = session.get(url)
        return result.json()
    except Exception:
        return {}

session = requests.Session()


########################################################
# Functions to call the EndPoints
########################################################
@st.cache
def client():
    # Getting clients Id
    #response = fetch(session, f"http://fastapi:8008/api/clients")
    response = requests.get("http://fastapi:8008/api/clients").json()
    if response:
        return response["clientsId"]
    else:
        return "Error"

def client_details(id):
    # Getting client's details
    response = fetch(session, f"http://fastapi:8008/api/clients/{id}")
    if response:
        return response
    else:
        return "Error"

def client_prediction(id):
    # Getting client's prediction
    response = fetch(session, f"http://fastapi:8008/api/predictions/clients/{id}")
    if response:
        return response
    else:
        return "Error"

@st.cache
def statistical_ages():
    # Getting General statistics about ages
    response = fetch(session, f"http://fastapi:8008/api/statistics/ages")
    if response:
        return response
    else:
        return "Error"

@st.cache
def statistical_years_employed():
    # Getting General statistics about ages
    response = fetch(session, f"http://fastapi:8008/api/statistics/yearsEmployed")
    if response:
        return response
    else:
        return "Error"

@st.cache
def statistical_amt_credit():
    # Getting General statistics amt credits
    response = fetch(session, f"http://fastapi:8008/api/statistics/amtCredits")
    if response:
        return response
    else:
        return "Error"


########################################################
# Sidebar section
########################################################
sb = st.sidebar # defining the sidebar
sb.image(image)

sb.markdown("🛰️ **Navigation**")
page_names = ["🏠 Home", "⚙️ Client prediction"]
page = sb.radio("", page_names, index=0)
sb.write('<style>.css-1p2iens { margin-bottom: 0px !important; min-height: 0 !important;}</style>', unsafe_allow_html=True)

msg_sb = sb.info("**How to use it ?** Select the **Home page** to see information related with the project. " \
                "Select **Client prediction** to know whether a specific client will pay the loan based on his information.")

if page == "🏠 Home":

    st.subheader("Project 7 - Implement a scoring model")
    st.markdown("This project is part of [OpenClassRooms Data Scientist training](https://openclassrooms.com/fr/paths/164-data-scientist)"\
                " and has two main objectives:")

    objectives_list = '<ul style="list-style-type:disc;">'\
                        '<li>Building a scoring model that will give a prediction about the probability of a client paying the loan.<br>'\
                        'The mision will be treated as a <strong>binary classification problem</strong>.<br>So, 0 will be the class who repaid/pay '\
                        'the loan and 1 will be the class who did not repay/pay the loan.</li>'\
                        '<li>Build an interactive <strong>dashboard for customer relationship managers</strong> to interpret the predictions made by the model,<br>'\
                        'and improve customer knowledge of customer relationship loaders.</li>'\
                    '</ul>'
    st.markdown(objectives_list, unsafe_allow_html=True)
    
    st.subheader("How to use it ?")
    how_to_use_text = "You can navigate through the <strong>Home page</strong> where you will find information related with the project.<br>"\
                        "Also, you can go to the <strong>Client prediction</strong> to know whether a specific client will pay the loan based on his information"
    st.markdown(how_to_use_text, unsafe_allow_html=True)

    st.subheader("Other information")
    other_text = '<ul style="list-style-type:disc;">'\
                    '<li><h4>Data</h4>'\
                    'The data used to develop this project are based on the <a href="https://www.kaggle.com/" target="_blank">Kaggle\'s</a> competition: '\
                    '<a href="https://www.kaggle.com/c/home-credit-default-risk/overview" target="_blank">Home Credit - Default Risk</a></li>'\
                    '<li><h4>Repository</h4>'\
                    'You can find more information about the project\'s code in its <a href="https://github.com/samirhinojosa/OC-P7-implement-a-scoring-model" target="_blank">Github\' repository</a></li>'\
                '</ul>'
    st.markdown(other_text, unsafe_allow_html=True)

else:

    client_selection_title = '<h3 style="margin-bottom:0; padding: 0.5rem 0px 1rem;">🔎 Client selection</h3>'
    st.markdown(client_selection_title, unsafe_allow_html=True)

    st.info("Select a client to **obtain** information related to **probability** of a client " \
            "**paying the loan**.\nIn addition, you can analyze some stats.")

    client_container_selection = st.container()
    col1_cs, col2_cs, col3_cs = client_container_selection.columns([1, 2, 1])

    with col1_cs:

        client_id = st.selectbox(
            "Client Id list", client()
        )
        see_stats = st.checkbox("See stats")

        result = st.button(label="Predict")

    with col2_cs:

        st.caption("&nbsp;")
        st.caption("&nbsp;")

        if see_stats:
            st.warning("**See stats** will take more time. Are you sure ?")

    with col3_cs:

        st.caption("&nbsp;")

    if result:
    
        data = client_details(client_id)
        ccp, cgs1, cgs2 = (st.container() for i in range(3))

        with ccp:

            client_information_title = '<h3 style="margin-bottom:0; padding: 0.5rem 0px 1rem;">📋 Client information</h3>'
            st.markdown(client_information_title, unsafe_allow_html=True)

            prediction = client_prediction(client_id)
            prediction_value = round(float(list(prediction["probability"].keys())[0]), 3) * 100

            if prediction["repay"] == "Yes":
                st.success("Based on the client's information, the credit application is **accepted!**")
            else:
                if prediction_value > 50:
                    st.warning("It is necessary to **analyze more in details** the client's information to accept the credit")
                else:
                    st.error("Based on the client's information, the credit application is **not accepted!**")

            col1_cp, col2_cp, col3_cp, col4_cp = ccp.columns([2, 1, 1, 1])

            with col1_cp:
                
                figP = go.Figure(
                        go.Indicator(
                            mode = "gauge+number",
                            value = prediction_value,
                            domain = {"x": [0, 1], "y": [0, 1]},
                            gauge = {
                                "axis": {"range": [None, 100], "tickwidth": 1, "tickcolor": "darkblue", "tick0": 0, "dtick": 20},
                                "bar": {"color": "LawnGreen"},
                                "bgcolor": "white",
                                "steps": [
                                    {"range": [0, 60], "color": "Red"},
                                    {"range": [60, 100], "color": "Green"}
                                ],
                            }
                        )   
                    )

                figP.update_layout(
                    paper_bgcolor="white",
                    font={
                        "color": "darkblue",
                        "family": "sans serif"
                    },
                    autosize=False,
                    width=500,
                    height=300,
                    margin=dict(
                        l=50, r=50, b=0, t=0, pad=0
                    ),
                    annotations=[
                        go.layout.Annotation(
                            text=f"<b>Probability that the client will pay the loan</b>",
                            x=0.5, xanchor="center", xref="paper",
                            y=0, yanchor="bottom", yref="paper",
                            showarrow=False,
                        )
                    ]
                )
                
                col1_cp.plotly_chart(figP, config=config, use_container_width=True)

                
            with col2_cp:
                st.caption("&nbsp;")
                st.markdown("**Client id:**")
                st.caption(data["clientId"])
                st.markdown("**Children:**")
                st.caption(data["children"])
                st.markdown("**Years employed:**")
                st.caption(data["yearsEmployed"])

            with col3_cp:
                st.caption("&nbsp;")
                st.markdown("**Gender:**")
                st.caption(data["gender"])
                st.markdown("**Own realty:**")
                st.caption(data["ownRealty"])
                st.markdown("**Anual income:**")
                total_income = "$ {:,.2f}".format(data["totalIncome"])
                st.caption(total_income)

            with col4_cp:
                st.caption("&nbsp;")
                st.markdown("**Age:**")
                st.caption(data["age"])
                st.markdown("**Own car:**")
                st.caption(data["ownCar"])
                st.markdown("**AMT credit:**")
                current_credit = "$ {:,.2f}".format(data["credit"])
                st.caption(current_credit)

        if see_stats:

            # Defining variables to use in graphs
            group_labels = ["Repaid", "Not repaid"]
            colors=["Green", "Red"]

            with cgs1:

                client_information_title = '<h3 style="margin-bottom:0; padding: 0.5rem 0px 1rem;">📊 General statistics</h3>'
                st.markdown(client_information_title, unsafe_allow_html=True)

                st.info("Below, you can see some general statistics about clients who " \
                        "repaid and do not repaid the loan")

                col1_gs_1, col2_gs_1 = cgs1.columns(2)

                with col1_gs_1:

                    ########################################################
                    # statistical Ages
                    ########################################################

                    st.caption("&nbsp;")

                    ages = statistical_ages()
                    ages_repaid = ages["ages_repaid"]
                    ages_not_repaid = ages["ages_not_repaid"]
                    ages_repaid_list = [int(key) for key, val in ages_repaid.items() for _ in range(val)]
                    ages_not_repaid_list = [int(key) for key, val in ages_not_repaid.items() for _ in range(val)]

                    fig_ages = ff.create_distplot([ages_repaid_list, ages_not_repaid_list], 
                                                group_labels, show_hist=False, show_rug=False, 
                                                colors=colors)
                    fig_ages.update_layout(
                        paper_bgcolor="white",
                        font={
                            "family": "sans serif"
                        },
                        autosize=False,
                        width=500,
                        height=360,
                        margin=dict(
                            l=50, r=50, b=0, t=20, pad=0
                        ),
                        title={
                            "text" : "Client's age vs Current clients",
                            "y" : 1,
                            "x" : 0.45,
                            "xanchor" : "center",
                            "yanchor" : "top"
                        },
                        xaxis_title="Ages",
                        yaxis_title="density",
                        legend={
                            "traceorder" : "normal"
                        }
                    )
                    fig_ages.add_vline(x=data["age"], line_width=3,
                                    line_dash="dash", line_color="blue", annotation_text="Client's age")

                    col1_gs_1.plotly_chart(fig_ages, config=config, use_container_width=True)

                with col2_gs_1:

                    ########################################################
                    # statistical Years Employed
                    ########################################################

                    st.caption("&nbsp;")
                    
                    years_employed = statistical_years_employed()
                    years_employed_repaid = years_employed["years_employed_repaid"]
                    years_employed_not_repaid = years_employed["years_employed_not_repaid"]
                    years_employed_repaid_list = [int(key) for key, val in years_employed_repaid.items() for _ in range(val)]
                    years_employed_not_repaid_list = [int(key) for key, val in years_employed_not_repaid.items() for _ in range(val)]

                    fig_years_worked = ff.create_distplot([years_employed_repaid_list, years_employed_not_repaid_list], 
                                                group_labels, show_hist=False, show_rug=False, 
                                                colors=colors)

                    fig_years_worked.update_layout(
                        paper_bgcolor="white",
                        font={
                            "family": "sans serif"
                        },
                        autosize=False,
                        width=500,
                        height=360,
                        margin=dict(
                            l=50, r=50, b=0, t=20, pad=0
                        ),
                        title={
                            "text" : "Years employed by the client vs Current clients",
                            "y" : 1,
                            "x" : 0.45,
                            "xanchor" : "center",
                            "yanchor" : "top"
                        },
                        xaxis_title="Years employed",
                        yaxis_title="density",
                        legend={
                            "traceorder" : "normal"
                        }
                    )
                    fig_years_worked.add_vline(x=data["yearsEmployed"], line_width=3,
                                    line_dash="dash", line_color="blue", annotation_text="Years employed by the client")

                    col2_gs_1.plotly_chart(fig_years_worked, config=config, use_container_width=True)


            with cgs2:    

                col1_gs_2, col2_gs_2 = cgs2.columns(2)

                with col1_gs_2:

                    ########################################################
                    # Statistical AMT Credit
                    ########################################################

                    st.caption("&nbsp;")

                    amt_credit = statistical_amt_credit()
                    amt_credit_repaid = amt_credit["amt_credit_repaid"]
                    amt_credit_not_repaid = amt_credit["amt_credit_not_repaid"]
                    amt_credit_repaid_list = [float(key) for key, val in amt_credit_repaid.items() for _ in range(val)]
                    amt_credit_not_repaid_list = [float(key) for key, val in amt_credit_not_repaid.items() for _ in range(val)]

                    fig_amt_credit = ff.create_distplot([amt_credit_repaid_list, amt_credit_not_repaid_list], 
                                                group_labels, show_hist=False, show_rug=False, 
                                                colors=colors)

                    fig_amt_credit.update_layout(
                        paper_bgcolor="white",
                        font={
                            "family": "sans serif"
                        },
                        autosize=False,
                        width=500,
                        height=360,
                        margin=dict(
                            l=50, r=50, b=0, t=20, pad=0
                        ),
                        title={
                            "text" : "Client's AMT credit vs Current clients",
                            "y" : 1,
                            "x" : 0.45,
                            "xanchor" : "center",
                            "yanchor" : "top"
                        },
                        xaxis_title="AMT Credit",
                        yaxis_title="density",
                        legend={
                            "traceorder" : "normal"
                        }
                    )
                    fig_amt_credit.add_vline(x=data["credit"], line_width=3,
                                    line_dash="dash", line_color="blue", annotation_text="Client's AMT credit")

                    col1_gs_2.plotly_chart(fig_amt_credit, config=config, use_container_width=True)

                with col2_gs_2:

                    st.caption("&nbsp;")

                    fig_income = px.histogram(df_current_clients, x="AMT_INCOME_TOTAL", color="TARGET", 
                            color_discrete_map={0:"Green", 1:"Red"}, labels={0:"Green", 1:"Red"})

                    fig_income.update_layout(
                        paper_bgcolor="white",
                        font={
                            "family": "sans serif"
                        },
                        autosize=False,
                        width=500,
                        height=360,
                        margin=dict(
                            l=50, r=50, b=0, t=20, pad=0
                        ),
                        title={
                            "text" : "Client's Income vs Current clients",
                            "y" : 1,
                            "x" : 0.45,
                            "xanchor" : "center",
                            "yanchor" : "top"
                        },
                        xaxis_title="Income",
                        legend_title_text= "",
                        showlegend=False,
                        xaxis_range=[25000, 300000]
                    )
                    fig_income.add_vline(x=data["totalIncome"], line_width=3,
                                    line_dash="dash", line_color="blue", annotation_text="Client's income")

                    col2_gs_2.plotly_chart(fig_income, config=config, use_container_width=True)