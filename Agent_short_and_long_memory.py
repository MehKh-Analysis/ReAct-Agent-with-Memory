
"""
Goal is to build a ReAct style agent ,
Using ollam to chat with LLM 
Adding short term and long term memory capabilities to the agent

"""


# Import required libraries for langchain-react approach
import pandas as pd
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.tools import tool
from langchain.agents import create_agent
from pathlib import Path 
from langgraph.checkpoint.memory import MemorySaver
from termcolor import colored


# Call long term memory module  
from longterm_memory import build_memory

# Define a tool to find course name & description from course number  
@tool
def find_course(number:int):
   
    """
    the goal of this tool is to help students find the course name and course description by the course number
    use this tool when user query the course number and needs the name and description of the course
    """
    print(f"Tool called is find_course for {number}")
    data_dir=Path("./data")
    name="course-catalog"
    csv_path=data_dir/f"{name}.csv"
    if csv_path.exists():
        df=pd.read_csv(csv_path)
        #print("File loaded successfully!")
    else: print("file not found")
    
    df.columns=df.columns.str.strip()
    
    df["Number"] = pd.to_numeric(df["Number"], errors="coerce").astype("Int64")
    if number in df["Number"].tolist():
        course_info=df.loc[df["Number"]==number, ["Name", "Description"]].iloc[0]
        course_name = course_info["Name"]
        course_description = course_info["Description"]
        print(f"Course {number}: {course_name}\nDescription: {course_description}")
        return course_name , course_description
    else :
        print("Wrong course number, use course numbers like 100,201,283,...")
        return None, None  
    
    #return course_name , course_description
if __name__ == "__main__":
    user_id = "1"

    # Load long-term memory (from JSON-like profile)
    store = build_memory(user_id)

    # Retrieve all user memories
    user_memories = store.search((user_id, "memories"))
    print("Loaded Long-Term Memory:")
    for mem in user_memories:
        print(mem)

    # merge the memory context for personalization
    # e.g., add user interests and career goals into the system prompt
    memory_context = ""
    for mem in user_memories:
    # Each mem.value is actual dictionary (like {"career_goal": "financial analyst"})
       for key, value in mem.value.items():
        memory_context += f"{key}: {value}\n"


    # Combine system message with memory context
    system_message = (
        "You are an academic advisor at a college. "
        "When a student asks about a course, use the tool to provide the name and description. "
        "After showing the course info, also explain how it relates to their career goals and interests very very short like a keyword.\n\n"
        f"Here is the student's background memory:\n{memory_context}"
    )

    Tools = [find_course]
    chat_model = ChatOllama(
        base_url="http://localhost:11434",
        model="llama3.2:latest",
        temperature=0
    )

    checkpointer = MemorySaver()
    graph = create_agent(
        model=chat_model, # "gpt-4o-mini",#
        tools=Tools,
        system_prompt=system_message,
        checkpointer=checkpointer
    )
    

    # Example user query
    query = "What is the course with number 304?"

    init_messages = {
        "messages": [
            SystemMessage(content="Provide the course info and career relevance."),
            HumanMessage(content=query)
        ]
    }

    cfg = {"configurable": {"thread_id": "student-session-001"}}

    print(colored("\n==== Turn 1: Student asks for course info ====\n", "cyan", attrs=["bold"]))
    state1 = graph.invoke(init_messages, config=cfg)
    ans = state1["messages"][-1].content
    print(ans)

    print(colored("\n==== Turn 2: Student asks follow-up ====\n", "green", attrs=["bold"]))
    follow_up = {"messages": [HumanMessage(content="Give me three career roles this course would be beneficial for very short just like keywords.")]}
    state2 = graph.invoke(follow_up, config=cfg)

    
    print(state2["messages"][-1].content)
    print("\n==== Demo Complete: Memory maintained across turns ====\n")


