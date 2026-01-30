# # app/services/ai_service.py

# import os
# import uuid
# from app.ai.manager import app as ai_app


# def run_document_ai(file_path: str, persona: str):
#     """
#     Runs the AI pipeline on a document and returns the final AI state.
#     """

#     config = {
#         "configurable": {
#             "thread_id": f"doc_{uuid.uuid4().hex[:8]}"
#         }
#     }

#     inputs = {
#         "file_path": file_path,
#         "persona": persona,
#         "query": "Analyze this document and provide a summary based on the persona.",
#         "raw_text": "",
#         "layout_type": "",
#         "summary": "",
#         "vector_status": "",
#         "reflection_count": 0,
#         "draft": "",
#         "critique": ""
#     }

#     final_state = {}

#     for state in ai_app.stream(inputs, config=config, stream_mode="values"):
#         final_state = state

#     return final_state
