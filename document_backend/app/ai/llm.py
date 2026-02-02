# from llama_cpp import Llama

# class LLMEngine:
#     def __init__(self, model_path="assets/Llama-3.2-3B-Instruct-Q4_K_M.gguf"):
#         # Llama-3.2 3B requires a larger context window (n_ctx) for PDFs
#         # We point directly to the new Llama-3.2 file path
#         engine = LLMEngine(model_path="assets/Llama-3.2-3B-Instruct-Q4_K_M.gguf")
#         self.llm = Llama(
#             model_path=model_path,
#             n_ctx=8192,         # Supports up to 128k, but 8k is safe for 8GB RAM
#             n_gpu_layers=-1,    # Set to -1 to offload to GPU if available
#             verbose=False
#         )

#     # def generate(self, user_query, system_prompt):
#     #     # Llama-3.2 uses special header IDs for roles (ChatML-like format)
#     #     prompt = (
#     #         f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n"
#     #         f"{system_prompt}<|eot_id|>"
#     #         f"<|start_header_id|>user<|end_header_id|>\n\n"
#     #         f"{user_query}<|eot_id|>"
#     #         f"<|start_header_id|>assistant<|end_header_id|>\n\n"
#     #     )
        
#     #     response = self.llm(
#     #         prompt,
#     #         max_tokens=512,
#     #         # CRITICAL: These prevent the "20 times a day" repetition loops
#     #         repeat_penalty=1.2,
#     #         temperature=0.1,    # Keep it factual for a CTO
#     #         # Stop tokens specific to Llama-3.2 family
#     #         stop=["<|eot_id|>", "<|end_of_text|>", "Task:", "Constraint:"]
#     #     )
#     #     return response["choices"][0]["text"].strip()
    
#     def generate(self, user_query, system_prompt, temperature=0.1):

#      prompt = (
#         # f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n"
#         f"{system_prompt}<|eot_id|>"
#         f"<|start_header_id|>user<|end_header_id|>\n\n"
#         f"{user_query}<|eot_id|>"
#         f"<|start_header_id|>assistant<|end_header_id|>\n\n"
#      )
    
#      response = self.llm(
#         prompt,
#         max_tokens=512,
#         repeat_penalty=1.2,
#         temperature=temperature, # Now dynamic based on the persona
#         stop=["<|eot_id|>", "<|end_of_text|>", "Task:", "Constraint:"]
#      )
#      return response["choices"][0]["text"].strip()





# from llama_cpp import Llama

# class LLMEngine:
#     def __init__(self, model_path="assets/Llama-3.2-3B-Instruct-Q4_K_M.gguf"):
#         # REMOVED: engine = LLMEngine(...) <--- This was the cause of the recursion error
        
#         print(f"--- Initializing Llama-3.2-3B: {model_path} ---")
#         self.llm = Llama(
#             model_path=model_path,
#             n_ctx=8192,         # 8k is perfect for 8GB RAM constraints
#             n_gpu_layers=-1,    # Offload to GPU
#             verbose=False,
#             cache=True,         # Added caching for speed
#             n_batch=512         # Added batching for faster prompt ingestion
#         )

#     def generate(self, user_query, system_prompt, temperature=0.1):
#         # Llama-3.2 formatting
#         prompt = (
#             f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n"
#             f"{system_prompt}<|eot_id|>"
#             f"<|start_header_id|>user<|end_header_id|>\n\n"
#             f"{user_query}<|eot_id|>"
#             f"<|start_header_id|>assistant<|end_header_id|>\n\n"
#         )
        
#         response = self.llm(
#             prompt,
#             max_tokens=512,
#             repeat_penalty=1.2,
#             temperature=temperature,
#             stop=["<|eot_id|>", "<|end_of_text|>", "Task:", "Constraint:"]
#         )
#         return response["choices"][0]["text"].strip()

# # --- CRITICAL: SINGLETON INSTANCE ---
# # This creates the engine ONLY ONCE when the file is imported.
# MODEL_PATH = "assets/Llama-3.2-3B-Instruct-Q4_K_M.gguf"
# engine = LLMEngine(model_path=MODEL_PATH)





# import os
# from llama_cpp import Llama

# # --- DYNAMIC PATH CALCULATION ---
# # This looks up from app/ai/llm.py to find the assets folder in document_backend/
# current_file_path = os.path.abspath(__file__)
# ai_dir = os.path.dirname(current_file_path)         # app/ai/
# app_dir = os.path.dirname(ai_dir)                  # app/
# #project_root = os.path.dirname(app_dir)  
# project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))           # document_backend/

