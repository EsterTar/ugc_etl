CREATE TABLE IF NOT EXISTS default.events (
    event String
) ENGINE = MergeTree()
ORDER BY event;