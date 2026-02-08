from app.ai.pdf_parser import extract_pdf_logic
from app.ai.embeddings import index_vector_logic
from app.ai.llm import engine
from app.ai.persona import PERSONAS

def node_extract_layout(state):
    print("--- NODE: EXTRACTING TEXT & LAYOUT ---")
    tool_result = extract_pdf_logic.invoke({"file_path": state['file_path']})
    return {
        "raw_text": tool_result["content"], 
        "layout_type": "scanned" if tool_result["is_scanned"] else "digital"
    }

def node_index_vectors(state):
    print("--- NODE: INDEXING TO SQLITE-VEC ---")
    index_vector_logic.invoke({"text": state['raw_text']})
    return {"vector_status": "completed"}

def node_generate_draft(state):
    """Generates the initial draft using Llama-3.2 specific ChatML headers."""
    print(f"--- NODE: GENERATING DRAFT AS {state['persona'].upper()} ---")
    
    persona_key = state.get('persona', 'executive').lower()
    persona_prompt = PERSONAS.get(persona_key, "Summarize this document clearly.")
    
    # Grab context from extracted text
    # 📉 Reduced to 2500 chars (~600 tokens) to ensure prompt fit in 800 token limit
    source_text = state.get('raw_text', '')[:2500]
    
    # Dynamic Temperature: Lower (0.1) for CTO/Architect, slightly higher for others
    temp_map = {"cto": 0.1, "software_architect": 0.1, "product_manager": 0.3}
    current_temp = temp_map.get(persona_key, 0.2)

    # 1. System Prompt holds the PDF context and persona constraints
    system_instructions = (
        f"{persona_prompt}\n\n"
        "STRICT RULES:\n"
        "- Generate a comprehensive summary of at least 200 words.\n"
        "- Focus strictly on architecture, implementation, and technical feasibility.\n"
        "- DO NOT mention 'Acting Director' or internal instruction labels.\n\n"
        f"DOCUMENT CONTENT:\n{source_text}"
    )

    # 2. User Query holds the specific task
    user_query = "Provide a deep technical breakdown of the system architecture and its core modules."

    try:
        # Pass the temperature to the updated engine.generate method
        draft = engine.generate(user_query, system_instructions, temperature=current_temp)
    except Exception as e:
        print(f"Error during generation: {e}")
        draft = "Error: Could not generate draft. Ensure Llama-3.2 model is in assets/."

    return {
        "draft": draft, 
        "reflection_count": 1
    }

def node_reflect_critic(state):
    """The Reflector Node: Binary check using the Instruct template."""
    print("--- NODE: REFLECTOR (CRITIC) ---")
    
    critic_prompt = (
        "You are a technical editor. Review the following summary for accuracy and repetition. "
        "If it repeats lines, lacks technical detail, or mentions persona names (like 'CTO'), "
        "output ONLY the word 'REWRITE'. "
        "If it is high-quality and correct, output ONLY 'NO_ERRORS_FOUND'."
    )
    
    critique = engine.generate(f"TEXT TO CHECK: {state['draft']}", critic_prompt, temperature=0.1)
    return {"critique": critique}

def node_refine_answer(state):
    """Refines the answer using Llama-3.2's stronger reasoning capabilities."""
    print(f"--- NODE: REFINER - ITERATION {state.get('reflection_count')} ---")
    current_count = state.get('reflection_count', 1)

    persona_key = state.get('persona', 'executive').lower()
    persona_instruction = PERSONAS.get(persona_key)

    system_instructions = (
        f"Role: {persona_instruction}\n"
        "Task: Technical refinement. Remove any conversational filler or instruction leakage.\n"
        "Do NOT remove any technical names, version numbers, or specific module names from the original draft unless they are explicitly identified as errors.\n"
        "Output only the improved facts."
    )

    context_data = f"DRAFT: {state['draft']}\nCRITIQUE: {state['critique']}"
    refined_draft = engine.generate(context_data, system_instructions, temperature=0.1)

    return {
        "draft": refined_draft.strip(),
        "reflection_count": current_count + 1
    }

def node_finalize(state):
    """Final cleaning for professional formatting."""
    print("--- NODE: FINALIZING & CLEANING ---")
    
    raw_text = state.get("draft", "")
    if not raw_text:
        return {"summary": "Error: Finalization failed."}

    # Remove instruction noise that might leak from Llama-3.2
    forbidden = ["Task:", "Constraint:", "Role:", "Rewrite", "OPTIONS:", "Acting Director"]

    lines = raw_text.split('\n')
    unique_lines = []
    seen = set()

    for line in lines:
        stripped = line.strip()
        if not stripped or len(stripped) < 15: # Filter out short noise
            continue
            
        if any(word.lower() in stripped.lower() for word in forbidden):
            continue

        if stripped.lower() not in seen:
            unique_lines.append(stripped)
            seen.add(stripped.lower())

    final_summary = "\n\n".join(unique_lines)
    return {"summary": final_summary}
