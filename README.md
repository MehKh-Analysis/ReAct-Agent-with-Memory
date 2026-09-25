# ReAct-Agent-with-Memory

AI agent that combines reasoning, tool use, and memory-driven personalization to help students explore academic courses intelligently.

The agent is powered by the ReAct (Reason + Act) architecture and integrates Ollama with the Llama 3.2 model for reasoning and tool-based actions.

---

**⚙️ How It Works**

Dataset:
The agent uses a dataset of 12,000+ courses (27 features each), including fields such as course number, name, registration status, and description.

[course-catalog data set](https://drive.google.com/file/d/1sfmf_pnHCYM8kq7QfpFrktvENvsi7Xvw/view?usp=sharing)

Tool:
A custom tool called find_course retrieves course details when a student asks something like:

“What’s the course with number 287?”

Short-Term Memory:
Thread-based memory that allows for multi-turn conversations within the same chat session.

Long-Term Memory:
Semantic memory that stores user profiles in a JSON-like structure to personalize recommendations based on preferences, career interests, or favorite courses.

---

`Agent_no_memory.py` -- agent is built as a base line with no memory

`Agent_short_and_long_memory.py` -- agent with added memory

`longterm_memory.py` -- defining the semantic memory profile

---

**🚀 How to Run**

1. Install [Ollama](https://ollama.com) and pull the model:

```bash
ollama pull llama3.2
```

2. Install the Python dependencies:

```bash
pip install -r requirements.txt
```

3. Download the [course catalog](https://drive.google.com/file/d/1sfmf_pnHCYM8kq7QfpFrktvENvsi7Xvw/view?usp=sharing) and save it as `data/course-catalog.csv`.

4. Run the agent:

```bash
python Agent_no_memory.py                # baseline, no memory
python Agent_short_and_long_memory.py    # with short- and long-term memory
```
