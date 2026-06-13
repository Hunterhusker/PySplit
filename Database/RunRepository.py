import sqlite3
from pathlib import Path

from Models.Game import Game
from Models.Run import Run, RunSplit
from Models.Split import Split


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
        CREATE TABLE games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            sub_title TEXT,
            start_offset REAL DEFAULT 0,
            display_pb INTEGER DEFAULT 1,
            lifetime_attempts INTEGER DEFAULT 0
        );
        
        CREATE TABLE split_definitions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            order_index INTEGER NOT NULL,
            pb_segment_ms INTEGER DEFAULT 0,
            gold_segment_ms INTEGER DEFAULT 0,
            FOREIGN KEY (game_id) REFERENCES games(id) ON DELETE CASCADE
        );
        
        CREATE TABLE runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id INTEGER NOT NULL,
            completed INTEGER DEFAULT 0,
            total_time_ms INTEGER,
            attempt_number INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (game_id) REFERENCES games(id) ON DELETE CASCADE
        );
        
        CREATE TABLE segments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id INTEGER NOT NULL,
            split_definition_id INTEGER NOT NULL,
            segment_time_ms INTEGER,
            cumulative_time_ms INTEGER,
            FOREIGN KEY (run_id) REFERENCES runs(id) ON DELETE CASCADE,
            FOREIGN KEY (split_definition_id) REFERENCES split_definitions(id) ON DELETE CASCADE
        );
        
        CREATE INDEX idx_runs_completed
        ON runs(completed);
        
        CREATE INDEX idx_run_splits_run
        ON segments(run_id);
        
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
        my_tables = {'games', 'split_definitions', 'runs', 'segments'}

        if not my_tables.issubset(tables):
            raise RuntimeError('Not all expected tables were found in game database!')

    def save_game(self, game: Game) -> int:
        """
        Updates or Inserts the Game object to the database

        Args:
            game: The Game to update/insert

        Returns:
            (int) game_id: The ID of the game that was updated
        """
        game_id = game.id  # just to make sure the variable is accessible outside the later ifs

        # if the game object doesn't have an id, insert it and save the id, else update it
        if game_id is None:
            game_id = self._insert_game(game)
            game.id = game_id
        else:
            game_id = self._update_game(game)

        # update all the splits in the game definition
        for i in range(len(game.splits)):
            split = game.splits[i]

            self.save_split_definition(split, i, game_id)

        return game_id  # return the id of the game that we updated

    def _update_game(self, game: Game):
        cur = self.conn.cursor()

        cur.execute("""
                UPDATE games
                SET title = ?,
                    sub_title = ?,
                    start_offset = ?,
                    display_pb = ?,
                    lifetime_attempts = ?
                WHERE id = ?;
                """, (
            game.title,
            game.sub_title,
            game.start_offset,
            game.display_pb,
            game.lifetime_attempts,
            game.id
        ))

        self.conn.commit()

        return game.id

    def _insert_game(self, game: Game):
        cur = self.conn.cursor()

        cur.execute("""
                INSERT INTO games (
                    title,
                    sub_title,
                    start_offset,
                    display_pb,
                    lifetime_attempts
                ) VALUES (?, ?, ?, ?, ?)
                """, (
            game.title,
            game.sub_title,
            game.start_offset,
            game.display_pb,
            game.lifetime_attempts
        ))

        self.conn.commit()

        return cur.lastrowid

    def delete_game(self, game_id: int):
        # if we try to delete something that was never inserted, don't
        if game_id is None:
            return

        # run the simple delete query, the cascades should take care of the rest
        cur = self.conn.cursor()
        cur.execute("""
        DELETE FROM games
        WHERE id = ?;
        """,
        (game_id,))
        self.conn.commit()

    def list_games(self) -> list[dict]:
        """
        Creates a list of game names and their id numbers so that users can select which game to use
        Returns:
            (list[dict]): Returns a list of dictionaries as follows {title, subTitle, id}
        """
        cur = self.conn.cursor()
        cur.execute("""
        SELECT title, sub_title, id FROM games;
        """)

        rows = cur.fetchall()

        game_options = []
        for row in rows:
            game_options.append({'title': row['title'], 'subTitle': row['sub_title'], 'id': row['id']})

        return game_options

    def save_split_definition(self, split_definition: Split, split_index: int, game_id: int):
        split_id = split_definition.id

        if split_id is None:
            split_id = self._insert_split_definition(split_definition, split_index, game_id)
        else:
            self._update_split_definition(split_definition, split_index, game_id)

        return split_id

    def delete_split_definition(self, split_definition_id: int):
        if split_definition_id is None:  # don't delete a split we haven't actually saved
            return

        cur = self.conn.cursor()  # delete the split and let cascades do the rest
        cur.execute("""
        DELETE FROM split_definitions
        WHERE id = ?;
        """,
        (split_definition_id,))
        self.conn.commit()

    def _update_split_definition(self, split_definition: Split, split_index: int, game_id: int):
        cur = self.conn.cursor()

        cur.execute("""
                UPDATE split_definitions
                SET name = ?,
                    order_index = ?,
                    pb_segment_ms = ?,
                    gold_segment_ms = ?
                WHERE id = ? AND game_id = ?;
                """, (
            split_definition.split_name,
            split_index,
            split_definition.pb_segment_ms,
            split_definition.gold_segment_ms,
            split_definition.id,
            game_id
        ))

        self.conn.commit()

        return split_definition.id

    def _insert_split_definition(self, split_definition: Split, split_index: int, game_id: int):
        cur = self.conn.cursor()

        cur.execute("""
                INSERT INTO split_definitions (
                    game_id,
                    name,
                    order_index,
                    pb_segment_ms,
                    gold_segment_ms
                ) VALUES (?, ?, ?, ?, ?)
                """, (
            game_id,
            split_definition.split_name,
            split_index,
            split_definition.pb_segment_ms,
            split_definition.gold_segment_ms
        ))

        self.conn.commit()

        return cur.lastrowid

    def save_run(self, run: Run):
        cur = self.conn.cursor()

        cur.execute("""
        INSERT INTO runs (completed, total_time_ms, attempt_number, created_at)
        VALUES (?, ?, ?, ?)
        """, (
            run.completed,
            run.total_time_ms,
            run.attempt_number,
            run.created_at
        ))

        self.conn.commit()

    def save_run_split(self, run_split: RunSplit):
        cur = self.conn.cursor()

        cur.execute("""
        INSERT INTO segments (run_id, split_definition_id, segment_time_ms, cumulative_time_ms)
        VALUES (?, ?, ?, ?)
        """, (
            run_split.run_id,
            run_split.split_definition_id,
            run_split.segment_time_ms,
            run_split.cumulative_time_ms
        ))

        self.conn.commit()

    # Loader methods that we use to get our objects out of the database
    def load_game(self, game_id: int) -> Game:
        # get the game data from the database
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM games WHERE id = ?", (game_id,))
        row = cur.fetchone()

        # also grab the split definitions from their rows in the database
        splits = self.load_split_definitions(game_id)

        return Game(
            id=game_id,
            title=row["title"],
            sub_title=row["sub_title"],
            start_offset=row["start_offset"],
            display_pb=row["display_pb"],
            lifetime_attempts=row["lifetime_attempts"],
            session_attempts=0,  # from the DB we're always going to assume it is a fresh session
            splits=splits  # the splits loaded for this game id
        )

    def load_split_definitions(self, game_id: int) -> list[Split]:
        splits = []

        cur = self.conn.cursor()
        cur.execute("""
            SELECT sd.*
            FROM split_definitions sd
            JOIN (
                SELECT order_index, MAX(id) as max_id
                FROM split_definitions
                WHERE game_id = 1
                GROUP BY order_index
            ) latest
            ON sd.order_index = latest.order_index
            AND sd.id = latest.max_id
            ORDER BY order_index;""")

        rows = cur.fetchall()
        local_total = 0

        for row in rows:  # create the splits in order from the database
            local_total += row['pb_segment_ms']  # add the pb segment to the total to get the accumulated time

            splits.append(Split(
                id=row['id'],
                split_name=row['name'],
                pb_time_ms=local_total,
                pb_segment_ms=row['pb_segment_ms'],
                gold_segment_ms=row['gold_segment_ms']
            ))

        return splits

    def load_run(self) -> Run:
        pass

    def load_run_splits(self) -> list[RunSplit]:
        pass
