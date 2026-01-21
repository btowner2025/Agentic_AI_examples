# =========================
# Imports
# =========================

# --- Standard library 
from datetime import datetime
import re
import json
import ast
import unittests 

# --- Third-party ---
from IPython.display import Markdown, display
from aisuite import Client

# --- initialize the client
CLIENT = client()

# === planner_agent ===

def planner_agent(topic: str, model: str = "openai:o4-mini") -> list[str]:
    """
    Generates a plan as a Python list of steps (strings) for a research workflow.

    Args:
        topic (str): Research topic to investigate.
        model (str): Language model to use.

    Returns:
        List[str]: A list of executable step strings.
    """

    
    # Build the user prompt
    user_prompt = f"""
    You are a planning agent responsible for organizing a research workflow with multiple intelligent agents.

    🧠 Available agents:
    - A research agent who can search the web, Wikipedia, and arXiv.
    - A writer agent who can draft research summaries.
    - An editor agent who can reflect and revise the drafts.

    🎯 Your job is to write a clear, step-by-step research plan **as a valid Python list**, where each step is a string.
    Each step should be atomic, executable, and must rely only on the capabilities of the above agents.

    🚫 DO NOT include irrelevant tasks like "create CSV", "set up a repo", "install packages", etc.
    ✅ DO include real research-related tasks (e.g., search, summarize, draft, revise).
    ✅ DO assume tool use is available.
    ✅ DO NOT include explanation text — return ONLY the Python list.
    ✅ The final step should be to generate a Markdown document containing the complete research report.

    Topic: "{topic}"
    """

    # Add the user prompt to the messages list
    messages = [{"role": "user", "content": user_prompt}]

    # Call the LLM
    response = CLIENT.chat.completions.create( 
        # Pass in the model
        model=model,
        # Define the messages. Remember this is meant to be a user prompt!
        messages=messages,
        # Keep responses creative
        temperature=1, 
    )

    # Extract message from response
    steps_str = response.choices[0].message.content.strip()

    # Parse steps
    steps = ast.literal_eval(steps_str)

    return steps

# Test your code!
unittests.test_planner_agent(planner_agent)