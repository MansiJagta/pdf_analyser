import os
import sys
from llama_cpp import Llama

# ==============================
# Robust Model Path Discovery
# ==============================
def find_model_path():
    """
    Locates the Llama-3.2 GGUF file by checking common directories.
    """
    # 1. Check relative to this file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Potential paths to check
    # We want to find: assets/Llama-3.2-3B-Instruct-Q4_K_M.gguf
    # It might be in document_backend/assets or document_backend/app/models/assets
    
    project_root = os.path.abspath(os.path.join(current_dir, "../../")) # document_backend/
    
    candidates = [
        os.path.join(project_root, "app", "models", "assets", "Llama-3.2-3B-Instruct-Q4_K_M.gguf"),
        os.path.join(project_root, "assets", "Llama-3.2-3B-Instruct-Q4_K_M.gguf"),
        os.path.join(current_dir, "assets", "Llama-3.2-3B-Instruct-Q4_K_M.gguf"),
        r"C:\Users\Jagta\OneDrive\Desktop\Alexa\pdf_analyser\document_backend\app\models\assets\Llama-3.2-3B-Instruct-Q4_K_M.gguf"
    ]
    
    for path in candidates:
        if os.path.exists(path):
            print(f"✅ Found model at: {path}")
            return path
            
    print("❌ Model file not found in common locations.")
    print(f"Checked: {candidates}")
    # Return the most likely one to let Llama raise the specific error if it fails
    return candidates[0]

MODEL_PATH = find_model_path()

class LLMEngine:
    def __init__(self, model_path=MODEL_PATH):
        print(f"--- 🚀 INITIALIZING AI ENGINE ---")
        print(f"Target Model: {model_path}")
        
        if not os.path.exists(model_path):
            print(f"⚠️ WARNING: Model file does not exist at {model_path}")
            # We don't raise here to allow the app to start, but AI will fail
        
        try:
            # --- 8GB RAM OPTIMIZED CONFIGURATION ---
            self.llm = Llama(
                model_path=model_path,
                n_ctx=2048,          # Reasonable context for 8GB RAM
                n_gpu_layers=-1,     # Offload to GPU if available
                n_threads=4,         # Good default for quad-core
                n_batch=128,         # Smaller batch size for lower memory usage
                verbose=False,
                offload_kqv=False    # Keep KV cache on CPU if GPU is small
            )
            print("✅ AI Engine initialized successfully.")
        except Exception as e:
            print(f"❌ Failed to initialize AI Engine: {e}")
            self.llm = None

    def generate(self, user_query, system_prompt, temperature=0.1):
        if not self.llm:
            return "AI Engine is not available. Please check server logs."
            
        # Llama-3.2 / ChatML Format
        # <|begin_of_text|> is often implicit or handled by the tokenizer, 
        # but strict formatting helps.
        prompt = (
            f"<|start_header_id|>system<|end_header_id|>\n\n"
            f"{system_prompt}<|eot_id|>"
            f"<|start_header_id|>user<|end_header_id|>\n\n"
            f"{user_query}<|eot_id|>"
            f"<|start_header_id|>assistant<|end_header_id|>\n\n"
        )
        
        try:
            response = self.llm(
                prompt,
                max_tokens=600,
                temperature=temperature,
                stop=["<|eot_id|>", "<|end_of_text|>"],
                echo=False
            )
            return response["choices"][0]["text"].strip()
        except Exception as e:
            print(f"❌ Generation Error: {e}")
            return "Error generating response."

# Singleton Instance
engine = LLMEngine()