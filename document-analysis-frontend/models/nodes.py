# from pdf_parser import HybridParser
# from llm import LLMEngine
# from embeddings import VectorEngine
# from persona import PERSONAS

# # Initialize tools once to save memory
# parser = HybridParser()
# vector_db = VectorEngine()

# def node_extract_layout(state):
#     """Detects if PDF is digital or needs OCR and extracts text."""
#     print("--- NODE: EXTRACTING TEXT & LAYOUT ---")
#     text, is_scanned = parser.extract(state['file_path'])
#     return {
#         "raw_text": text, 
#         "layout_type": "scanned" if is_scanned else "digital"
#     }

# def node_summarize(state):
#     """Generates a summary based on the chosen persona."""
#     print(f"--- NODE: SUMMARIZING AS {state['persona']} ---")
#     engine = LLMEngine(model_path="assets/smollm2.gguf")
#     prompt = PERSONAS.get(state['persona'].lower(), PERSONAS['executive'])
#     summary = engine.generate(state['raw_text'], prompt)
#     return {"summary": summary}

# def node_index_vectors(state):
#     """Stores the text in a local SQLite-vec database."""
#     print("--- NODE: INDEXING TO SQLITE-VEC ---")
#     vector_db.index_text(state['raw_text'])
#     return {"vector_status": "completed"}










# from pdf_parser import HybridParser
# from llm import LLMEngine
# from embeddings import VectorEngine
# from persona import PERSONAS

# # Initialize tool instances
# # When using @tool, these become 'StructuredTool' objects
# parser_instance = HybridParser()
# vector_instance = VectorEngine()

# def node_extract_layout(state):
#     """Detects if PDF is digital or needs OCR and extracts text."""
#     print("--- NODE: EXTRACTING TEXT & LAYOUT ---")
    
#     # Since 'extract' is a @tool, we MUST use .invoke()
#     # We pass the input as a dictionary matching the function arguments
#     tool_result = parser_instance.extract.invoke({"file_path": state['file_path']})
    
#     # tool_result is the dictionary returned by your HybridParser.extract
#     return {
#         "raw_text": tool_result["content"], 
#         "layout_type": "scanned" if tool_result["is_scanned"] else "digital"
#     }

# def node_summarize(state):
#     """Generates a summary based on the chosen persona."""
#     print(f"--- NODE: SUMMARIZING AS {state['persona']} ---")
    
#     # Initialize the LLM Engine with your local GGUF path
#     engine = LLMEngine(model_path="assets/smollm2.gguf")
    
#     # Get the specific persona instructions
#     prompt = PERSONAS.get(state['persona'].lower(), PERSONAS['executive'])
    
#     # Generate summary using the raw_text from the previous node
#     summary = engine.generate(state['raw_text'], prompt)
    
#     return {"summary": summary}

# def node_index_vectors(state):
#     """Stores the text in a local SQLite-vec database."""
#     print("--- NODE: INDEXING TO SQLITE-VEC ---")
    
#     # Use .invoke() for the vector tool
#     vector_instance.index_text.invoke({"text": state['raw_text']})
    
#     return {"vector_status": "completed"}









# # Import the tools directly
# from pdf_parser import extract_pdf_logic
# from embeddings import index_vector_logic
# from llm import LLMEngine
# from persona import PERSONAS

# def node_extract_layout(state):
#     print("--- NODE: EXTRACTING TEXT & LAYOUT ---")
    
#     # Call the standalone tool via .invoke()
#     # We no longer need an 'instance' or 'self'
#     tool_result = extract_pdf_logic.invoke({"file_path": state['file_path']})
    
#     return {
#         "raw_text": tool_result["content"], 
#         "layout_type": "scanned" if tool_result["is_scanned"] else "digital"
#     }

# def node_index_vectors(state):
#     print("--- NODE: INDEXING TO SQLITE-VEC ---")
    
#     # Call the vector tool via .invoke()
#     index_vector_logic.invoke({"text": state['raw_text']})
    
#     return {"vector_status": "completed"}

# def node_summarize(state):
#     """Generates a summary based on the chosen persona."""
#     print(f"--- NODE: SUMMARIZING AS {state['persona']} ---")
#     engine = LLMEngine(model_path="assets/smollm2.gguf")
#     # prompt = PERSONAS.get(state['persona'].lower(), PERSONAS['executive'])
#     prompt = PERSONAS.get(state['persona'].lower(), "Summarize this document clearly.")
#     summary = engine.generate(state['raw_text'], prompt)
#     print(f"DEBUG: AI generated {len(summary)} characters.")
#     return {"summary": summary}







# Import the tools directly
from pdf_parser import extract_pdf_logic
from embeddings import index_vector_logic
from llm import LLMEngine
from persona import PERSONAS

# Initialize Engine once to save memory in local environment
engine = LLMEngine(model_path="assets/smollm2.gguf")

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

# --- UPDATED REFLECTOR LOGIC NODES ---

  
def node_reflect_critic(state):
    """The Reflector Node: Binary check for accuracy/quality."""
    print("--- NODE: REFLECTOR (CRITIC) ---")
