import sqlite3
from pathlib import Path

DB_PATH = Path('conf/game_database.db')

class GameDatabase:
    def __init__(self):
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row
        self._configure()
        self._migrate()

    def _configure(self):
        cur = self.conn.cursor()
        cur.execute("PRAGMA foreign_keys = ON")
        cur.execute("PRAGMA journal_mode = WAL")
        cur.execute("PRAGMA synchronous = NORMAL")

    def _migrate(self):
        cur = self.conn.cursor()
        cur.execute("PRAGMA user_version")
        version = cur.fetchone()[0]

        if version < 1:
            cur.executescript("""
                    CREATE TABLE games (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL
                    );

                    CREATE TABLE split_versions (
                        id INTEGER PRIMARY KEY,
                        game_id INTEGER NOT NULL,
                        name TEXT NOT NULL,
                        FOREIGN KEY (game_id) REFERENCES games(id)
                    );

                    CREATE TABLE splits (
                        id INTEGER PRIMARY KEY,
                        split_version_id INTEGER NOT NULL,
                        name TEXT NOT NULL,
                        split_index INTEGER NOT NULL,
                        FOREIGN KEY (split_version_id) REFERENCES split_versions(id)
                    );

                    CREATE TABLE runs (
                        id INTEGER PRIMARY KEY,
                        game_id INTEGER NOT NULL,
                        split_version_id INTEGER NOT NULL,
                        started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        completed BOOLEAN DEFAULT 1,
                        total_time_ms INTEGER,
                        FOREIGN KEY (game_id) REFERENCES games(id),
                        FOREIGN KEY (split_version_id) REFERENCES split_versions(id)
                    );

                    CREATE TABLE run_splits (
                        id INTEGER PRIMARY KEY,
                        run_id INTEGER NOT NULL,
                        split_id INTEGER NOT NULL,
                        split_time_ms INTEGER NOT NULL,
                        segment_time_ms INTEGER NOT NULL,
                        FOREIGN KEY (run_id) REFERENCES runs(id),
                        FOREIGN KEY (split_id) REFERENCES splits(id)
                    );
                    """)
            cur.execute("PRAGMA user_version = 1")

        self.conn.commit()

    def cursor(self):
        return self.conn.cursor()

    def close(self):
        self.conn.close()

    def commit(self):
        self.conn.commit()
