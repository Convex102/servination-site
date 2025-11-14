import sqlite3
import json
from typing import List, Tuple, Optional

DB_PATH = "servination.db"


def init():
    """Initialise the SQLite database with required tables and ensure a dev tenant exists."""
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    # Tenants: used for API key / plan mapping
    cur.execute(
        """CREATE TABLE IF NOT EXISTS tenants(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            plan TEXT,
            api_key TEXT UNIQUE,
            credits INTEGER
        )"""
    )
    # Simple IP-based usage tracking for anonymous 'sample' requests
    cur.execute(
        """CREATE TABLE IF NOT EXISTS ip_usage(
            ip TEXT PRIMARY KEY,
            uses INTEGER DEFAULT 0
        )"""
    )
    # Conversation memory per tenant / IP / assistant
    cur.execute(
        """CREATE TABLE IF NOT EXISTS conversation_memory(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tenant_id INTEGER,
            ip TEXT,
            assistant TEXT,
            role TEXT,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )"""
    )
    # Simple knowledge document store with embeddings for RAG
    cur.execute(
        """CREATE TABLE IF NOT EXISTS knowledge_docs(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tenant_id INTEGER,
            assistant TEXT,
            doc_id TEXT,
            title TEXT,
            text TEXT,
            embedding TEXT
        )"""
    )

    # --- Dev convenience: ensure there is at least one tenant so the client login can be tested ---
    try:
        cur.execute(
            "SELECT id FROM tenants WHERE email = ?",
            ("nuttallg101@gmail.com",),
        )
        row = cur.fetchone()
        if not row:
            # Create a high-plan dev tenant for local testing
            dev_api_key = "SERV-DEV-GRAEME-KEY"
            cur.execute(
                "INSERT INTO tenants(name,email,plan,api_key,credits) VALUES(?,?,?,?,?)",
                ("Graeme (Dev)", "nuttallg101@gmail.com", "diamond", dev_api_key, 100000),
            )
    except Exception:
        # Fail open: database is still valid, just without the seeded tenant
        pass

    con.commit()
    con.close()



def create_tenant(name, email, plan, api_key, credits):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(
        "INSERT INTO tenants(name,email,plan,api_key,credits) VALUES(?,?,?,?,?)",
        (name, email, plan, api_key, credits),
    )
    con.commit()
    con.close()


def verify_key(api_key: str):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(
        "SELECT id,name,email,plan,api_key,credits FROM tenants WHERE api_key=?",
        (api_key,),
    )
    row = cur.fetchone()
    con.close()
    return row


def increment_ip_usage(ip: str) -> int:
    """Increment and return the number of anonymous sample uses for a given IP.

    This is a simple demo implementation to cap 'try it' usage at two requests per IP.
    In a production setup you would typically key this to authenticated user accounts
    instead of raw IP addresses.
    """
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    # Ensure a row exists
    cur.execute(
        "INSERT OR IGNORE INTO ip_usage(ip, uses) VALUES(?, 0)",
        (ip,),
    )
    # Increment
    cur.execute(
        "UPDATE ip_usage SET uses = uses + 1 WHERE ip = ?",
        (ip,),
    )
    # Fetch updated count
    cur.execute("SELECT uses FROM ip_usage WHERE ip = ?", (ip,))
    row = cur.fetchone()
    con.commit()
    con.close()
    return int(row[0]) if row else 0


# ---- Conversation memory helpers -------------------------------------------------


def add_memory(
    tenant_id: Optional[int],
    ip: Optional[str],
    assistant: str,
    role: str,
    content: str,
) -> None:
    """Append a memory entry for a tenant or anonymous IP."""
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(
        "INSERT INTO conversation_memory(tenant_id, ip, assistant, role, content) VALUES(?,?,?,?,?)",
        (tenant_id, ip, assistant, role, content),
    )
    con.commit()
    con.close()


def get_recent_memory(
    tenant_id: Optional[int],
    ip: Optional[str],
    assistant: str,
    limit: int = 6,
) -> List[Tuple[str, str]]:
    """Return recent (role, content) memory entries for a given assistant."""
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    if tenant_id is not None:
        cur.execute(
            """SELECT role, content
                   FROM conversation_memory
                   WHERE tenant_id = ? AND assistant = ?
                   ORDER BY id DESC
                   LIMIT ?""",
            (tenant_id, assistant, limit),
        )
    else:
        cur.execute(
            """SELECT role, content
                   FROM conversation_memory
                   WHERE ip = ? AND assistant = ?
                   ORDER BY id DESC
                   LIMIT ?""",
            (ip, assistant, limit),
        )
    rows = cur.fetchall() or []
    con.close()
    # Reverse to chronological order
    return list(reversed(rows))


def clear_memory(tenant_id: Optional[int], ip: Optional[str], assistant: str) -> None:
    """Clear stored memory for a given assistant / tenant or IP."""
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    if tenant_id is not None:
        cur.execute(
            "DELETE FROM conversation_memory WHERE tenant_id = ? AND assistant = ?",
            (tenant_id, assistant),
        )
    else:
        cur.execute(
            "DELETE FROM conversation_memory WHERE ip = ? AND assistant = ?",
            (ip, assistant),
        )
    con.commit()
    con.close()


# ---- Knowledge document store (vector RAG) ---------------------------------------


def upsert_knowledge_doc(
    tenant_id: Optional[int],
    assistant: str,
    doc_id: str,
    title: str,
    text: str,
    embedding: list[float],
) -> None:
    """Insert or update a knowledge document for RAG."""
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    embedding_json = json.dumps(embedding)
    # Simple upsert by (tenant_id, assistant, doc_id)
    cur.execute(
        """SELECT id FROM knowledge_docs
               WHERE tenant_id IS ? AND assistant = ? AND doc_id = ?""",
        (tenant_id, assistant, doc_id),
    )
    row = cur.fetchone()
    if row:
        cur.execute(
            """UPDATE knowledge_docs
                   SET title = ?, text = ?, embedding = ?
                   WHERE id = ?""",
            (title, text, embedding_json, row[0]),
        )
    else:
        cur.execute(
            """INSERT INTO knowledge_docs(tenant_id, assistant, doc_id, title, text, embedding)
                   VALUES(?,?,?,?,?,?)""",
            (tenant_id, assistant, doc_id, title, text, embedding_json),
        )
    con.commit()
    con.close()


def _cosine_similarity(vec_a, vec_b) -> float:
    """Compute cosine similarity between two vectors represented as Python lists."""
    if not vec_a or not vec_b or len(vec_a) != len(vec_b):
        return 0.0
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = sum(a * a for a in vec_a) ** 0.5
    norm_b = sum(b * b for b in vec_b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def query_knowledge_docs(
    tenant_id: Optional[int],
    assistant: str,
    query_embedding: list[float],
    top_k: int = 5,
):
    """Return top_k knowledge docs ranked by cosine similarity to the query embedding."""
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(
        """SELECT id, title, text, embedding
               FROM knowledge_docs
               WHERE tenant_id IS ? AND assistant = ?""",
        (tenant_id, assistant),
    )
    rows = cur.fetchall() or []
    con.close()

    scored = []
    for doc_id, title, text, emb_json in rows:
        try:
            emb = json.loads(emb_json) if emb_json else []
        except Exception:
            emb = []
        score = _cosine_similarity(query_embedding, emb)
        scored.append((score, {"id": doc_id, "title": title, "text": text}))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [item for _, item in scored[:top_k]]
