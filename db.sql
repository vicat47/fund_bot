CREATE TABLE IF NOT EXISTS users
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    in_use INT default 1,
    bot_id TEXT NOT NULL,
    chat_id TEXT
);

CREATE TABLE IF NOT EXISTS funds
(
    id TEXT NOT NULL,
    user_id INT NOT NULL
);