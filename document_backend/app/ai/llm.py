from langchain_ollama import ChatOllama
import logging

class LLMEngine:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LLMEngine, cls).__new__(cls)
            # Defer initialization to allow lifespan to start the engine first
            cls._instance.llm = None
        return cls._instance

    def initialize(self, model_name: str = "gemma3:4b"):
        """Called explicitly after the engine process is confirmed running."""
        print(f"--- INITIALIZING OLLAMA ENGINE (STRICT CONSTRAINTS) ---")
        try:
            self.llm = ChatOllama(
                model=model_name,
                temperature=0.1,
                num_ctx=1024,
                num_thread=2,
                num_predict=400,
                keep_alive="5m"
            )
            print("--- OLLAMA ENGINE CONNECTED ---")
        except Exception as e:
            print(f"--- OLLAMA CONNECTION FAILED: {e} ---")
            self.llm = None

    def stream(self, user_query: str, system_prompt: str, model_name: str = "gemma3:4b"):
        """Yields tokens from Ollama with dynamic model support."""
        
        # 1. Logic to handle model switching or initialization
        if not self.llm or (hasattr(self.llm, 'model') and self.llm.model != model_name):
            print(f"🔄 Switching/Initializing AI model to: {model_name}")
            # We pass the model_name to the initialize method
            self.initialize(model_name=model_name)
            
            if not self.llm:
                yield "AI Engine is currently unavailable. Ensure Ollama is running."
                return

        # 2. Prepare messages for ChatModel
        messages = [
            ("system", system_prompt),
            ("human", user_query)
        ]

        # 3. Stream tokens
        try:
            # Note: We use self.llm which is now set to the correct model_name
            for chunk in self.llm.stream(messages):
                if chunk.content:
                    yield chunk.content
        except Exception as e:
            # Improved error logging to catch path or model mismatches
            print(f"❌ Stream Error details: {str(e)}")
            yield f"\n[Stream Error: {e}]"

    def generate(self, user_query, system_prompt, temperature=0.1):
        """Generates a complete response."""
        if not self.llm: 
            self.initialize()
            if not self.llm: return "AI Engine unavailable."

        messages = [
            ("system", system_prompt),
            ("human", user_query)
        ]

        try:
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            return f"Error: {e}"

# Global singleton instance
engine = LLMEngine()