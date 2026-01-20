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









# Import the tools directly
from pdf_parser import extract_pdf_logic
from embeddings import index_vector_logic
from llm import LLMEngine
from persona import PERSONAS

def node_extract_layout(state):
    print("--- NODE: EXTRACTING TEXT & LAYOUT ---")
    
    # Call the standalone tool via .invoke()
    # We no longer need an 'instance' or 'self'
    tool_result = extract_pdf_logic.invoke({"file_path": state['file_path']})
    
    return {
        "raw_text": tool_result["content"], 
        "layout_type": "scanned" if tool_result["is_scanned"] else "digital"
    }

def node_index_vectors(state):
    print("--- NODE: INDEXING TO SQLITE-VEC ---")
    
    # Call the vector tool via .invoke()
    index_vector_logic.invoke({"text": state['raw_text']})
    
    return {"vector_status": "completed"}

def node_summarize(state):
    """Generates a summary based on the chosen persona."""
    print(f"--- NODE: SUMMARIZING AS {state['persona']} ---")
    engine = LLMEngine(model_path="assets/smollm2.gguf")
    prompt = PERSONAS.get(state['persona'].lower(), PERSONAS['executive'])
    summary = engine.generate(state['raw_text'], prompt)
    print(f"DEBUG: AI generated {len(summary)} characters.")
    return {"summary": summary}