# # Construct the absolute path to the model file
# #MODEL_PATH = os.path.join(project_root, "assets", "Llama-3.2-3B-Instruct-Q4_K_M.gguf")
# MODEL_PATH = r"C:\Users\Jagta\OneDrive\Desktop\Alexa\pdf_analyser\document_backend\assets\Llama-3.2-3B-Instruct-Q4_K_M.gguf"
# class LLMEngine:
#     def __init__(self, model_path=MODEL_PATH):
#         # Verify the file actually exists before trying to load it
#         if not os.path.exists(model_path):
#             print(f"❌ ERROR: Model file not found at: {model_path}")
#             print(f"Current working directory is: {os.getcwd()}")
#             raise FileNotFoundError(f"Model path does not exist: {model_path}")
            
#         print(f"--- Initializing Llama-3.2-3B: {model_path} ---")
#         self.llm = Llama(
#             model_path=model_path,
#             n_ctx=8192,         # 8k is perfect for 8GB RAM constraints
#             n_gpu_layers=-1,    # Offload to GPU
#             verbose=False,
#             cache=True,         # Added caching for speed
#             n_batch=512         # Added batching for faster prompt ingestion
#         )

#     def generate(self, user_query, system_prompt, temperature=0.1):
#         # Llama-3.2 formatting
#         prompt = (
#             f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n"
#             f"{system_prompt}<|eot_id|>"
#             f"<|start_header_id|>user<|end_header_id|>\n\n"
#             f"{user_query}<|eot_id|>"
#             f"<|start_header_id|>assistant<|end_header_id|>\n\n"
#         )
        
#         response = self.llm(
#             prompt,
#             max_tokens=512,
#             repeat_penalty=1.2,
#             temperature=temperature,
#             stop=["<|eot_id|>", "<|end_of_text|>", "Task:", "Constraint:"]
#         )
#         return response["choices"][0]["text"].strip()

# # --- CRITICAL: SINGLETON INSTANCE ---
# # This creates the engine ONLY ONCE when the file is imported.
# engine = LLMEngine(model_path=MODEL_PATH)









# import os
# from llama_cpp import Llama

# # --- ROBUST PATH CALCULATION ---
# # This calculates the path relative to the project root
# current_file_path = os.path.abspath(__file__)
# project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))

# # Base file name we expect
# EXPECTED_FILENAME = "Llama-3.2-3B-Instruct-Q4_K_M.gguf"
# ASSETS_DIR = os.path.join(project_root, "assets")
# MODEL_PATH = os.path.join(ASSETS_DIR, EXPECTED_FILENAME)

# class LLMEngine:
#     def __init__(self, model_path=MODEL_PATH):
#         # 1. Check if the assets folder exists at all
#         if not os.path.exists(ASSETS_DIR):
#             print(f"❌ ERROR: 'assets' folder not found at: {ASSETS_DIR}")
#             print("Please create the 'assets' folder in your project root.")
#             raise FileNotFoundError(f"Missing directory: {ASSETS_DIR}")

#         # 2. AUTO-RECOVERY: If the exact file is missing, look for hidden extensions
#         if not os.path.exists(model_path):
#             print(f"🔍 Searching for model in {ASSETS_DIR}...")
#             files = os.listdir(ASSETS_DIR)
            
#             # Find any file that looks like our Llama model
#             found_file = next((f for f in files if f.startswith("Llama-3.2-3B") and f.endswith(".gguf")), None)
            
#             if found_file:
#                 print(f"✅ Found model with different name: {found_file}")
#                 model_path = os.path.join(ASSETS_DIR, found_file)
#             else:
#                 print(f"❌ ERROR: Model not found at: {model_path}")
#                 print(f"Files currently in assets: {files}")
#                 print("💡 TIP: If you see the file in Explorer but not here, right-click it and select 'Always keep on this device' (OneDrive).")
#                 raise FileNotFoundError(f"Model file missing from assets.")
            
#         print(f"--- Initializing Llama-3.2-3B: {model_path} ---")
#         try:
#             self.llm = Llama(
#                 model_path=model_path,
#                 n_ctx=8192,         # 8k context for 8GB RAM
#                 n_gpu_layers=-1,    # Offload to GPU if available
#                 verbose=False,
#                 cache=True,
#                 n_batch=512
#             )
#         except Exception as e:
#             print(f"❌ FAILED TO LOAD MODEL: {e}")
#             raise

#     def generate(self, user_query, system_prompt, temperature=0.1):
#         prompt = (
#             f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n"
#             f"{system_prompt}<|eot_id|>"
#             f"<|start_header_id|>user<|end_header_id|>\n\n"
#             f"{user_query}<|eot_id|>"
#             f"<|start_header_id|>assistant<|end_header_id|>\n\n"
#         )
        
