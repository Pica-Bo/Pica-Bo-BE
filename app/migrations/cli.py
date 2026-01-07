#!/usr/bin/env python3
"""CLI tool for managing database migrations.

Usage:
    python -m app.migrations.cli migrate    # Run all pending migrations
    python -m app.migrations.cli status     # Show migration status
"""

import asyncio
import sys
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings
from app.migrations.runner import MigrationRunner
from app.migrations.registry import MIGRATIONS


async def run_migrations():
    """Run all pending migrations."""
    client = AsyncIOMotorClient(settings.mongo_uri)
    runner = MigrationRunner(client)
    
    print("Running migrations...")
    await runner.run_migrations(MIGRATIONS)
    print("All migrations completed successfully.")


async def show_status():
    """Show which migrations have been applied."""
    client = AsyncIOMotorClient(settings.mongo_uri)
    runner = MigrationRunner(client)
    
    print("\nMigration Status:")
    print("-" * 60)
    
    for migration in MIGRATIONS:
        has_run = await runner.has_run(migration.name)
        status = "✓ Applied" if has_run else "✗ Pending"
        print(f"{status:12} | {migration.name}")
    
    print("-" * 60)


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m app.migrations.cli [migrate|status]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "migrate":
        asyncio.run(run_migrations())
    elif command == "status":
        asyncio.run(show_status())
    else:
        print(f"Unknown command: {command}")
        print("Available commands: migrate, status")
        sys.exit(1)


if __name__ == "__main__":
    main()
