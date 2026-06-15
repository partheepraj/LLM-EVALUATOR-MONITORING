import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🚀 Multi-Model Benchmark")

df = pd.read_csv(
    "model_benchmark.csv"
)

st.dataframe(df)

fig = px.bar(
    df,
    x="Model",
    y="Latency",
    title="Latency Comparison"
)

st.plotly_chart(fig)

fig2 = px.bar(
    df,
    x="Model",
    y="Words",
    title="Response Length"
)

st.plotly_chart(fig2)