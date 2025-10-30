
"""
Goal is to build a ReAct style agent ,
using ollam to chat with LLM 
and later adding memory capabilities to the agent

"""

# Import required libraries for langchain-react approach
import pandas as pd
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.tools import tool
from langchain.agents import create_agent
from pathlib import Path 

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
        print("File loaded successfully!")
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
if __name__ == "__main__" : 
    
    system_message=(
        "You are an academic advisor at a college, when student ask about a course, call the relevent tool to provide course name and description.\n" 
        " Do not answer directly, Always use the tool "
    )
    Tools=[find_course]
    chat_model = ChatOllama(
        base_url="http://localhost:11434",
        model="llama3.2:latest",
        temperature=0
    )
    graph = create_agent(
        model=chat_model, # "gpt-4o-mini",#
        tools=Tools,
        system_prompt=system_message
    )
  
    query = "What's the course with number 287?"
    # add an extra explainatio note : course application in future career path
    init_messages = {
        "messages": [
            SystemMessage(content="regarding the course name and description add a short extra note of this course application in future career path"),
            HumanMessage(content=query)
        ]
    }

    state = graph.invoke(init_messages)
    ans = state["messages"][-1].content
    print(ans)


