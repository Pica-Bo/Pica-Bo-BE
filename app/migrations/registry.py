"""Registry of all migrations to run.

Import all migration classes here and add them to MIGRATIONS list in order.
"""

from typing import List
from app.migrations import BaseMigration
from app.migrations.versions.m001_initial import CreateCollectionsAndIndexes
from app.migrations.versions.m002_reference_collections import CreateReferenceCollections

# Add new migrations to this list in order
MIGRATIONS: List[BaseMigration] = [
    CreateCollectionsAndIndexes(),
    CreateReferenceCollections(),
]
