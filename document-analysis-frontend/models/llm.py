from llama_cpp import Llama
import os

class LLMEngine:
    def __init__(self, model_path="models/assets/smollm2-360m-instruct-q8_0.gguf"):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}")
        self.llm = Llama(model_path=model_path, n_ctx=2048, verbose=False)

    def generate_response(self, prompt, system_message):
        full_prompt = f"<|im_start|>system\n{system_message}<|im_end|>\n<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"
        output = self.llm(full_prompt, max_tokens=512, stop=["<|im_end|>"])
        return output["choices"][0]["text"]