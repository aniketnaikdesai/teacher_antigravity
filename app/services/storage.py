import json
from pathlib import Path
from typing import Any, Dict, Optional

from app.models.schemas import ConversationStore, NoteGenerationOutput
from app.core.logger import logger

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"

class StorageService:
    """
    Handles immutable filesystem storage for conversations and notes.
    """
    
    @staticmethod
    def _get_conversation_path(conversation_id: str) -> Path:
        # conv_20260304_0001
        return DATA_DIR / "conversations" / f"{conversation_id}.json"

    @staticmethod
    def save_conversation(conversation: ConversationStore) -> Path:
        """
        Saves a conversation to the immutable data store (Section 12).
        Fails if the file already exists to preserve immutability.
        """
        filepath = StorageService._get_conversation_path(conversation.conversation_id)
        if filepath.exists():
            error_msg = f"Immutability violation: Conversation {conversation.conversation_id} already exists."
            logger.error(error_msg, extra={"stage": "Conversation Intake", "failure_class": "StorageError"})
            raise FileExistsError(error_msg)
            
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(conversation.model_dump_json(indent=2))
            
        logger.info(f"Saved conversation {conversation.conversation_id}", extra={"stage": "Conversation Intake"})
        return filepath

    @staticmethod
    def get_conversation(conversation_id: str) -> Optional[ConversationStore]:
        filepath = StorageService._get_conversation_path(conversation_id)
        if not filepath.exists():
            return None
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return ConversationStore(**data)

    @staticmethod
    def save_note(note: NoteGenerationOutput) -> Path:
        """
        Saves a note using the standardized Markdown template (Section 10).
        """
        filepath = DATA_DIR / "notes" / f"{note.note_id}.md"
        
        # We process body_markdown correctly so it is rendered seamlessly.
        # Check if the generated markdown already contains headings
        body = note.body_markdown.strip()

        # Build citations and risk flags
        citations_str = "\n".join([f"- {c}" for c in note.citations])
        risks_str = "\n".join([f"- {r}" for r in note.risk_flags])
        source_convs_str = ", ".join(note.source_conversation_ids)

        markdown_content = f"""# {note.title}

## Topic
{note.topic}

## Summary
{note.summary}

{body}

## Risk Considerations
{risks_str}

## Evidence / Citations
{citations_str}

## Metadata
- note_id: {note.note_id}
- version: {note.version}
- schema_version: {note.schema_version}
- created_at: {note.created_at.isoformat() + "Z"}
- source_conversation_ids: [{source_convs_str}]
"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(markdown_content)

        logger.info(f"Saved note {note.note_id}", extra={"stage": "Note Generation"})
        return filepath
