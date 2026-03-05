import re
from typing import Optional, List
from sqlmodel import Field, Session, SQLModel, create_engine, select
from pathlib import Path
from app.core.logger import logger

# Setup SQLite Database for Topic Registry
BASE_DIR = Path(__file__).resolve().parent.parent.parent
REGISTRY_DB_PATH = BASE_DIR / "data" / "topic_registry" / "registry.db"
DATABASE_URL = f"sqlite:///{REGISTRY_DB_PATH}"

engine = create_engine(DATABASE_URL, echo=False)


class TopicRecord(SQLModel, table=True):
    """
    Topic Registry authoritative model (Section 5).
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    slug: str = Field(index=True, unique=True, description="Lowercase, snake_case canonical topic ID")
    display_name: str
    description: Optional[str] = None
    parent_slug: Optional[str] = None


def create_db_and_tables():
    """Idempotent database initialization."""
    SQLModel.metadata.create_all(engine)


class TopicRegistryService:
    """
    Enforces Topic Normalization and Authority.
    """
    
    @staticmethod
    def normalize_topic_name(topic_name: str) -> str:
        """
        Normalizes a topic name to lowercase and snake_case (Section 5).
        """
        # Convert to lowercase
        normalized = topic_name.lower().strip()
        # Replace spaces and non-alphanumeric chars with underscores
        normalized = re.sub(r'[^a-z0-9]+', '_', normalized)
        # Remove leading/trailing underscores
        normalized = normalized.strip('_')
        return normalized

    @staticmethod
    def get_topic(topic_slug: str) -> Optional[TopicRecord]:
        """Finds a canonical topic by slug."""
        normalized_slug = TopicRegistryService.normalize_topic_name(topic_slug)
        with Session(engine) as session:
            statement = select(TopicRecord).where(TopicRecord.slug == normalized_slug)
            return session.exec(statement).first()

    @staticmethod
    def add_topic(display_name: str, description: Optional[str] = None, parent_slug: Optional[str] = None) -> TopicRecord:
        """
        Adds a new canonical topic if it doesn't already exist.
        """
        slug = TopicRegistryService.normalize_topic_name(display_name)
        
        with Session(engine) as session:
            existing = TopicRegistryService.get_topic(slug)
            if existing:
                return existing
            
            new_topic = TopicRecord(
                slug=slug,
                display_name=display_name,
                description=description,
                parent_slug=parent_slug
            )
            session.add(new_topic)
            session.commit()
            session.refresh(new_topic)
            
            logger.info(f"Created new canonical topic: {slug}", extra={"stage": "Knowledge Integrity Check"})
            return new_topic

    @staticmethod
    def list_topics() -> List[TopicRecord]:
        with Session(engine) as session:
            return session.exec(select(TopicRecord)).all()

# Init on module load
create_db_and_tables()
