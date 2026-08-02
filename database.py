"""
SQLite database layer for the Nigeria Grant & Empowerment Tracker.
"""

import sqlite3
from datetime import datetime, date
from pathlib import Path
from typing import Optional, List, Dict, Any

DB_PATH = Path(__file__).parent / "data" / "grants.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    """Create tables and seed sample data if the database is new."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = get_connection()
    cur = conn.cursor()

    cur.executescript(
        """
        CREATE TABLE IF NOT EXISTS grants (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            title           TEXT NOT NULL,
            organization    TEXT NOT NULL,
            category        TEXT NOT NULL,          -- scholarship, business, agriculture, youth, women, skills, loan, other
            description     TEXT NOT NULL,
            eligibility     TEXT,
            benefits        TEXT,
            deadline        TEXT,                   -- ISO date or 'Ongoing' / 'Rolling'
            application_url TEXT,
            states          TEXT DEFAULT 'Nationwide',  -- comma-separated or Nationwide
            target_group    TEXT,                   -- youth, women, students, farmers, etc.
            amount          TEXT,                   -- e.g. "₦1,000,000" or "Up to ₦50M"
            status          TEXT DEFAULT 'open',    -- open, closed, upcoming
            created_at      TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at      TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS users (
            user_id         INTEGER PRIMARY KEY,
            username        TEXT,
            first_name      TEXT,
            last_name       TEXT,
            preferred_state TEXT DEFAULT 'Nationwide',
            preferred_categories TEXT DEFAULT '',   -- comma-separated
            notify_new      INTEGER DEFAULT 1,
            notify_deadline INTEGER DEFAULT 1,
            joined_at       TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS subscriptions (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id         INTEGER NOT NULL,
            category        TEXT NOT NULL,
            UNIQUE(user_id, category),
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS saved_grants (
            user_id         INTEGER NOT NULL,
            grant_id        INTEGER NOT NULL,
            saved_at        TEXT DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (user_id, grant_id),
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
            FOREIGN KEY (grant_id) REFERENCES grants(id) ON DELETE CASCADE
        );
        """
    )
    conn.commit()

    # Seed only if empty
    count = cur.execute("SELECT COUNT(*) FROM grants").fetchone()[0]
    if count == 0:
        seed_sample_grants(conn)

    conn.close()


