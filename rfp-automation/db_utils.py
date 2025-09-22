"""
Database utilities for the RFP Response Automation application
"""

import sqlite3
import os
from typing import List, Tuple, Optional


def init_db() -> None:
    """Initialize the database with required tables."""
    try:
        conn = sqlite3.connect('rfp_automation.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bids (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bid_name TEXT NOT NULL,
                contact_name TEXT,
                contact_email TEXT,
                summary TEXT,
                status TEXT DEFAULT 'Draft',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error initializing database: {e}")


def get_all_bids() -> List[Tuple]:
    """Retrieve all bids from the database."""
    try:
        conn = sqlite3.connect('rfp_automation.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, bid_name, contact_name, contact_email, summary, status, created_at, updated_at
            FROM bids
            ORDER BY created_at DESC
        ''')
        
        bids = cursor.fetchall()
        conn.close()
        return bids
    except Exception as e:
        print(f"Error retrieving bids: {e}")
        return []


def delete_bid(bid_id: int) -> bool:
    """Delete a bid from the database."""
    try:
        conn = sqlite3.connect('rfp_automation.db')
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM bids WHERE id = ?', (bid_id,))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error deleting bid {bid_id}: {e}")
        return False


def create_bid(bid_name: str, contact_name: str = None, contact_email: str = None, 
               summary: str = None, status: str = "Draft") -> Optional[int]:
    """Create a new bid in the database."""
    try:
        conn = sqlite3.connect('rfp_automation.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO bids (bid_name, contact_name, contact_email, summary, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (bid_name, contact_name, contact_email, summary, status))
        
        bid_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return bid_id
    except Exception as e:
        print(f"Error creating bid: {e}")
        return None


def update_bid(bid_id: int, **kwargs) -> bool:
    """Update a bid in the database."""
    try:
        conn = sqlite3.connect('rfp_automation.db')
        cursor = conn.cursor()
        
        fields = []
        values = []
        for key, value in kwargs.items():
            if key in ['bid_name', 'contact_name', 'contact_email', 'summary', 'status']:
                fields.append(f"{key} = ?")
                values.append(value)
        
        if not fields:
            return False
            
        fields.append("updated_at = CURRENT_TIMESTAMP")
        values.append(bid_id)
        
        query = f"UPDATE bids SET {', '.join(fields)} WHERE id = ?"
        cursor.execute(query, values)
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating bid {bid_id}: {e}")
        return False
