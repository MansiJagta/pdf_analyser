# # from models import PDFParser, LLMEngine, PERSONA_PROMPTS
# from pdf_parser import PDFParser
# from llm import LLMEngine
# from persona import PERSONA_PROMPTS
# # 1. Parse
# parser = PDFParser()
# text = parser.extract_text("sample.pdf")

# # 2. Summarize as Executive
# llm = LLMEngine()
# summary = llm.generate_response(text, PERSONA_PROMPTS["executive"])

# print(f"Executive Summary:\n{summary}")






# import asyncio
# from manager import run_agent

# async def debug_test():
#     print("🚀 Starting Offline Analysis Test...")
    
#     # Replace with a real path to a PDF in your folder
#     test_pdf = "sample_document.pdf" 
#     test_persona = "executive"

#     try:
#         # Run the agent and capture the result
#         result = run_agent(test_pdf, test_persona)
        
#         print("\n✅ ANALYSIS COMPLETE")
#         print("-" * 30)
#         print(f"📄 Layout Detected: {result.get('layout_type')}")
#         print(f"🧠 Vector Status: {result.get('vector_status')}")
#         print(f"📝 Summary:\n{result.get('summary')}")
#         print("-" * 30)

#     except Exception as e:
#         print(f"❌ TEST FAILED: {str(e)}")

# if __name__ == "__main__":
#     asyncio.run(debug_test())









# from manager import app
# import uuid

# def run_debug():
#     # Use a unique thread_id
#     config = {"configurable": {"thread_id": "test_session_123"}}
    
#     inputs = {
#         "file_path": "sample.pdf", # Ensure this file exists in your folder!
#         "persona": "executive",
#         "raw_text": "",
#         "layout_type": "",
#         "summary": "",
#         "vector_status": ""
#     }

#     print("🚀 Starting Debug Run...")
    
#     # CORRECTED LOOP: In 'values' mode, the event IS the state
#     for state in app.stream(inputs, config=config, stream_mode="values"):
#         print("\n--- State Update ---")
#         if state.get('raw_text'):
#             print(f"📝 Text Extracted: {len(state['raw_text'])} characters")
#         if state.get('layout_type'):
#             print(f"📄 Layout: {state['layout_type']}")
#         if state.get('summary'):
#             print(f"💡 Summary Ready!")
#         if state.get('vector_status'):
#             print(f"🗄️ Vector Status: {state['vector_status']}")
    
#     print("\n✅ Run Finished Successfully.")

# if __name__ == "__main__":
#     run_debug()









import os
import sys # For flushing the output

from manager import app
import uuid

def run_debug():
    # Use a unique thread_id
    config = {"configurable": {"thread_id": "test_session_123"}}
    
    # Ensure this matches your ACTUAL file name
    target_file = "sample.pdf" 
    
    inputs = {
        "file_path": target_file,
        "persona": "student",
        "raw_text": "",
        "layout_type": "",
        "summary": "",
        "vector_status": ""
    }

    display_name = os.path.basename(target_file).upper()
    print(f"🚀 Starting Debug Run for: {display_name}...", flush=True)
    
    final_state = {}

    # Iterate through the graph steps
    for state in app.stream(inputs, config=config, stream_mode="values"):
        final_state = state # Capture every update
        
        print("\n--- State Update ---", flush=True)
        
        if state.get('raw_text'):
            print(f"📝 Text Extracted: {len(state['raw_text'])} characters", flush=True)
        if state.get('layout_type'):
            print(f"📄 Layout: {state['layout_type']}", flush=True)
        if state.get('vector_status'):
            print(f"🗄️ Vector Status: {state['vector_status']}", flush=True)
        if state.get('summary'):
            print(f"💡 Summary Ready!", flush=True)

    # DYNAMIC PRINTING OF FINAL SUMMARY
    print("\n" + "="*60, flush=True)
    print(f"📋 FINAL AI SUMMARY FOR: {display_name}", flush=True)
    print("="*60, flush=True)
    
    # Access the final result from the captured state
    final_summary = final_state.get("summary")
    
    if final_summary:
        print(final_summary, flush=True)
    else:
        print(f"❌ Error: No summary content was found in the final graph state.", flush=True)
    
    print("="*60, flush=True)
    print(f"\n✅ {display_name} Run Finished Successfully.", flush=True)

if __name__ == "__main__":
    run_debug()