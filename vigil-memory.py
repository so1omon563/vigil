#!/usr/bin/env python3
"""
Vigil Memory System
==================
SQLite-based memory storage without embeddings (simplified from Sammy's approach).
Text search via SQLite FTS5 for semantic-ish retrieval without Ollama dependency.

Usage:
    python3 vigil-memory.py add "System running on Raspberry Pi in Mesa, AZ" --category system
    python3 vigil-memory.py add "Always use so1omon (not Jed) in public content" --category rule
    python3 vigil-memory.py search "location"
    python3 vigil-memory.py category promises
    python3 vigil-memory.py startup
    python3 vigil-memory.py list
    python3 vigil-memory.py count
    python3 vigil-memory.py delete <id>
"""

import sys
import os
import json
import argparse
import time
import sqlite3

DB_PATH = "/home/so1omon/autonomous-ai/vigil-memory.db"

def get_db():
    """Initialize database with FTS5 for full-text search."""
    conn = sqlite3.connect(DB_PATH)

    # Main memories table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            category TEXT DEFAULT 'general',
            person TEXT DEFAULT '',
            created_at TEXT NOT NULL,
            last_accessed TEXT
        )
    """)

    # FTS5 virtual table for fast text search
    conn.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts USING fts5(
            text,
            content='memories',
            content_rowid='id'
        )
    """)

    # Triggers to keep FTS in sync
    conn.execute("""
        CREATE TRIGGER IF NOT EXISTS memories_ai AFTER INSERT ON memories BEGIN
            INSERT INTO memories_fts(rowid, text) VALUES (new.id, new.text);
        END
    """)
    conn.execute("""
        CREATE TRIGGER IF NOT EXISTS memories_ad AFTER DELETE ON memories BEGIN
            DELETE FROM memories_fts WHERE rowid = old.id;
        END
    """)
    conn.execute("""
        CREATE TRIGGER IF NOT EXISTS memories_au AFTER UPDATE ON memories BEGIN
            UPDATE memories_fts SET text = new.text WHERE rowid = new.id;
        END
    """)

    conn.execute("CREATE INDEX IF NOT EXISTS idx_category ON memories(category)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_person ON memories(person)")
    conn.commit()
    return conn

def add_memory(text, category="general", person=""):
    """Add a memory to the database."""
    conn = get_db()
    now = time.strftime("%Y-%m-%dT%H:%M:%S")
    conn.execute(
        "INSERT INTO memories (text, category, person, created_at, last_accessed) VALUES (?, ?, ?, ?, ?)",
        (text, category, person, now, now)
    )
    conn.commit()
    last_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.close()
    return last_id

def search_memory(query, limit=10, category=None, person=None):
    """Search memories using FTS5."""
    conn = get_db()

    if category or person:
        # Filtered search: use FTS + JOIN
        where = []
        params = [query]
        if category:
            where.append("m.category = ?")
            params.append(category)
        if person:
            where.append("m.person = ?")
            params.append(person)

        where_clause = " AND " + " AND ".join(where) if where else ""
        sql = f"""
            SELECT m.id, m.text, m.category, m.person, m.created_at, fts.rank
            FROM memories_fts fts
            JOIN memories m ON m.id = fts.rowid
            WHERE memories_fts MATCH ?{where_clause}
            ORDER BY fts.rank
            LIMIT ?
        """
        params.append(limit)
        rows = conn.execute(sql, params).fetchall()
    else:
        # Pure FTS search
        rows = conn.execute("""
            SELECT m.id, m.text, m.category, m.person, m.created_at, fts.rank
            FROM memories_fts fts
            JOIN memories m ON m.id = fts.rowid
            WHERE memories_fts MATCH ?
            ORDER BY fts.rank
            LIMIT ?
        """, (query, limit)).fetchall()

    # Update last_accessed for retrieved memories
    now = time.strftime("%Y-%m-%dT%H:%M:%S")
    for row in rows:
        conn.execute("UPDATE memories SET last_accessed = ? WHERE id = ?", (now, row[0]))
    conn.commit()
    conn.close()

    results = []
    for row in rows:
        rid, text, cat, per, created, rank = row
        results.append({
            "id": rid,
            "text": text,
            "category": cat,
            "person": per,
            "created_at": created,
            "rank": rank
        })
    return results

def list_by_category(category):
    """List all memories in a category."""
    conn = get_db()
    rows = conn.execute(
        "SELECT id, text, category, person, created_at FROM memories WHERE category = ? ORDER BY id DESC",
        (category,)
    ).fetchall()
    conn.close()
    return rows

