import os
import llama_cpp
from llama_cpp import Llama

def find_model_path():
    """
    Locates the Llama-3.2 GGUF file.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, "../../"))
    
    candidates = [
        os.path.join(project_root, "app", "models", "assets", "Llama-3.2-3B-Instruct-Q4_K_M.gguf"),
        os.path.join(project_root, "assets", "Llama-3.2-3B-Instruct-Q4_K_M.gguf"),
        os.path.join(current_dir, "assets", "Llama-3.2-3B-Instruct-Q4_K_M.gguf"),
        r"C:\Users\Jagta\OneDrive\Desktop\Alexa\pdf_analyser\document_backend\app\models\assets\Llama-3.2-3B-Instruct-Q4_K_M.gguf"
    ]
    
    for path in candidates:
        if os.path.exists(path):
            print(f"Found model at: {path}")
            return path
            
    print("Model file not found in common locations.")
    return None

class LLMEngine:
    _instance = None

    def __new__(cls):
        """Singleton pattern to prevent RAM overflow from multiple loads."""
        if cls._instance is None:
            cls._instance = super(LLMEngine, cls).__new__(cls)
            cls._instance.llm = None
            cls._instance._initialize_model()
        return cls._instance

    def _initialize_model(self):
        """Loads the model with strict 8GB RAM optimizations."""
        model_path = find_model_path()
        if not model_path:
            return

        try:
            print(f"--- LOADING MEMORY-SAFE AI ENGINE ---")
            self.llm = Llama(
                model_path=model_path,
                n_ctx=1024,              # 📉 Fixed context to stay within 8GB RAM
                n_threads=2,             # 💻 Limit threads to stop 'ggml' fatal errors
                n_batch=128,             # 🚀 Smaller batches reduce CPU/RAM spikes
                use_mmap=False,          # ⚡ Faster allocation for Windows
                type_k=llama_cpp.GGML_TYPE_I8, 
                type_v=llama_cpp.GGML_TYPE_I8,
                last_n_tokens_size=64,
                verbose=False
            )
            print("--- AI ENGINE INITIALIZED SUCCESSFULLY ---")
        except Exception as e:
            print(f"--- CRITICAL AI LOAD FAILED: {e} ---")
            self.llm = None

    def _truncate_prompt(self, prompt, max_chars=3200):
        """
        Hard truncation to ensures prompt fits in 1024 context.
        Approx 4 chars per token -> 3200 chars ~= 800 tokens.
        Leaves ~200 tokens for generation.
        """
        if len(prompt) > max_chars:
            return prompt[:max_chars]
        return prompt

    def stream(self, user_query, system_prompt, temperature=0.1):
        """Yields tokens one by one. Limits output length to preserve RAM stability."""
        if not self.llm:
            yield "AI Engine is currently unavailable."
            return
            
        prompt = self._format_prompt(user_query, system_prompt)
        prompt = self._truncate_prompt(prompt)

        try:
            # We limit max_tokens to 256 to ensure generation stays within bounds
            for chunk in self.llm(
                prompt,
                max_tokens=256,          
                temperature=temperature,
                stop=["<|eot_id|>", "<|end_of_text|>"],
                stream=True 
            ):
                token = chunk["choices"][0]["text"]
                if token:
                    yield token
        except Exception as e:
            yield f"\n[Stream Error: {e}]"

    def generate(self, user_query, system_prompt, temperature=0.1):
        """Standard generation for summaries. Limits context to prevent crashes."""
        if not self.llm: return "AI Engine unavailable."
        
        prompt = self._format_prompt(user_query, system_prompt)
        prompt = self._truncate_prompt(prompt)

        try:
            response = self.llm(
                prompt,
                max_tokens=300,          # 📉 Conservative generation length
                temperature=temperature,
                stop=["<|eot_id|>", "<|end_of_text|>"]
            )
            return response["choices"][0]["text"].strip()
        except Exception as e:
            return f"Error: {e}"

    def _format_prompt(self, user_query, system_prompt):
        """Llama-3.2 strict formatting."""
        return (
            f"<|start_header_id|>system<|end_header_id|>\n\n"
            f"{system_prompt}<|eot_id|>"
            f"<|start_header_id|>user<|end_header_id|>\n\n"
            f"{user_query}<|eot_id|>"
            f"<|start_header_id|>assistant<|end_header_id|>\n\n"
        )

# Global singleton instance
engine = LLMEngine()