def seed_sample_grants(conn: sqlite3.Connection) -> None:
    """Insert realistic sample grants based on current Nigerian programmes."""
    samples = [
        {
            "title": "NELFUND Student Loan Scheme",
            "organization": "Nigerian Education Loan Fund (NELFUND)",
            "category": "scholarship",
            "description": "Interest-free student loans covering tuition and upkeep for Nigerian students in tertiary institutions. Repayment starts after NYSC.",
            "eligibility": "Nigerian citizens admitted into accredited public tertiary institutions. Must meet income and academic criteria.",
            "benefits": "Interest-free loans for tuition + upkeep. Flexible repayment after graduation/NYSC.",
            "deadline": "Ongoing",
            "application_url": "https://nelf.gov.ng/",
            "states": "Nationwide",
            "target_group": "students",
            "amount": "Tuition + Upkeep (as approved)",
            "status": "open",
        },
        {
            "title": "BOI Guaranteed Loans for Women (GLOW)",
            "organization": "Bank of Industry (BOI)",
            "category": "loan",
            "description": "₦10 billion intervention fund providing affordable financing, mentorship and capacity building for women-owned and women-led businesses.",
            "eligibility": "Women-owned or women-led MSMEs registered in Nigeria. Viable business plan required.",
            "benefits": "Loans up to ₦50 million at single-digit interest, plus mentorship.",
            "deadline": "Ongoing",
            "application_url": "https://iprogrammes.boi.ng/",
            "states": "Nationwide",
            "target_group": "women",
            "amount": "Up to ₦50,000,000",
            "status": "open",
        },
        {
            "title": "NiYA Startup Grants",
            "organization": "Federal Ministry of Youth Development / Nigerian Youth Academy",
            "category": "business",
            "description": "Seed grants and support for youth-led startups and informal sector beneficiaries under the NiYA StartUp Programme.",
            "eligibility": "Young Nigerian entrepreneurs (typically 18–35) with innovative or scalable ideas.",
            "benefits": "₦1,000,000 grants for selected startups + ₦500,000 for informal sector; mentorship & visibility.",
            "deadline": "Check portal for current cohort",
            "application_url": "https://fmyd.gov.ng/",
            "states": "Nationwide",
            "target_group": "youth",
            "amount": "₦500,000 – ₦1,000,000",
            "status": "open",
        },
        {
            "title": "3MTT Technical Talent Programme",
            "organization": "NITDA / Federal Government",
            "category": "skills",
            "description": "3 Million Technical Talent programme training Nigerians in high-demand digital and technical skills with pathways to employment and freelancing.",
            "eligibility": "Nigerian citizens interested in tech skills (software, data, cybersecurity, etc.).",
            "benefits": "Free/subsidised training, certification, job placement support.",
            "deadline": "Ongoing (cohort-based)",
            "application_url": "https://3mtt.nitda.gov.ng/",
            "states": "Nationwide",
            "target_group": "youth",
            "amount": "Training + Placement support",
            "status": "open",
        },
        {
            "title": "Youth Investment Fund (YIF)",
            "organization": "Federal Government of Nigeria",
            "category": "business",
            "description": "Financial support and business development services for young Nigerian entrepreneurs.",
            "eligibility": "Young Nigerians with existing or startup businesses.",
            "benefits": "Access to finance and business support services.",
            "deadline": "Check yif.gov.ng",
            "application_url": "https://yif.gov.ng/",
            "states": "Nationwide",
            "target_group": "youth",
            "amount": "Varies",
            "status": "open",
        },
        {
            "title": "BOI–NYSC Entrepreneurship Programme",
            "organization": "Bank of Industry & NYSC",
            "category": "business",
            "description": "₦2 billion fund supporting NYSC Corps Members to start nano and micro enterprises with affordable financing and capacity building.",
            "eligibility": "Serving or recently passed-out NYSC Corps Members.",
            "benefits": "Affordable loans + entrepreneurship training.",
            "deadline": "Ongoing",
            "application_url": "https://iprogrammes.boi.ng/",
            "states": "Nationwide",
            "target_group": "youth",
            "amount": "Nano/Micro enterprise financing",
            "status": "open",
        },
        {
            "title": "SMEDAN Conditional Grant Scheme for Micro Enterprises",
            "organization": "SMEDAN",
            "category": "business",
            "description": "Conditional grants for micro enterprises to support business growth and formalisation.",
            "eligibility": "Registered micro enterprises meeting SMEDAN criteria.",
            "benefits": "Grant support (e.g. ₦50,000 schemes in recent rounds).",
            "deadline": "Check SMEDAN announcements",
            "application_url": "https://smedan.gov.ng/",
            "states": "Nationwide",
            "target_group": "entrepreneurs",
            "amount": "Around ₦50,000 (scheme dependent)",
            "status": "open",
        },
        {
            "title": "NNPC Renaissance Scholarship",
            "organization": "NNPC Limited / Joint Venture Partners",
            "category": "scholarship",
            "description": "Scholarships for Nigerian students in selected disciplines, often focused on STEM and oil & gas related fields.",
            "eligibility": "Nigerian students meeting academic and other criteria set by the scheme.",
            "benefits": "Tuition and related support.",
            "deadline": "Check current call",
            "application_url": "https://nnpcgroup.com/",
            "states": "Nationwide",
            "target_group": "students",
            "amount": "Full/Partial scholarship",
            "status": "open",
        },
        {
            "title": "Transforming Nigerian Youths (SARA-TNY) Seed Grants",
            "organization": "ALAT by Wema / Partners",
            "category": "business",
            "description": "Enterprise training, mentoring and seed grants of up to ₦2.5 million for young Nigerian entrepreneurs, with focus on female inclusion.",
            "eligibility": "Young Nigerian entrepreneurs (strong focus on women).",
            "benefits": "Training + seed grants up to ₦2,500,000 + market access support.",
            "deadline": "Cohort-based",
            "application_url": "https://sara-tny.alat.ng/",
            "states": "Nationwide",
            "target_group": "youth,women",
            "amount": "Up to ₦2,500,000",
            "status": "open",
        },
        {
            "title": "AfDB Youth & Women-Led Enterprises Support",
            "organization": "African Development Bank / Partners",
            "category": "business",
            "description": "Large-scale financing and business support targeting youth and women-led enterprises in Nigeria.",
            "eligibility": "Youth and women-led MSMEs.",
            "benefits": "Access to capital and business development services.",
            "deadline": "Through implementing partners",
            "application_url": "https://www.afdb.org/",
            "states": "Nationwide",
            "target_group": "youth,women",
            "amount": "Varies (programme scale ~$100M)",
            "status": "open",
        },
        {
            "title": "First Lady Renewed Hope Women Empowerment Grants",
            "organization": "Office of the First Lady / Renewed Hope Initiative",
            "category": "women",
            "description": "Grant support for women entrepreneurs to strengthen micro and small businesses.",
            "eligibility": "Nigerian women running or starting micro businesses.",
            "benefits": "Direct grants (recent rounds included ₦50,000 packages).",
            "deadline": "Announced per state/phase",
            "application_url": "Check official First Lady / RHI channels",
            "states": "Nationwide",
            "target_group": "women",
            "amount": "Around ₦50,000 (phase dependent)",
            "status": "open",
        },
        {
            "title": "PTDF Scholarship Scheme",
            "organization": "Petroleum Technology Development Fund",
            "category": "scholarship",
            "description": "Scholarships for Nigerians to study oil & gas related courses locally and overseas.",
            "eligibility": "Nigerian citizens with relevant academic background; specific criteria per call.",
            "benefits": "Full scholarships for approved programmes.",
            "deadline": "Annual calls – check PTDF portal",
            "application_url": "https://ptdf.gov.ng/",
            "states": "Nationwide",
            "target_group": "students",
            "amount": "Full scholarship",
            "status": "open",
        },
    ]

    cur = conn.cursor()
    for g in samples:
        cur.execute(
            """
            INSERT INTO grants (
                title, organization, category, description, eligibility,
                benefits, deadline, application_url, states, target_group,
                amount, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                g["title"],
                g["organization"],
                g["category"],
                g["description"],
                g["eligibility"],
                g["benefits"],
                g["deadline"],
                g["application_url"],
                g["states"],
                g["target_group"],
                g["amount"],
                g["status"],
            ),
        )
    conn.commit()


# --------------- Grant helpers ---------------

def add_grant(data: Dict[str, Any]) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO grants (
            title, organization, category, description, eligibility,
            benefits, deadline, application_url, states, target_group,
            amount, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data["title"],
            data["organization"],
            data["category"],
            data["description"],
            data.get("eligibility", ""),
            data.get("benefits", ""),
            data.get("deadline", "Ongoing"),
            data.get("application_url", ""),
            data.get("states", "Nationwide"),
            data.get("target_group", ""),
            data.get("amount", ""),
            data.get("status", "open"),
        ),
    )
    grant_id = cur.lastrowid
    conn.commit()
    conn.close()
    return grant_id


def update_grant(grant_id: int, data: Dict[str, Any]) -> bool:
    conn = get_connection()
    cur = conn.cursor()
    fields = []
    values = []
    for key in [
        "title", "organization", "category", "description", "eligibility",
        "benefits", "deadline", "application_url", "states", "target_group",
        "amount", "status",
    ]:
        if key in data:
            fields.append(f"{key} = ?")
            values.append(data[key])
    if not fields:
        conn.close()
        return False
    fields.append("updated_at = ?")
    values.append(datetime.utcnow().isoformat())
    values.append(grant_id)
    cur.execute(f"UPDATE grants SET {', '.join(fields)} WHERE id = ?", values)
    updated = cur.rowcount > 0
    conn.commit()
    conn.close()
    return updated


def delete_grant(grant_id: int) -> bool:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM grants WHERE id = ?", (grant_id,))
    deleted = cur.rowcount > 0
    conn.commit()
    conn.close()
    return deleted


def get_grant(grant_id: int) -> Optional[Dict]:
    conn = get_connection()
    row = conn.execute("SELECT * FROM grants WHERE id = ?", (grant_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def search_grants(
    query: str = "",
    category: str = "",
    state: str = "",
    target_group: str = "",
    status: str = "open",
    limit: int = 20,
    offset: int = 0,
) -> List[Dict]:
    conn = get_connection()
    sql = "SELECT * FROM grants WHERE 1=1"
    params: List[Any] = []

    if status:
        sql += " AND status = ?"
        params.append(status)
    if category:
        sql += " AND category = ?"
        params.append(category.lower())
    if query:
        sql += " AND (title LIKE ? OR description LIKE ? OR organization LIKE ? OR benefits LIKE ?)"
        q = f"%{query}%"
        params.extend([q, q, q, q])
    if state and state.lower() != "nationwide":
        sql += " AND (states LIKE ? OR states = 'Nationwide')"
        params.append(f"%{state}%")
    if target_group:
        sql += " AND (target_group LIKE ? OR target_group = '')"
        params.append(f"%{target_group}%")

    sql += " ORDER BY updated_at DESC, id DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def count_grants(category: str = "", status: str = "open") -> int:
    conn = get_connection()
    sql = "SELECT COUNT(*) FROM grants WHERE 1=1"
    params = []
    if status:
        sql += " AND status = ?"
        params.append(status)
    if category:
        sql += " AND category = ?"
        params.append(category.lower())
    count = conn.execute(sql, params).fetchone()[0]
    conn.close()
    return count


def get_categories() -> List[str]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT DISTINCT category FROM grants WHERE status = 'open' ORDER BY category"
    ).fetchall()
    conn.close()
    return [r[0] for r in rows]


# --------------- User helpers ---------------

def upsert_user(user_id: int, username: str = None, first_name: str = None, last_name: str = None) -> None:
    conn = get_connection()
    conn.execute(
        """
        INSERT INTO users (user_id, username, first_name, last_name)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            username = excluded.username,
            first_name = excluded.first_name,
            last_name = excluded.last_name
        """,
        (user_id, username, first_name, last_name),
    )
    conn.commit()
    conn.close()


def get_user(user_id: int) -> Optional[Dict]:
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def set_user_preference(user_id: int, key: str, value: Any) -> None:
    allowed = {"preferred_state", "preferred_categories", "notify_new", "notify_deadline"}
    if key not in allowed:
        return
    conn = get_connection()
    conn.execute(f"UPDATE users SET {key} = ? WHERE user_id = ?", (value, user_id))
    conn.commit()
    conn.close()


def save_grant_for_user(user_id: int, grant_id: int) -> bool:
    conn = get_connection()
    try:
        conn.execute(
            "INSERT OR IGNORE INTO saved_grants (user_id, grant_id) VALUES (?, ?)",
            (user_id, grant_id),
        )
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()


def unsave_grant(user_id: int, grant_id: int) -> None:
    conn = get_connection()
    conn.execute(
        "DELETE FROM saved_grants WHERE user_id = ? AND grant_id = ?",
        (user_id, grant_id),
    )
    conn.commit()
    conn.close()


def get_saved_grants(user_id: int) -> List[Dict]:
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT g.* FROM grants g
        JOIN saved_grants s ON g.id = s.grant_id
        WHERE s.user_id = ?
        ORDER BY s.saved_at DESC
        """,
        (user_id,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_users_for_notification(category: str = None) -> List[int]:
    """Return user_ids who want notifications (optionally filtered by category preference)."""
    conn = get_connection()
    if category:
        rows = conn.execute(
            """
            SELECT user_id FROM users
            WHERE notify_new = 1
              AND (preferred_categories = '' OR preferred_categories LIKE ?)
            """,
            (f"%{category}%",),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT user_id FROM users WHERE notify_new = 1"
        ).fetchall()
    conn.close()
    return [r[0] for r in rows]
