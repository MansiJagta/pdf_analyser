# from llama_cpp import Llama
# import os

# class LLMEngine:
#     def __init__(self, model_path="models/assets/smollm2-360m-instruct-q8_0.gguf"):
#         if not os.path.exists(model_path):
#             raise FileNotFoundError(f"Model file not found at {model_path}")
#         self.llm = Llama(model_path=model_path, n_ctx=2048, verbose=False)

#     def generate_response(self, prompt, system_message):
#         full_prompt = f"<|im_start|>system\n{system_message}<|im_end|>\n<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"
#         output = self.llm(full_prompt, max_tokens=512, stop=["<|im_end|>"])
#         return output["choices"][0]["text"]








# from llama_cpp import Llama

# class LLMEngine:
#     def __init__(self, model_path: str):
#         # Optimized for CPU usage
#         self.llm = Llama(
#             model_path=model_path,
#             n_ctx=8192,
#             n_threads=4,
#             verbose=False
#         )

#     def generate(self, context: str, persona_prompt: str):
#         """Generates a summary based on the document and the selected persona."""
#         prompt = f"System: {persona_prompt}\nContext: {context}\nAI:"
#         response = self.llm(
#             prompt,
#             max_tokens=512,
#             stop=["User:", "\n"],
#             echo=False
#         )
#         return response["choices"][0]["text"]








from llama_cpp import Llama

class LLMEngine:
    def __init__(self, model_path: str):
        # Optimized for CPU usage
        self.llm = Llama(
            model_path=model_path,
            n_ctx=8192,
            n_threads=4,
            verbose=False
        )

    def generate(self, context: str, persona_prompt: str):
        """Generates a summary based on the document and the selected persona."""
        
        # 1. Use the ChatML format which SmolLM2 understands best
        # This prevents the model from getting confused by the 12k characters of text
        prompt = (
            f"<|im_start|>system\n{persona_prompt}<|im_end|>\n"
            f"<|im_start|>user\nDocument Content: {context[:6000]}\n\n"
            f"Please provide a summary based on your persona.<|im_end|>\n"
            f"<|im_start|>assistant\n"
        )

        response = self.llm(
            prompt,
            max_tokens=512,
            # 2. REMOVED "\n" from stop. 
            # We only want it to stop when it's actually finished (im_end).
            stop=["<|im_end|>", "User:"], 
            echo=False,
            temperature=0.7 # Added a bit of 'creativity' for better summaries
        )
        
        output = response["choices"][0]["text"].strip()
        
        # Debugging print to confirm it's working
        print(f"DEBUG: AI Response length: {len(output)} characters")
        
        return output