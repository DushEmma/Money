"""
Migration: Expand image URL columns to VARCHAR(500)
====================================================
Cloudinary URLs are typically 200-350 characters long.
The original schema used VARCHAR(200) which truncates URLs,
causing broken images when fetching profiles.

Run this ONCE against your production database.
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

from app import app, db

def migrate_image_columns():
    """Alter profile_picture, id_photo, and screenshot_path columns to VARCHAR(500)."""
    with app.app_context():
        database_url = app.config.get('SQLALCHEMY_DATABASE_URI', '')
        is_postgres = 'postgresql' in database_url or 'postgres' in database_url
        is_sqlite = 'sqlite' in database_url

        conn = db.engine.connect()
        trans = conn.begin()

        try:
            if is_postgres:
                print("🐘 PostgreSQL detected — running ALTER COLUMN statements...")
                statements = [
                    "ALTER TABLE worker ALTER COLUMN profile_picture TYPE VARCHAR(500);",
                    "ALTER TABLE worker ALTER COLUMN id_photo TYPE VARCHAR(500);",
                    "ALTER TABLE employer ALTER COLUMN profile_picture TYPE VARCHAR(500);",
                    "ALTER TABLE payment ALTER COLUMN screenshot_path TYPE VARCHAR(500);",
                ]
                for stmt in statements:
                    print(f"  ▶ {stmt}")
                    conn.execute(db.text(stmt))
                trans.commit()
                print("✅ PostgreSQL columns successfully expanded to VARCHAR(500).")

            elif is_sqlite:
                print("🗂  SQLite detected.")
                print("   SQLite does not support ALTER COLUMN, but SQLite has no")
                print("   enforced VARCHAR length limits — long URLs are stored fine.")
                print("   No migration needed for SQLite.")
                print("✅ No changes required.")

            else:
                print(f"⚠️  Unknown database: {database_url[:40]}...")
                print("   Please manually run:")
                print("   ALTER TABLE worker ALTER COLUMN profile_picture VARCHAR(500);")
                print("   ALTER TABLE worker ALTER COLUMN id_photo VARCHAR(500);")
                print("   ALTER TABLE employer ALTER COLUMN profile_picture VARCHAR(500);")
                print("   ALTER TABLE payment ALTER COLUMN screenshot_path VARCHAR(500);")

        except Exception as e:
            trans.rollback()
            print(f"❌ Migration failed: {e}")
            sys.exit(1)
        finally:
            conn.close()

if __name__ == '__main__':
    migrate_image_columns()
