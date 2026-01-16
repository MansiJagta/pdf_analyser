# from models import PDFParser, LLMEngine, PERSONA_PROMPTS
from pdf_parser import PDFParser
from llm import LLMEngine
from persona import PERSONA_PROMPTS
# 1. Parse
parser = PDFParser()
text = parser.extract_text("sample.pdf")

# 2. Summarize as Executive
llm = LLMEngine()
summary = llm.generate_response(text, PERSONA_PROMPTS["executive"])

print(f"Executive Summary:\n{summary}")