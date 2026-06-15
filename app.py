import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import glob
import os

from evaluator import evaluate_prompt

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_PATH = os.path.join(DATA_DIR, "results.csv")
BENCHMARK_PATH = os.path.join(DATA_DIR, "model_benchmark.csv")


def get_results_path():
    # Prefer last-written path stored in session state (set after evaluation)
    try:
        if 'last_results_path' in st.session_state:
            p = st.session_state['last_results_path']
            if p and os.path.exists(p):
                return p
    except Exception:
        pass

    candidates = glob.glob(os.path.join(DATA_DIR, "results*.csv"))
    if not candidates:
        return RESULTS_PATH

    return max(candidates, key=os.path.getmtime)


def load_full_history():
    files = sorted(
        glob.glob(os.path.join(DATA_DIR, "results*.csv")),
        key=os.path.getmtime
    )
    if not files:
        return pd.DataFrame(columns=[
            "Prompt",
            "Response",
            "Latency",
            "Word_Count",
            "Char_Count",
            "Quality_Score",
            "Hallucination_Score",
            "Hallucination_Risk",
            "Response_Rating"
        ])

    frames = []
    for file in files:
        try:
            frames.append(pd.read_csv(file))
        except Exception:
            pass

    if not frames:
        return pd.DataFrame(columns=[
            "Prompt",
            "Response",
            "Latency",
            "Word_Count",
            "Char_Count",
            "Quality_Score",
            "Hallucination_Score",
            "Hallucination_Risk",
            "Response_Rating"
        ])

    return pd.concat(frames, ignore_index=True)


st.set_page_config(
    page_title="LLM Evaluation Platform",
    layout="wide"
)

st.title("🤖 LLM Evaluation & Monitoring Platform")

# ==================================================
# PROMPT INPUT
# ==================================================

st.header("🧠 Evaluate Prompt")

prompt = st.text_area(
    "Enter Prompt",
    height=120
)

if st.button("🚀 Evaluate Prompt"):

    if prompt.strip() != "":

        with st.spinner("Running LLM..."):

            result = evaluate_prompt(prompt)

        st.success("Evaluation Completed")

        st.subheader("Response")

        st.write(result["response"])

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Latency",
            f"{result['latency']}s"
        )

        c2.metric(
            "Words",
            result["word_count"]
        )

        c3.metric(
            "Quality",
            f"{result['quality_score']}%"
        )

        c4.metric(
            "Hallucination",
            f"{result['hallucination_score']}%"
        )

        # If evaluator returned csv metadata, reload from that path
        if result.get("csv_path"):
            RESULTS_PATH_TO_USE = result.get("csv_path")
            st.session_state['last_results_path'] = RESULTS_PATH_TO_USE
        else:
            RESULTS_PATH_TO_USE = get_results_path()

        # Show debug info
        st.caption(f"CSV used: {RESULTS_PATH_TO_USE}")
        st.caption(f"Rows before save: {result.get('rows_before')}")
        st.caption(f"Rows after save: {result.get('rows_after')}")

        # Validate that exactly one row was appended
        rows_before = result.get('rows_before') or 0
        rows_after = result.get('rows_after') or 0
        try:
            if rows_after == rows_before + 1:
                st.success("Row appended to CSV successfully.")
            else:
                st.warning(f"Unexpected CSV row count change: before={rows_before}, after={rows_after}")
        except Exception:
            pass

# ==================================================
# TABS
# ==================================================

