import sqlite3
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from state import GraphState
from nodes import node_extract_layout, node_summarize, node_index_vectors

# 1. Setup Persistence (Checkpoints)
# This saves your progress in a local file called 'checkpoints.db'
conn = sqlite3.connect("checkpoints.db", check_same_thread=False)
checkpointer = SqliteSaver(conn)

# 2. Build the Workflow
workflow = StateGraph(GraphState)

# 3. Add Nodes
workflow.add_node("parser", node_extract_layout)
workflow.add_node("indexer", node_index_vectors)
workflow.add_node("summarizer", node_summarize)

# 4. Define Edges (The Flow)
workflow.add_edge(START, "parser")
workflow.add_edge("parser", "indexer")
workflow.add_edge("indexer", "summarizer")
workflow.add_edge("summarizer", END)

# 5. Compile the Graph
app = workflow.compile(checkpointer=checkpointer)

def run_analysis(pdf_path: str, persona: str = "executive"):
    config = {"configurable": {"thread_id": "session_1"}}
    inputs = {"file_path": pdf_path, "persona": persona}
    return app.invoke(inputs, config)


try:
    # Generates a PNG of your workflow logic
    app.get_graph().draw_mermaid_png(output_file_path="workflow_map.png")
    print("🎨 Workflow map saved as workflow_map.png")
except Exception:
    # Fallback if dependencies aren't installed
    print(app.get_graph().draw_ascii())