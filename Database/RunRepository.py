import sqlite3
from pathlib import Path


class RunRepository:
    def __init__(self, database_path_string: str):
        db_path = Path(database_path_string)
        db_path.parent.mkdir(parents=True, exist_ok=True)

        db_exists = db_path.exists()

        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._configure()

        if not db_exists:
            self._create_tables()
        else:
            self._validate_schema()

    def _configure(self):
        cur = self.conn.cursor()
        cur.execute("PRAGMA foreign_keys = ON")
        cur.execute("PRAGMA journal_mode = WAL")
        cur.execute("PRAGMA synchronous = NORMAL")

    def _create_tables(self):
        cur = self.conn.cursor()

        cur.executescript("""
        CREATE TABLE game (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            sub_title TEXT,
            start_offset REAL DEFAULT 0,
            display_pb INTEGER DEFAULT 1,
            lifetime_attempts INTEGER DEFAULT 0
        );
        
        
        CREATE TABLE split_definitions (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            order_index INTEGER NOT NULL,
            pb_segment_ms INTEGER,
            gold_segment_ms INTEGER
        );
        
        CREATE TABLE runs (
            id INTEGER PRIMARY KEY,
            completed INTEGER DEFAULT 0,
            total_time_ms INTEGER,
            attempt_number INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE splits (
            id INTEGER PRIMARY KEY,
            run_id INTEGER NOT NULL,
            split_definition_id INTEGER NOT NULL,
            segment_time_ms INTEGER,
            cumulative_time_ms INTEGER,
            FOREIGN KEY (run_id) REFERENCES runs(id),
            FOREIGN KEY (split_definition_id) REFERENCES split_definitions(id)
        );
        
        CREATE INDEX idx_runs_completed
        ON runs(completed);
        
        CREATE INDEX idx_run_splits_run
        ON splits(run_id);
        
        CREATE INDEX idx_split_order
        ON split_definitions(order_index);
        """)

        self.conn.commit()

    def _validate_schema(self):
        cur = self.conn.cursor()

        cur.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table';
        """)

        tables = {row[0] for row in cur.fetchall()}
        my_tables = {'game', 'split_definitions', 'runs', 'splits'}

        if not my_tables.issubset(tables):
            raise RuntimeError('Not all expected tables were found in game database!')

    def cursor(self):
        return self.conn.cursor()

    def close(self):
        self.conn.close()

    def commit(self):
        self.conn.commit()
