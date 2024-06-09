def create_events_model() -> str:
    return """CREATE TABLE IF NOT EXISTS events(
        _id SERIAL PRIMARY KEY,
        photo_id VARCHAR(255),
        description TEXT,
        event_date VARCHAR(10),
        link TEXT,
        is_active BOOLEAN DEFAULT TRUE
    );"""