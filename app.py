from dotenv import load_dotenv
import os
load_dotenv()

from deepagents import create_deep_agent
from pypdf import PdfReader

# 1. READ THE PDF LOCAL FIRST
pdf_filename = "FF2023-28-Phil-Demographic-Profile.pdf"
pdf_text = ""

print("📖 Reading the PDF file locally...")
try:
    reader = PdfReader(pdf_filename)
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pdf_text += text + "\n"
    
    print(f"✅ Successfully read {len(pdf_text)} characters from the document.")
except Exception as e:
    print(f"❌ Error reading file: {e}")

# 2. CREATE A SIMPLE AGENT (NO TOOLS NEEDED)
agent = create_deep_agent(
    model="google_genai:gemini-2.5-flash",
    system_prompt="You are a precise data analyst. Answer the user's question using ONLY the provided document text context.",
)

# 3. BUILD THE SINGLE-SHOT INJECTION PROMPT
user_question = "What is the population of the Philippines according to the document?"

full_prompt = f"""
Below is the complete text extracted from the demographic profile document:
-----------------------------------------------------------------
{pdf_text}
-----------------------------------------------------------------

Based strictly on the text provided above, please answer this question: {user_question}
"""

print("🚀 Sending the text context and your question to Gemini in a single hop...")

# 4. EXECUTE THE INVOCATION
result = agent.invoke(
    {"messages": [{"role": "user", "content": full_prompt}]}
)

# 5. PRINT THE CLEAN RESPONSE DIRECTLY
final_message = result['messages'][-1]
print("\n🤖 Final Agent Response:")
print(final_message.content)