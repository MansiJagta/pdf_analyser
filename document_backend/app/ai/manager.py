import sqlite3
from langgraph.graph import StateGraph, START, END
# from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.checkpoint.memory import MemorySaver

# Import your state definition and specialized nodes
# from state import GraphState
from app.ai.state import GraphState
from app.ai.nodes import (
    node_extract_layout, 
    node_index_vectors, 
    node_generate_draft, 
    node_finalize
)

# 1. Setup Persistence (Checkpoints)
# conn = sqlite3.connect("checkpoints.db", check_same_thread=False)
# checkpointer = SqliteSaver(conn)
# FIX: Use MemorySaver for async compatibility by default
checkpointer = MemorySaver()

# 3. Build the Workflow Structure
workflow = StateGraph(GraphState)

# 4. Register Nodes
workflow.add_node("parser", node_extract_layout)      # Text/Layout extraction
workflow.add_node("indexer", node_index_vectors)      # Member 4: Vector Storage
workflow.add_node("generator", node_generate_draft)   # Draft Creation
workflow.add_node("finalize", node_finalize)          # Finalizes 'summary' key

# 5. Define Edges (The Linear Flow)
workflow.add_edge(START, "parser")
workflow.add_edge("parser", "indexer")
workflow.add_edge("indexer", "generator")

# ⚡ CHANGE: Linear flow straight to 'finalize'
# This removes the memory-heavy loop that causes the fatal error.
workflow.add_edge("generator", "finalize")

# Ensure finalize leads to END
workflow.add_edge("finalize", END)

# 7. Compile the Application
app = workflow.compile(checkpointer=checkpointer)


# 8. Execution Wrapper
def run_analysis(pdf_path: str, persona: str = "technical_architect", query: str = "Summarize"):
    # Using a unique thread_id per session to maintain history in the DB
    config = {"configurable": {"thread_id": f"session_{pdf_path.split('/')[-1]}"}}
    
    inputs = {
        "file_path": pdf_path, 
        "persona": persona,
        "query": query,
        "reflection_count": 0,
        "summary": "",
        "draft": "",
        "critique": ""
    }
    
    return app.invoke(inputs, config)

# Optional: Draw the map
try:
    app.get_graph().draw_mermaid_png(output_file_path="graph_structure.png")
    print("Graph structure saved as graph_structure.png")
except Exception as e:
    print(f"Could not draw graph: {e}")