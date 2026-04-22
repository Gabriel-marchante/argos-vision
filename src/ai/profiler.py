import os
import json
from openai import OpenAI
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

class Profiler:
    def __init__(self, provider="openai"):
        self.provider = provider
        if provider == "openai":
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        elif provider == "anthropic":
            self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        else:
            raise ValueError(f"Unsupported AI provider: {provider}")

    def extract_information(self, transcript, current_profile=None):
        """Extract facts and interests from a transcript using an LLM."""
        prompt = f"""
        Extract key information about the person in the following transcript. 
        Focus on:
        - Name (if mentioned)
        - Interests and hobbies
        - Relationships (friends, family mentioned)
        - Context (work, location, plans)
        - Personal data (age, occupation, etc. if mentioned)

        Current known profile: {json.dumps(current_profile) if current_profile else "None"}

        Transcript: "{transcript}"

        Return the updated information in a structured JSON format. 
        Only return the JSON.
        """

        if self.provider == "openai":
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        
        elif self.provider == "anthropic":
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )
            # Find JSON in response
            content = response.content[0].text
            start = content.find('{')
            end = content.rfind('}') + 1
            return json.loads(content[start:end])