#         response = self.llm(
#             prompt,
#             max_tokens=512,
#             repeat_penalty=1.2,
#             temperature=temperature,
#             stop=["<|eot_id|>", "<|end_of_text|>", "Task:", "Constraint:"]
#         )
#         return response["choices"][0]["text"].strip()

# # --- SINGLETON INSTANCE ---
# engine = LLMEngine(model_path=MODEL_PATH)








# import os
# from llama_cpp import Llama

# # --- MATCHING YOUR FOLDER STRUCTURE ---
# # Based on your image: document_backend > models > assets > Llama...
# current_file_path = os.path.abspath(__file__)
# project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))

# # Updated path to include the 'models' folder seen in your sidebar
# MODEL_PATH = os.path.join(project_root, "models", "assets", "Llama-3.2-3B-Instruct-Q4_K_M.gguf")

# class LLMEngine:
#     def __init__(self, model_path=MODEL_PATH):
#         print(f"--- 🔍 LOADING FROM: {model_path} ---")
        
#         if not os.path.exists(model_path):
#             # Troubleshooting print to see what Python sees
#             actual_assets_path = os.path.join(project_root, "models", "assets")
#             if os.path.exists(actual_assets_path):
#                 print(f"✅ 'models/assets' folder found. Contents: {os.listdir(actual_assets_path)}")
#             else:
#                 print(f"❌ Folder NOT found at: {actual_assets_path}")
#             raise FileNotFoundError(f"Check your sidebar! File missing at: {model_path}")

#         # --- 8GB RAM CONSTRAINED SETTINGS ---
#         self.llm = Llama(
#             model_path=model_path,
#             n_ctx=4096,         # Reduced to 4k to fit comfortably in 8GB RAM
#             n_gpu_layers=-1,    # Offload to GPU if your laptop has one
#             n_batch=512,
#             verbose=False
#         )

#     def generate(self, user_query, system_prompt, temperature=0.1):
#         prompt = (
#             f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n"
#             f"{system_prompt}<|eot_id|>"
#             f"<|start_header_id|>user<|end_header_id|>\n\n"
#             f"{user_query}<|eot_id|>"
#             f"<|start_header_id|>assistant<|end_header_id|>\n\n"
#         )
        
#         response = self.llm(
#             prompt,
#             max_tokens=512,
#             temperature=temperature,
#             stop=["<|eot_id|>", "<|end_of_text|>"]
#         )
#         return response["choices"][0]["text"].strip()

# # Singleton instance
# engine = LLMEngine(model_path=MODEL_PATH)





# import os
# from llama_cpp import Llama

# def find_model_path():
#     # Get the project root (document_backend)
#     current_file = os.path.abspath(__file__)
#     root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
    
#     # Aggressively walk through every folder to find the .gguf file
#     for dirpath, dirnames, filenames in os.walk(root):
#         for f in filenames:
#             if f.startswith("Llama-3.2-3B") and f.endswith(".gguf"):
#                 return os.path.join(dirpath, f)
#     return None

# MODEL_PATH = find_model_path()

# class LLMEngine:
#     def __init__(self, model_path=MODEL_PATH):
#         if not model_path:
#             # If walk failed, try a direct hardcoded fallback to the exact folder
#             model_path = r"C:\Users\Jagta\OneDrive\Desktop\Alexa\pdf_analyser\document_backend\models\assets\Llama-3.2-3B-Instruct-Q4_K_M.gguf"
            
#         print(f"--- 🔍 ENGINE ATTEMPTING LOAD: {model_path} ---")
        
#         if not os.path.exists(model_path):
#             print(f"❌ STILL NOT FOUND. Please check if OneDrive has a 'cloud' icon on the assets folder.")
#             raise FileNotFoundError(f"Model file not found anywhere in project.")

#         # --- 8GB RAM OPTIMIZATION ---
#         self.llm = Llama(
#             model_path=model_path,
#             n_ctx=4096,         # Reduced context to save RAM
#             n_gpu_layers=-1,    # Offload to GPU if available
#             n_threads=4,        # Standard for quad-core CPUs
#             verbose=False
#         )

#     def generate(self, user_query, system_prompt, temperature=0.1):
#         prompt = (
#             f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n"
#             f"{system_prompt}<|eot_id|>"
#             f"<|start_header_id|>user<|end_header_id|>\n\n"
#             f"{user_query}<|eot_id|>"
#             f"<|start_header_id|>assistant<|end_header_id|>\n\n"
#         )
        
#         response = self.llm(
#             prompt,
#             max_tokens=512,
#             temperature=temperature,
#             stop=["<|eot_id|>", "<|end_of_text|>"]
#         )
#         return response["choices"][0]["text"].strip()

# # Initialize the shared engine
# engine = LLMEngine(model_path=MODEL_PATH)










