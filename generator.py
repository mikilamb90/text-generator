import os
import time
from google import genai
from dotenv import load_dotenv

load_dotenv()

def generate_ai_text(prompt: str, max_retries: int = 3, initial_delay: int = 2) -> str:
    """Sends a prompt to Gemini with detailed status printing for debugging."""
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "Error: GEMINI_API_KEY is missing. Check your .env file."

    client = genai.Client(api_key=api_key)
    delay = initial_delay

    for attempt in range(max_retries):
        try:
            print(f"[Attempt {attempt + 1}] Connecting to Gemini...")
            
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt,
            )
            
            # Check if text was successfully generated
            if response and hasattr(response, 'text') and response.text:
                return response.text
            else:
                return "Warning: The API responded, but no text was returned. The prompt might have triggered safety filters."
            
        except Exception as e:
            print(f"[Debug] Error caught on attempt {attempt + 1}: {e}")
            if attempt == max_retries - 1:
                return f"Sorry, an error occurred: {e}"
            
            time.sleep(delay)
            delay *= 2

def main():
    print("=== Local Gemini AI Text Generator (Debug Mode) ===")
    print("Type 'exit' or 'quit' to stop.\n")
    
    while True:
        user_prompt = input("Enter your prompt: ").strip()
        
        if user_prompt.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
            
        if not user_prompt:
            print("Prompt cannot be empty. Please try again.\n")
            continue
            
        print("\nGenerating response...\n")
        
        result = generate_ai_text(user_prompt)
        
        print("--- Response ---")
        print(result)
        print("-" * 40 + "\n")

if __name__ == "__main__":
    main()