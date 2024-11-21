import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go

#################################################
### DATA
#################################################
@st.cache_data(max_entries=5)
def load_data():
    data = pd.read_csv("data/data.csv")
    return data


#################################################
### UI
#################################################

st.title("📊 BGP IP Prefixes Analytics")

IPV4_IPV6_df = load_data()

IPV4_df = IPV4_IPV6_df[IPV4_IPV6_df['Network'].str.contains(r'\.', regex=True)]
IPV6_df = IPV4_IPV6_df[IPV4_IPV6_df['Network'].str.contains(r'\:', regex=True)]

# Read the AS numbers from the file
with open('./data/transitASN.txt', 'r') as file:
    transit_as_numbers = [int(line.strip()) for line in file]

transit_IPV4_df = IPV4_df[IPV4_df['transit_as'].isin(transit_as_numbers)]
transit_IPV6_df = IPV6_df[IPV6_df['transit_as'].isin(transit_as_numbers)]

count_number_ipv4_ipv6_prefixes = len(IPV4_IPV6_df)
count_number_ipv4_prefixes = len(IPV4_df)
count_number_ipv6_prefixes = len(IPV6_df)
count_number_ipv4_transit_prefixes = len(transit_IPV4_df)
count_number_ipv6_transit_prefixes = len(transit_IPV6_df)

count_number_ipv4_ipv6_transit_prefixes = count_number_ipv4_transit_prefixes + count_number_ipv6_transit_prefixes

row_metrics = st.columns(3)

with row_metrics[0]:
    with st.container(border=True):
        st.metric(
            "Total Number of IP Prefixes",
            f"{count_number_ipv4_ipv6_prefixes:,}",  # Adding comma separator
        )
with row_metrics[1]:
    with st.container(border=True):
        st.metric(
            "Total Number of IPV4 Prefixes",
            f"{count_number_ipv4_prefixes:,}",  # Adding comma separator
        )
with row_metrics[2]:
    with st.container(border=True):
        st.metric(
            "Total Number of IPV6 Prefixes",
            f"{count_number_ipv6_prefixes:,}",  # Adding comma separator
        )

colors = ['#FFD700', '#1E90FF']

st.text("IP prefixes coming from transit providers versus external providers - Visualization")

pie_chart_metrics = st.columns(3)

with pie_chart_metrics[0]:
    with st.container():
        values = [count_number_ipv4_ipv6_transit_prefixes, count_number_ipv4_ipv6_prefixes - count_number_ipv4_ipv6_transit_prefixes]
        fig = go.Figure(data=[go.Pie(labels=['IPV4 and IPV6 prefixes coming from transit providers', 'Other IPV4 and IPV6 prefixes'], values=values, hole=.3, marker=dict(colors=colors), showlegend=True, textinfo='value')])
        fig.update_layout(title_text='IPV4 and IPV6', title_x=0.35, legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5))  # Legend below chart
        st.plotly_chart(fig)

with pie_chart_metrics[1]:
    with st.container():
        values = [count_number_ipv4_transit_prefixes, count_number_ipv4_prefixes - count_number_ipv4_transit_prefixes]
        fig = go.Figure(data=[go.Pie(labels=['IPV4 prefixes coming from transit providers', 'Other IPV4 prefixes'], values=values, hole=.3, marker=dict(colors=colors), showlegend=True, textinfo='value')])
        fig.update_layout(title_text='IPV4', title_x=0.45, legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5))  # Legend below chart
        st.plotly_chart(fig)

with pie_chart_metrics[2]:
    with st.container():
        values = [count_number_ipv6_transit_prefixes, count_number_ipv6_prefixes - count_number_ipv6_transit_prefixes]
        fig = go.Figure(data=[go.Pie(labels=['IPV6 prefixes coming from transit providers', 'Other IPV6 prefixes'], values=values, hole=.3, marker=dict(colors=colors), showlegend=True, textinfo='value')])
        fig.update_layout(title_text='IPV6', title_x=0.45, legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5))  # Legend below chart
        st.plotly_chart(fig)


# hopcount_query = """
# SELECT  No_of_Hops,  count(*) AS Count_of_IP_Prefixes
# FROM   (
#     SELECT path,  (LENGTH(path) - LENGTH(REPLACE(path, ' ', ''))) AS No_of_Hops FROM etisalat_project.ipv4_ipv6
#   ) AS subquery
# WHERE   No_of_Hops != 0
# GROUP BY   No_of_Hops
# ORDER BY   No_of_Hops;
# """

# hopcount_df = load_data(hopcount_query)

# import plotly.express as px
# import streamlit as st

# import pandas as pd

# Count the number of IP prefixes (paths) for each hop count
hop_count_distribution = IPV4_IPV6_df['hop_count'].value_counts().sort_index()

# Create a DataFrame for better visualization
hop_count_df = hop_count_distribution.reset_index()
hop_count_df.columns = ['No. of Hops', 'Count of IP Prefixes']

hop_count_df = hop_count_df.iloc[1:, :]

# Create bar chart
fig = px.bar(hop_count_df, x='No. of Hops', y='Count of IP Prefixes',
             labels={'No. of Hops': 'No. of Hops', 'Count of IP Prefixes': 'Count of IP Prefixes'},
             title="Count of IP Prefixes by Number of Hops")
st.plotly_chart(fig)

st.subheader("Count of IP Prefixes by Number of Hops - _Tabular View_ ")
st.table(hop_count_df)
