"""
Sehr einfacher Speicher fuer User Stories: eine Liste im Arbeitsspeicher.
"""

from typing import List, Optional
from .models import UserStory

_userstories: List[UserStory] = []


def add_story(story: UserStory) -> None:
    for index, vorhandene in enumerate(_userstories):
        if vorhandene.id == story.id:
            _userstories[index] = story
            return
    _userstories.append(story)


def add_stories(stories: List[UserStory]) -> None:
    for story in stories:
        add_story(story)


def get_all() -> List[UserStory]:
    return list(_userstories)


def get_by_id(story_id: str) -> Optional[UserStory]:
    for story in _userstories:
        if story.id == story_id:
            return story
    return None


def count() -> int:
    return len(_userstories)
