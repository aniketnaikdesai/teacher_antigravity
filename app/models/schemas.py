from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


# --- Conversation Storage Schemas (Section 12) ---

class Message(BaseModel):
    id: str = Field(..., description="Unique ID for the message (e.g., msg1)")
    role: str = Field(..., description="Role of the participant (user, assistant)")
    timestamp: datetime = Field(..., description="ISO-8601 UTC timestamp")
    content: str = Field(..., description="Message content")

class ConversationStore(BaseModel):
    conversation_id: str = Field(..., description="e.g., conv_20260304_0001")
    created_at: datetime = Field(..., description="ISO-8601 UTC timestamp")
    participants: List[str] = Field(..., description="Participants in the conversation")
    messages: List[Message] = Field(..., description="List of messages")


# --- Output Validation Schemas (Section 9) ---

class SchemaVersionBase(BaseModel):
    schema_version: str = Field("1.0", description="Strictly required version tag for structured outputs")

class TopicClassificationOutput(SchemaVersionBase):
    """Schema for Stage 2: Topic Classification (Section 9.1)"""
    conversation_id: str
    primary_topic: str
    secondary_topics: List[str] = Field(default_factory=list)
    confidence: float = Field(..., ge=0.0, le=1.0)
    is_new_topic_candidate: bool
    reasoning_brief: str

class NoteGenerationOutput(SchemaVersionBase):
    """Schema for Stage 4: Note Generation (Section 9.2)"""
    note_id: str
    topic: str
    title: str
    summary: str
    body_markdown: str
    citations: List[str]
    risk_flags: List[str]
    version: str
    source_conversation_ids: List[str]
    created_at: datetime


# --- pedagogical schema (Section 32) ---

class TeachingOutput(SchemaVersionBase):
    """Schema for teaching-mode outputs (Section 32)"""
    learning_objective: str
    prerequisites: List[str]
    concept_explanation: str
    worked_example: str
    common_mistakes: List[str]
    checkpoint_questions: List[str] = Field(..., min_length=2)
    recap: str
    next_step: str
