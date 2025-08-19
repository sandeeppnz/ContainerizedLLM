import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os


load_dotenv()

# BASE_URL = "http://localhost:12434/engines/llama.cpp/v1/"
# client = OpenAI(base_url=BASE_URL, api_key="anything")
client = OpenAI(base_url=os.getenv("BASE_URL"), api_key=os.getenv("API_KEY"))


# MODEL_NAME="ai/smollm2:latest"
# PROMPT="Explain how transformers work."

# messages = [
#     {
#         "role": "user",
#         "content": PROMPT
#     }
# ]

# response = client.chat.completions.create(
#     model=MODEL_NAME,
#     messages=messages
# )

# print(response.choices[0].message.content)

temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1)


st.title("LLM Chat")
prompt = st.text_area("Enter your prompt:", "What is 2+1")

# Send button
if st.button("Send"):
    if not prompt.strip():
        st.warning("Please enter a prompt.")
    else:
        with st.spinner("Thinking..."):
            messages = [{"role": "user", "content": prompt}]
            try:
                response = client.chat.completions.create(
                    model=os.getenv("MODEL"),
                    messages=messages,
                    temperature=temperature,
                )

                # Extract the assistant's reply
                reply = response.choices[0].message.content if response.choices else ""
                if not reply:
                    st.info("No content returned.")
                else:
                    st.success("Response:")
                    st.write(reply)

                # Optional: token/usage info (may be absent on some local servers)
                usage = getattr(response, "usage", None)
                if usage:
                    st.caption(
                        f"Usage — prompt_tokens: {usage.prompt_tokens}, "
                        f"completion_tokens: {usage.completion_tokens}, "
                        f"total_tokens: {usage.total_tokens}"
                    )

            except Exception as e:
                st.error(f"Error calling model: {e}")

# Optional: small help footer
st.caption(
    "Reads BASE_URL, API_KEY, and MODEL from .env. "
    "Works with any OpenAI-compatible Chat Completions endpoint."
)