tab1, tab2, tab3 = st.tabs([
    "📊 Evaluation",
    "🆚 A/B Testing",
    "🚀 Benchmark"
])
with tab1:

    st.header("📊 Evaluation Dashboard")

    try:

        # Load full historical data from all results files
        df = load_full_history()

        st.subheader("📋 Evaluation Data")

        st.caption(f"Loading dashboard data from: {', '.join(sorted(glob.glob(os.path.join(DATA_DIR, 'results*.csv'))))}")

        st.dataframe(
            df,
            use_container_width=True
        )

        # Ensure Recent Evaluations uses history
        recent = df.tail(10)

        st.subheader("📈 Key Metrics")

        c1, c2, c3, c4, c5 = st.columns(5)

        c1.metric("Prompts", len(df))
        c2.metric("Avg Latency", round(df["Latency"].mean(), 2))
        c3.metric("Avg Words", int(df["Word_Count"].mean()))
        c4.metric("Avg Quality", round(df["Quality_Score"].mean(), 2))
        c5.metric("Avg Hallucination", round(df["Hallucination_Score"].mean(), 2))

        st.divider()

        # Most Detailed Response

        st.subheader("🏆 Most Detailed Response")

        detailed = df.loc[df["Word_Count"].idxmax()]

        st.code(detailed["Prompt"])

        st.success(
            f"Words: {detailed['Word_Count']}"
        )

        st.info(
            f"Quality Score: {detailed['Quality_Score']}%"
        )

        # Highest Quality

        st.subheader("🎯 Highest Quality Prompt")

        best = df.loc[df["Quality_Score"].idxmax()]

        st.code(best["Prompt"])

        st.success(
            f"Quality Score: {best['Quality_Score']}%"
        )

        st.divider()

        # Latency

        st.subheader("⚡ Latency Analysis")

        fig = px.bar(
            df,
            x=df.index,
            y="Latency",
            title="Prompt Latency"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # Response Length

        st.subheader("📝 Response Length Trend")

        fig = px.line(
            df,
            x=df.index,
            y="Word_Count",
            markers=True,
            title="Word Count Trend"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # Quality Trend

        st.subheader("🎯 Quality Score Trend")

        fig = px.line(
            df,
            x=df.index,
            y="Quality_Score",
            markers=True,
            title="Quality Score Over Time"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )        # Hallucination

        st.subheader("🚨 Hallucination Analysis")

        fig = px.bar(
            df,
            x=df.index,
            y="Hallucination_Score",
            color="Hallucination_Risk"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # Latency vs Length

        st.subheader("📊 Latency vs Response Length")

        fig = px.scatter(
            df,
            x="Latency",
            y="Word_Count",
            color="Quality_Score",
            size="Quality_Score"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # Rating Distribution

        st.subheader("⭐ Response Rating Distribution")

        rating_counts = (
            df["Response_Rating"]
            .value_counts()
            .reset_index()
        )

        fig = px.pie(
            rating_counts,
            names="Response_Rating",
            values="count"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # Leaderboard

        st.subheader("🥇 Prompt Leaderboard")

        leaderboard = (
            df.sort_values(
                "Quality_Score",
                ascending=False
            )[
                [
                    "Prompt",
                    "Quality_Score",
                    "Latency",
                    "Response_Rating"
                ]
            ]
        )

        st.dataframe(
            leaderboard,
            use_container_width=True
        )

        # Benchmark Analysis

        st.subheader("🏆 Benchmark Analysis")

        best_prompt = df.loc[
            df["Quality_Score"].idxmax()
        ]

        worst_prompt = df.loc[
            df["Quality_Score"].idxmin()
        ]

        col1, col2 = st.columns(2)

        with col1:

            st.success("Best Prompt")

            st.code(best_prompt["Prompt"])

            st.write(
                f"Quality: {best_prompt['Quality_Score']}"
            )

        with col2:

            st.error("Worst Prompt")

            st.code(worst_prompt["Prompt"])

            st.write(
                f"Quality: {worst_prompt['Quality_Score']}"
            )

        # Highest Hallucination

        st.subheader("⚠ Highest Hallucination Risk")

        hall = df.loc[
            df["Hallucination_Score"].idxmax()
        ]

        st.dataframe(
            hall.to_frame().T,
            use_container_width=True
        )

        # Recent Evaluations

        st.subheader("📄 Recent Evaluations")

        st.dataframe(
            recent,
            use_container_width=True
        )

        # Export

        st.subheader("📥 Export Results")

        csv = df.to_csv(index=False)

        st.download_button(
            "Download Evaluation Report",
            csv,
            file_name="evaluation_report.csv",
            mime="text/csv"
        )

    except Exception as e:

        st.warning(
            f"results.csv not found: {e}"
        )

with tab2:

    st.header("🆚 A/B Prompt Testing")

    try:

        df = pd.read_csv(get_results_path())

        if len(df) >= 2:

            a = df.iloc[-2]
            b = df.iloc[-1]

            col1, col2 = st.columns(2)

            with col1:

                st.subheader("Prompt A")

                st.code(a["Prompt"])

                st.metric(
                    "Quality",
                    a["Quality_Score"]
                )

            with col2:

                st.subheader("Prompt B")

                st.code(b["Prompt"])

                st.metric(
                    "Quality",
                    b["Quality_Score"]
                )

            winner = (
                "Prompt A"
                if a["Quality_Score"] >
                b["Quality_Score"]
                else "Prompt B"
            )

            st.success(
                f"🏆 Winner: {winner}"
            )

        else:

            st.info(
                "Run at least two prompts."
            )

    except:

        st.warning(
            "No results available."
        )

with tab3:

    st.header("🚀 Multi-Model Benchmark")

    try:

        benchmark = pd.read_csv(
            BENCHMARK_PATH
        )

        st.dataframe(
            benchmark,
            use_container_width=True
        )

        fig1 = px.bar(
            benchmark,
            x="Model",
            y="Latency",
            title="Latency Comparison"
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

        fig2 = px.bar(
            benchmark,
            x="Model",
            y="Words",
            title="Word Comparison"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

        fig3 = px.bar(
            benchmark,
            x="Model",
            y="Characters",
            title="Character Comparison"
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )

        fastest = benchmark.loc[
            benchmark["Latency"].idxmin()
        ]

        st.success(
            f"⚡ Fastest Model: {fastest['Model']} ({fastest['Latency']}s)"
        )

    except Exception as e:

        st.warning(
            f"Benchmark file not found: {e}"
        )