def list_all():
    """List all memories."""
    conn = get_db()
    rows = conn.execute(
        "SELECT id, text, category, person, created_at FROM memories ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return rows

def count_memories():
    """Count total memories."""
    conn = get_db()
    count = conn.execute("SELECT COUNT(*) FROM memories").fetchone()[0]
    conn.close()
    return count

def delete_memory(mem_id):
    """Delete a memory by ID."""
    conn = get_db()
    conn.execute("DELETE FROM memories WHERE id = ?", (mem_id,))
    conn.commit()
    conn.close()

def check_integrity():
    """Run integrity checks on vigil-memory.db. Returns (passed, report)."""
    import os
    report = []
    passed = True

    if not os.path.exists(DB_PATH):
        return False, ["ERROR: database file not found at " + DB_PATH]

    size_bytes = os.path.getsize(DB_PATH)
    report.append(f"File size: {size_bytes:,} bytes")

    conn = get_db()
    try:
        # PRAGMA integrity_check: checks B-tree structure, page counts, sort order
        integrity = conn.execute("PRAGMA integrity_check").fetchall()
        if integrity == [("ok",)]:
            report.append("PRAGMA integrity_check: OK")
        else:
            passed = False
            for row in integrity:
                report.append("INTEGRITY ERROR: " + row[0])

        # PRAGMA quick_check: faster, skips cross-reference checks
        quick = conn.execute("PRAGMA quick_check").fetchall()
        if quick == [("ok",)]:
            report.append("PRAGMA quick_check: OK")
        else:
            passed = False
            for row in quick:
                report.append("QUICK CHECK ERROR: " + row[0])

        # FTS5 integrity check
        try:
            conn.execute("INSERT INTO memories_fts(memories_fts) VALUES('integrity-check')")
            conn.rollback()
            report.append("FTS5 index: OK")
        except Exception as e:
            passed = False
            report.append(f"FTS5 ERROR: {e}")

        # Row count consistency: memories vs FTS
        mem_count = conn.execute("SELECT COUNT(*) FROM memories").fetchone()[0]
        fts_count = conn.execute("SELECT COUNT(*) FROM memories_fts").fetchone()[0]
        report.append(f"Rows in memories: {mem_count}")
        report.append(f"Rows in memories_fts: {fts_count}")
        if mem_count != fts_count:
            passed = False
            report.append(f"ROW COUNT MISMATCH: memories={mem_count} fts={fts_count}")
        else:
            report.append("Row count consistency: OK")

        # Expected columns
        cols = [row[1] for row in conn.execute("PRAGMA table_info(memories)").fetchall()]
        expected = {"id", "text", "category", "person", "created_at", "last_accessed"}
        missing = expected - set(cols)
        if missing:
            passed = False
            report.append(f"MISSING COLUMNS: {missing}")
        else:
            report.append(f"Schema columns: OK ({', '.join(sorted(cols))})")

    except Exception as e:
        passed = False
        report.append(f"UNEXPECTED ERROR: {e}")
    finally:
        conn.close()

    return passed, report

def startup_context():
    """Get essential startup context across query categories."""
    queries = [
        ("promises commitments owe", "promises", 3),
        ("email conversation reply pending", "communication", 2),
        ("system running location hardware", "system", 2),
        ("naming rule so1omon Jed", "rule", 2),
        ("recent work session journal", "recent", 3),
        ("relationship personality jedidiah foster owner", "relationship", 2),
    ]

    seen_ids = set()
    context = []

    for query, cat_hint, limit in queries:
        results = search_memory(query, limit=limit)
        for r in results:
            if r["id"] not in seen_ids:
                seen_ids.add(r["id"])
                context.append(r)

    # Sort by rank (FTS relevance)
    context.sort(key=lambda x: x["rank"] if x.get("rank") else 0)
    return context

def main():
    parser = argparse.ArgumentParser(description="Vigil Memory System")
    subparsers = parser.add_subparsers(dest="command")

    add_p = subparsers.add_parser("add", help="Add a memory")
    add_p.add_argument("text")
    add_p.add_argument("--category", default="general")
    add_p.add_argument("--person", default="")

    search_p = subparsers.add_parser("search", help="Search memories")
    search_p.add_argument("query")
    search_p.add_argument("--limit", type=int, default=10)
    search_p.add_argument("--category", default=None)
    search_p.add_argument("--person", default=None)

    cat_p = subparsers.add_parser("category", help="List by category")
    cat_p.add_argument("name")

    subparsers.add_parser("list", help="List all memories")
    subparsers.add_parser("count", help="Count memories")
    subparsers.add_parser("startup", help="Get startup context")

    del_p = subparsers.add_parser("delete", help="Delete a memory by ID")
    del_p.add_argument("id", type=int)

    subparsers.add_parser("integrity", help="Run database integrity checks")

    args = parser.parse_args()

    if args.command == "add":
        mid = add_memory(args.text, args.category, args.person)
        print(f"Added memory #{mid}")

    elif args.command == "search":
        results = search_memory(args.query, limit=args.limit, category=args.category, person=args.person)
        for r in results:
            meta = f" [{r['category']}]" if r['category'] else ""
            meta += f" (re: {r['person']})" if r['person'] else ""
            print(f"#{r['id']}{meta} {r['text']}")

    elif args.command == "category":
        rows = list_by_category(args.name)
        for r in rows:
            rid, text, cat, person, created = r
            meta = f" (re: {person})" if person else ""
            print(f"#{rid}{meta} {text}")

    elif args.command == "list":
        rows = list_all()
        for r in rows:
            rid, text, cat, person, created = r
            meta = f" [{cat}]" if cat else ""
            meta += f" (re: {person})" if person else ""
            print(f"#{rid}{meta} {text}")

    elif args.command == "count":
        print(f"Total memories: {count_memories()}")

    elif args.command == "startup":
        context = startup_context()
        print(f"Startup context ({len(context)} memories):\n")
        for c in context:
            cat = f"[{c['category']}] " if c['category'] else ""
            print(f"{cat}{c['text']}")

    elif args.command == "delete":
        delete_memory(args.id)
        print(f"Deleted memory #{args.id}")

    elif args.command == "integrity":
        import datetime
        passed, report = check_integrity()
        status = "PASSED" if passed else "FAILED"
        print(f"vigil-memory.db integrity check — {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} — {status}")
        for line in report:
            print(f"  {line}")
        if not passed:
            sys.exit(1)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
