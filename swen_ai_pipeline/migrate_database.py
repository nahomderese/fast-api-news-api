#!/usr/bin/env python3
"""
Database migration script to add source_url and published_date columns.
Run this script to update your existing database schema.
"""

import asyncio
import os
from sqlalchemy import text
from swen_ai_pipeline.db.database import database
from swen_ai_pipeline.core.config import settings

async def run_migration():
    """Run the database migration to add missing columns."""
    
    print("🔄 Starting Database Migration...")
    print("=" * 50)
    
    # Check if database URL is configured
    if not settings.database_url:
        print("❌ No database URL configured. Please set DATABASE_URL environment variable.")
        return False
    
    print(f"📊 Database URL: {settings.database_url}")
    
    try:
        # Initialize database connection
        database.init(settings.database_url)
        
        async with database.session() as session:
            # Check if columns already exist
            print("\n🔍 Checking existing columns...")
            
            check_columns_query = text("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns 
                WHERE table_name = 'news_articles' 
                AND column_name IN ('source_url', 'published_date')
                ORDER BY column_name;
            """)
            
            result = await session.execute(check_columns_query)
            existing_columns = {row[0]: row for row in result.fetchall()}
            
            print(f"   Existing columns: {list(existing_columns.keys())}")
            
            # Add source_url column if it doesn't exist
            if 'source_url' not in existing_columns:
                print("\n➕ Adding source_url column...")
                await session.execute(text("""
                    ALTER TABLE news_articles 
                    ADD COLUMN source_url VARCHAR(1000) NOT NULL DEFAULT 'https://example.com';
                """))
                print("   ✅ source_url column added")
            else:
                print("   ✅ source_url column already exists")
            
            # Add published_date column if it doesn't exist
            if 'published_date' not in existing_columns:
                print("\n➕ Adding published_date column...")
                await session.execute(text("""
                    ALTER TABLE news_articles 
                    ADD COLUMN published_date VARCHAR(50);
                """))
                print("   ✅ published_date column added")
            else:
                print("   ✅ published_date column already exists")
            
            # Make author column nullable if it isn't already
            print("\n🔧 Checking author column...")
            author_check_query = text("""
                SELECT is_nullable 
                FROM information_schema.columns 
                WHERE table_name = 'news_articles' 
                AND column_name = 'author';
            """)
            
            result = await session.execute(author_check_query)
            author_nullable = result.scalar()
            
            if author_nullable == 'NO':
                print("   Making author column nullable...")
                await session.execute(text("""
                    ALTER TABLE news_articles 
                    ALTER COLUMN author DROP NOT NULL;
                """))
                print("   ✅ author column made nullable")
            else:
                print("   ✅ author column already nullable")
            
            # Update existing records with proper source_url values
            print("\n🔄 Updating existing records...")
            update_query = text("""
                UPDATE news_articles 
                SET source_url = 'https://example.com/legacy-article-' || id::text
                WHERE source_url = 'https://example.com';
            """)
            
            result = await session.execute(update_query)
            updated_count = result.rowcount
            print(f"   ✅ Updated {updated_count} existing records")
            
            # Remove default constraint from source_url
            print("\n🔧 Removing default constraint...")
            await session.execute(text("""
                ALTER TABLE news_articles 
                ALTER COLUMN source_url DROP DEFAULT;
            """))
            print("   ✅ Default constraint removed")
            
            # Add index on source_url for better performance
            print("\n📊 Adding index on source_url...")
            await session.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_news_articles_source_url 
                ON news_articles(source_url);
            """))
            print("   ✅ Index added")
            
            # Commit all changes
            await session.commit()
            
            # Verify the changes
            print("\n✅ Verifying migration...")
            verify_query = text("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns 
                WHERE table_name = 'news_articles' 
                AND column_name IN ('source_url', 'published_date', 'author')
                ORDER BY column_name;
            """)
            
            result = await session.execute(verify_query)
            columns = result.fetchall()
            
            print("   Final column structure:")
            for col in columns:
                print(f"     {col[0]}: {col[1]} (nullable: {col[2]}, default: {col[3]})")
            
            print("\n🎉 Migration completed successfully!")
            return True
            
    except Exception as e:
        print(f"\n❌ Migration failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        await database.close()

async def main():
    """Main function to run the migration."""
    print("🚀 Database Migration Tool")
    print("This will add source_url and published_date columns to news_articles table")
    print("=" * 60)
    
    # Confirm before proceeding
    response = input("\nDo you want to proceed with the migration? (y/N): ")
    if response.lower() != 'y':
        print("Migration cancelled.")
        return
    
    success = await run_migration()
    
    if success:
        print("\n✅ Migration completed successfully!")
        print("You can now run your application with the updated schema.")
    else:
        print("\n❌ Migration failed. Please check the error messages above.")
        print("You may need to run the SQL migration manually.")

if __name__ == "__main__":
    asyncio.run(main())
