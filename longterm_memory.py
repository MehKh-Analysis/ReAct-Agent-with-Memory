"""
Adding long term memory with semantic technique
Facts about user as json is stored under a  namespace in langgraph store memory
"""

from langgraph.store.memory import InMemoryStore
import uuid

def build_memory(user_id):
    in_memory_store = InMemoryStore()
    namespace_for_memory = (user_id, "memories")

    # Add some sample memory entries
    
    memory_id = str(uuid.uuid4())
    memory = {
        "interests": ["accounting", "finance", "taxation"],
        "career_goal": "financial analyst"
    }
    in_memory_store.put(namespace_for_memory, memory_id, memory)

    memory_id = str(uuid.uuid4())
    memory = {
        "favorite_courses": [201, 304, 312, 410],
        "notes": "Prefers courses emphasizing accounting systems, financial reporting, and tax principles."
    }
    in_memory_store.put(namespace_for_memory, memory_id, memory)

    # Optional: to keep the name for personalization
    memory_id = str(uuid.uuid4())
    memory = {"name": "Alex"}
    in_memory_store.put(namespace_for_memory, memory_id, memory)

    return in_memory_store

if __name__ == "__main__":
    user_id = "1"
    store = build_memory(user_id)

    # Example search: find all memories mentioning 'finance'
    memories = store.search(
        (user_id, "memories"),
        filter={"career_goal": "financial analyst"}
    )

    print("Retrieved memory entry:")
    print(memories[-1] if memories else "No matching memory found.")