# import os
# from llama_cpp import Llama

# # --- DYNAMIC PROJECT PATHING ---
# # We go up 3 levels from: document_backend/app/ai/llm.py -> document_backend/
# current_file = os.path.abspath(__file__)
# project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))

# # Your new path: backend > models > assets
# MODEL_PATH = os.path.join(project_root, "models", "assets", "Llama-3.2-3B-Instruct-Q4_K_M.gguf")

# class LLMEngine:
#     def __init__(self, model_path=MODEL_PATH):
#         print(f"--- 🔍 SEARCHING AT: {model_path} ---")
        
#         # Check if the file is physically there
#         if not os.path.exists(model_path):
#             # If the specific path fails, scan the whole backend for any .gguf file
#             print("⚠️ Path not found, scanning project folders...")
#             for root, dirs, files in os.walk(project_root):
#                 for file in files:
#                     if file.endswith(".gguf"):
#                         model_path = os.path.join(root, file)
#                         print(f"✅ Auto-located model at: {model_path}")
#                         break
#                 if model_path: break

#         if not model_path or not os.path.exists(model_path):
#             raise FileNotFoundError(f"❌ Could not find model. Please ensure it finished moving to: {MODEL_PATH}")

#         # --- 8GB RAM CONSTRAINTS ---
#         # Llama-3.2-3B is ~2GB. We limit context to keep total usage under 4GB.
#         self.llm = Llama(
#             model_path=model_path,
#             n_ctx=4096,         # Reduced context to save RAM
#             n_threads=4,        # Optimized for standard laptop CPUs
#             n_gpu_layers=-1,    # Uses GPU if available
#             verbose=False
#         )

#     def generate(self, user_query, system_prompt, temperature=0.1):
#         prompt = (
#             f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n"
#             f"{system_prompt}<|eot_id|>"
#             f"<|start_header_id|>user<|end_header_id|>\n\n"
#             f"{user_query}<|eot_id|>"
#             f"<|start_header_id|>assistant<|end_header_id|>\n\n"
#         )
        
#         response = self.llm(
#             prompt,
#             max_tokens=512,
#             temperature=temperature,
#             stop=["<|eot_id|>", "<|end_of_text|>"]
#         )
#         return response["choices"][0]["text"].strip()

# # Initialize the shared engine
# engine = LLMEngine(model_path=MODEL_PATH)









import os
from llama_cpp import Llama

# --- THE EXACT PATH FROM YOUR TERMINAL ---
# We use a raw string (r"...") to handle Windows backslashes correctly
#MODEL_PATH = r"C:\Users\Jagta\OneDrive\Desktop\Alexa\pdf_analyser\document_backend\app\models\assets\Llama-3.2-3B-Instruct-Q4_K_M.gguf"
MODEL_PATH = r"C:\Users\Jagta\OneDrive\Desktop\Alexa\pdf_analyser\document_backend\app\models\assets\Llama-3.2-3B-Instruct-Q4_K_M.gguf"



class LLMEngine:
    def __init__(self, model_path=MODEL_PATH):
        print(f"--- 🚀 TARGETING MODEL AT: {model_path} ---")
        
        # Check if OneDrive has the file ready
        if not os.path.exists(model_path):
            print("❌ ERROR: Path is correct, but the file is not accessible.")
            print("💡 ACTION: Right-click the file in File Explorer and select 'Always keep on this device'.")
            raise FileNotFoundError(f"OneDrive Link not resolved: {model_path}")

        # --- 8GB RAM OPTIMIZED INITIALIZATION ---
        # Llama-3.2-3B is ~2.02GB (as seen in your 'Length' output)
        self.llm = Llama(
            model_path=model_path,
            n_ctx=1024,         # Context size for 8GB RAM
            n_gpu_layers=-1,    # Auto-detect GPU
            n_threads=4,        # Optimal for most CPUs
            verbose=False
            n_batch=128,     # Smaller batches for 8GB RAM
            offload_kqv=False
        )

    def generate(self, user_query, system_prompt, temperature=0.1):
        prompt = (
            f"<|start_header_id|>system<|end_header_id|>\n\n"
        f"{system_prompt}<|eot_id|>"
        f"<|start_header_id|>user<|end_header_id|>\n\n"
        f"{user_query}<|eot_id|>"
        f"<|start_header_id|>assistant<|end_header_id|>\n\n"
        )
        
        response = self.llm(
            prompt,
            max_tokens=512,
            temperature=temperature,
            stop=["<|eot_id|>", "<|end_of_text|>"]
        )
        return response["choices"][0]["text"].strip()

# Initialize the shared engine
engine = LLMEngine(model_path=MODEL_PATH)