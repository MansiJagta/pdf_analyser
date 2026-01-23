from state_qa import QAState
from embeddings import query_vector_logic  # Uses E5 + sqlite-vec
from llm import engine                     # Your local LLMEngine

def node_retrieve(state: QAState):
    """Retrieves relevant facts from the local vector DB."""
    print("--- NODE: RETRIEVING FACTS ---")
    # Prefix with 'query: ' for E5 accuracy
    query = f"query: {state['question']}"
    docs = query_vector_logic.invoke({"query": query, "file_id": state['file_id']})
    return {"retrieved_context": docs}

def node_answer(state: QAState):
    """Generates an answer based ONLY on the retrieved context."""
    print("--- NODE: GENERATING ANSWER ---")
    prompt = (
        f"Context from PDF:\n{state['retrieved_context']}\n\n"
        f"Question: {state['question']}\n"
        "Constraint: Answer using only the context. If unknown, say you can't find it."
    )
    answer = engine.generate(state['question'], prompt)
    return {"answer": answer, "reflection_count": state.get("reflection_count", 0) + 1}

def node_reflect_qa(state: QAState):
    """Reflector Node: Audits the answer against the source context."""
    print("--- NODE: REFLECTOR (QA AUDIT) ---")
    audit_prompt = (
        f"Context: {state['retrieved_context']}\n"
        f"AI Answer: {state['answer']}\n"
        "Does the answer contain info NOT in the context? Reply 'REWRITE' or 'NO_ERRORS'."
    )
    critique = engine.generate("Audit Answer", audit_prompt)
    return {"critique": critique}