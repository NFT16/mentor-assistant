import streamlit as st
import requests
import os

st.set_page_config(page_title="EEF AI Mentor Assistant", page_icon="🎓", layout="wide")
st.title("🎓 EEF AI Mentor Assistant")
st.caption("Knowledge retrieval • Mentor makes final decisions")

try:
    default_api_url = st.secrets["API_URL"]
except Exception:
    default_api_url = "https://mentor-assistant-api.onrender.com"

API_URL = st.sidebar.text_input(
    "Backend API URL", default_api_url
).rstrip("/")

try:
    response = requests.get(f"{API_URL}/health", timeout=10)
    response.raise_for_status()
except Exception as exc:
    st.error(f"Backend is not running or unavailable: {exc}")
    st.stop()

try:
    response = requests.get(f"{API_URL}/interns", timeout=10)
    response.raise_for_status()
    interns = response.json()
except requests.RequestException as exc:
    st.error(f"Could not load intern profiles: {exc}")
    st.stop()

choices = {
    f"{x['name']} ({x['intern_id']})": x["intern_id"]
    for x in interns
}

tabs = st.tabs([
    "Student Assistant",
    "Intern Profiles",
    "Mentor Dashboard",
    "Learning Plan"
])

with tabs[0]:
    st.subheader("Ask an internship question")

    selected = st.selectbox(
        "Optional intern context",
        ["No intern selected"] + list(choices)
    )

    intern_id = choices.get(selected)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    question = st.chat_input(
        "Ask about tasks, case studies, feedback, or debugging..."
    )

    if question:
        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):
            st.markdown(question)

        try:
            res = requests.post(
                f"{API_URL}/chat",
                json={
                    "question": question,
                    "intern_id": intern_id
                },
                timeout=30
            )
            res.raise_for_status()
            data = res.json()

            with st.chat_message("assistant"):
                st.markdown(data["answer"])

                if "confidence" in data:
                    st.caption(
                        f"Heuristic retrieval confidence: {data['confidence']:.0%}"
                    )

                if data.get("sources"):
                    with st.expander("Retrieved sources"):
                        for src in data["sources"]:
                            st.write(
                                f"{src['title']} · {src['source']} · score {src['score']}"
                            )

            st.session_state.messages.append({
                "role": "assistant",
                "content": data["answer"]
            })

        except requests.RequestException as exc:
            st.error(f"API request failed: {exc}")

with tabs[1]:
    st.subheader("Sample intern profiles")

    for intern in interns:
        with st.expander(f"{intern['name']} — {intern['track']}"):
            a, b, c = st.columns(3)

            a.metric("Progress", f"{intern['progress']}%")
            b.metric(
                "Tasks",
                f"{intern['tasks_completed']}/{intern['tasks_total']}"
            )
            c.metric("Status", intern["status"])

            st.write(
                "**Current skills:**",
                ", ".join(intern["skills"])
            )

            st.write(
                "**Required skills:**",
                ", ".join(intern["required_skills"])
            )

with tabs[2]:
    st.subheader("Mentor overview")

    try:
        dashboard_response = requests.get(
            f"{API_URL}/mentor/dashboard",
            timeout=10
        )
        dashboard_response.raise_for_status()
        dashboard = dashboard_response.json()["interns"]
    except requests.RequestException as exc:
        st.error(f"Could not load mentor dashboard: {exc}")
        dashboard = []

    for intern in dashboard:
        with st.container(border=True):
            left, right = st.columns([2, 1])

            left.markdown(
                f"### {intern['name']} · {intern['track']}"
            )

            left.write(intern["latest_feedback"])

            left.write(
                "**Skill gaps:** " +
                (", ".join(intern["skill_gaps"]) or "No listed gaps")
            )

            right.metric(
                "Progress",
                f"{intern['progress']}%"
            )

            right.metric(
                "Rule-based risk flag",
                intern["risk_level"]
            )

    st.info(
        "These are illustrative flags based on sample data, not final performance decisions."
    )

with tabs[3]:
    st.subheader("Personalized learning plan")

    selected_plan = st.selectbox(
        "Choose intern",
        list(choices),
        key="plan_intern"
    )

    if st.button("Generate learning plan"):
        try:
            result_response = requests.get(
                f"{API_URL}/interns/{choices[selected_plan]}/learning-plan",
                timeout=10
            )
            result_response.raise_for_status()
            result = result_response.json()

            st.write(
                "**Skill gaps:**",
                ", ".join(result["skill_gaps"]) or "None identified"
            )

            for item in result["plan"]:
                st.markdown(
                    f"**Week {item['week']}: {item['focus']}**"
                )
                st.write(item["milestone"])

        except requests.RequestException as exc:
            st.error(f"Could not generate learning plan: {exc}")