def node_generate_draft(state):
    """Generates the initial draft with structured constraints to prevent repetition."""
    print(f"--- NODE: GENERATING DRAFT AS {state['persona'].upper()} ---")
    
    # 1. Safely get the persona
    persona_key = state.get('persona', 'executive').lower()
    persona_prompt = PERSONAS.get(persona_key, "Summarize this document clearly.")
    
    # 2. Safely get the query
    query_text = state.get('query') or "Provide a technical overview"
    
    # 3. Handle the Raw Text (Chunking to prevent LLM confusion)
    # We take the first 3000 characters to ensure the model stays focused
    source_text = state.get('raw_text', '')[:3000]
    
    # 4. DEFINING FULL_PROMPT (This fixes your UnboundLocalError)
    # We use a structured format that forces the AI to provide facts, not fluff
    full_prompt = (
    f"Role: {persona_prompt}\n"
    "Task: Provide a technical breakdown in 3-5 unique bullet points.\n"
    "Constraint: Each bullet point must cover a DIFFERENT aspect of the document. "
    "Do NOT repeat information across points.\n\n"
    f"Content: {source_text}\n"
   )
    
    # 5. Generate the result
    try:
        draft = engine.generate(query_text, full_prompt)
    except Exception as e:
        print(f"Error during generation: {e}")
        draft = "Error: Could not generate draft. Please check model path."

    # 6. Return the state update
    return {
        "draft": draft, 
        "reflection_count": 1 # Start at 1 for the first draft
    }  
    # CORRECTION: Using a simpler 'Pass/Fail' prompt for small model reliability.
    critic_prompt = (
        "Evaluate this summary. If it is generic or repeats 'the document' constantly, say 'REWRITE'. "
        "If it contains specific facts and is accurate, say 'NO_ERRORS_FOUND'.\n"
        f"Summary to check: {state['draft']}"
    )
    
    critique = engine.generate("Check summary quality", critic_prompt)
    return {"critique": critique}

# def node_refine_answer(state):
#     print(f"--- NODE: REFINER (FIXING ERRORS) - ITERATION {state.get('reflection_count')} ---")
    
#     current_count = state.get('reflection_count', 1)
    
#     persona_key = state.get('persona', 'executive').lower()
#     base_persona_instruction = PERSONAS.get(persona_key, "You are a professional assistant.")
#     dynamic_instruction = (
#         f"Role: {base_persona_instruction}\n"
#         "Task: Review the draft and the critique below. "
#         "Rewrite the summary to fix the identified issues while strictly maintaining your professional persona. "
#         "Output ONLY the revised text. No introductions like 'Here is the revised draft'."
#     )
    
#     # 3. Provide the Context
#     context_data = (
#         f"Current Draft: {state['draft']}\n"
#         f"Criticism to Address: {state['critique']}"
#     )
    

#     refined_draft = engine.generate(context_data, system_prompt)
    

#     for word in ["Task:", "Question:", "CRITICAL RULES:", "REWRITE"]:
#         if word in refined_draft:
#             refined_draft = refined_draft.replace(word, "").strip()

#     # Log the history
#     error_entry = [f"Iteration {current_count}: {state['critique'][:50]}..."]
    
#     return {
#         "draft": refined_draft, 
#         "errors": state.get("errors", []) + error_entry, 
#         "reflection_count": current_count + 1
#     }
# nodes.py

def node_refine_answer(state):
    print(f"--- NODE: REFINER (FIXING ERRORS) - ITERATION {state.get('reflection_count')} ---")
    current_count = state.get('reflection_count', 1)

    # 1. Fetch persona
    persona_key = state.get('persona', 'executive').lower()
    persona_instruction = PERSONAS.get(persona_key, "You are a professional assistant.")

    # 2. Define the prompt variable (MAKE SURE THIS NAME MATCHES BELOW)
    system_prompt = (
        f"Role: {persona_instruction}\n"
        "Task: Rewrite the draft to address the critique. Fix technical inaccuracies.\n"
        "STRICT RULES: Output ONLY the revised text. No meta-talk."
    )

    # 3. Prepare context
    context_data = f"DRAFT: {state['draft']}\nCRITIQUE: {state['critique']}"

    # 4. Generate - Using 'system_prompt' here because it was defined above
    refined_draft = engine.generate(context_data, system_prompt)

    # 5. Clean up and log
    refined_draft = refined_draft.replace("REWRITE", "").strip()
    error_log = state.get("errors", []) + [f"Iteration {current_count}: Refined based on critique"]

    return {
        "draft": refined_draft,
        "errors": error_log,
        "reflection_count": current_count + 1
    }

def node_finalize(state):
    print("--- NODE: FINALIZING & DEDUPLICATING ---")
    text = state.get("draft", "")
    
    # Split into sentences or lines
    lines = text.split('\n')
    seen = set()
    unique_lines = []
    
    for line in lines:
        clean_line = line.strip().lower()
        # Only add if the line isn't a duplicate
        if clean_line not in seen and len(clean_line) > 5:
            unique_lines.append(line)
            seen.add(clean_line)
            
    final_summary = "\n".join(unique_lines)
    return {"summary": final_summary}