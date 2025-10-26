from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class PromptStructure(BaseModel):
    """Structured prompt model based on general prompt engineering best practices."""

    objective: str = Field(
        ...,
        description="Clear, specific instruction describing what the model should do.",
    )
    tone: Literal["formal", "informal", "friendly", "professional", "humorous", "serious"] = Field(
        default="professional",
        description="Desired tone of the response.",
    )
    refinement_notes: List[str] = Field(
        default_factory=list,
        description="History of iterative adjustments made to improve the prompt.",
    )

    def render(self) -> str:
        """Compose the prompt text that can be supplied to a language model."""
        segments: List[str] = [f"Objective: {self.objective}"]
        segments.append(f"Tone: {self.tone}")
        if self.refinement_notes:
            segments.append("Refinement Notes:")
            segments.extend(f"- {note}" for note in self.refinement_notes)
        return "\n".join(segments)
