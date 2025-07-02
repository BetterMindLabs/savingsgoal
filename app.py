import streamlit as st
import google.generativeai as genai

# Configure Gemini
genai.configure(api_key=st.secrets["API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

st.title("💸 Personalized Saving Goal Assistant")

st.markdown("""
Plan your savings, set achievable goals, and get personalized AI tips to stay on track!
""")

# Inputs
monthly_income = st.number_input("Your Monthly Income (₹)", min_value=1000, value=50000)
monthly_expenses = st.number_input("Your Monthly Expenses (₹)", min_value=500, value=30000)
saving_goal = st.number_input("Your Total Saving Goal (₹)", min_value=1000, value=200000)
goal_months = st.slider("Target Months to Reach Goal", 1, 60, 12)

if st.button("Generate Saving Plan"):
    # Calculate potential savings per month
    possible_saving = monthly_income - monthly_expenses

    # Suggested required saving per month to meet goal
    required_saving = saving_goal / goal_months

    st.markdown("---")
    st.subheader("💡 Analysis")

    st.write(f"**Possible saving per month (current):** ₹{possible_saving}")
    st.write(f"**Required saving per month to reach goal:** ₹{required_saving:.2f}")

    if possible_saving >= required_saving:
        st.success("🎉 You can achieve this goal comfortably with your current budget!")
    else:
        st.warning("⚠️ Your current possible savings are less than what you need to meet the goal.")

    # Gemini prompt
    prompt = f"""
    Here is my saving plan:
    - Monthly income: ₹{monthly_income}
    - Monthly expenses: ₹{monthly_expenses}
    - Total saving goal: ₹{saving_goal}
    - Target months: {goal_months}
    - Possible saving per month: ₹{possible_saving}
    - Required saving per month: ₹{required_saving:.2f}

    Please give me:
    - Personalized advice on how to increase my monthly savings.
    - Simple, practical expense reduction tips.
    - Motivational message to help me stay committed.
    Present it in a friendly and encouraging style.
    """

    with st.spinner("Consulting Gemini..."):
        response = model.generate_content(prompt)
        advice = response.text

    st.markdown("---")
    st.subheader("🤖 Gemini AI Recommendations")
    st.markdown(advice)

st.caption("✨ Built with Python, Streamlit & Gemini API")
