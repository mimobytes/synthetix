import os
from typing import List, Optional
from pydantic import BaseModel, Field
from google import genai
from google.genai import types

class QuizQuestion(BaseModel):
    """Schema representing an individual conceptual assessment question."""
    question: str = Field(description="The question prompt testing deep understanding")
    options: List[str] = Field(description="Exactly four distinct multiple choice options")
    correct_answer: str = Field(description="The exact text of the single correct option")
    explanation: str = Field(description="Detailed academic rationale for why this option is correct")

class StudySection(BaseModel):
    """Schema for a dedicated topical deep-dive section."""
    heading: str = Field(description="Subtopic or thematic section title")
    content: str = Field(description="Exhaustive, detailed pedagogical explanation breaking down the concepts, mechanics, and trade-offs")
    bullet_points: List[str] = Field(description="Key formulas, sub-rules, or core technical facts for this section")

class TermDefinition(BaseModel):
    """Schema for key vocabulary, theorems, and definitions."""
    term: str = Field(description="Name of the theorem, algorithm, parameter, or term")
    definition: str = Field(description="Accurate and precise definition")

class StudyPayload(BaseModel):
    """Schema for full academic study dossier."""
    title: str = Field(description="Descriptive academic title for the topic")
    overview: str = Field(description="Comprehensive conceptual briefing and high-level synthesis")
    sections: List[StudySection] = Field(description="Thorough deep-dive sections covering every subtopic in depth")
    glossary: List[TermDefinition] = Field(description="Core definitions, parameters, and terminology glossary")
    high_yield_takeaways: List[str] = Field(description="High-yield facts, exam points, and pitfalls to remember")
    quiz: List[QuizQuestion] = Field(description="Set of 5 to 8 challenging multi-choice questions")

class GeminiService:
    """Orchestrates structured generative content requests using Gemini 2.5 Flash."""

    def __init__(self, api_key: Optional[str] = None):
        """Initializes the GenAI client with AI Studio credentials."""
        key = api_key or os.getenv("GEMINI_API_KEY")
        if not key:
            raise ValueError("GEMINI_API_KEY environment variable is missing.")
        self.client = genai.Client(api_key=key)
        self.model_name = "gemini-2.5-flash"

    def process_study_notes(self, text: str) -> dict:
        """Transforms raw notes into an exhaustive, multi-section academic study guide."""
        system_instruction = (
            "You are a distinguished university professor and master tutor. "
            "Your objective is to produce exhaustive, highly thorough study notes that capture "
            "every nuance, theorem, formula, edge case, and architectural detail from the source text. "
            "Do NOT summarize into brief snippets. Break the topic down into comprehensive modules, "
            "explain technical mechanisms step-by-step, define all specialized terminology, "
            "and craft rigorous assessment questions that test true conceptual comprehension."
        )

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=text,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.2,
                response_mime_type="application/json",
                response_schema=StudyPayload
            )
        )

        if response.parsed:
            return response.parsed.model_dump()

        import json
        return json.loads(response.text)