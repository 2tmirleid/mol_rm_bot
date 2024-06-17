def create_events_model() -> str:
    return """CREATE TABLE IF NOT EXISTS events(
        _id SERIAL PRIMARY KEY,
        photo VARCHAR(255),
        title VARCHAR(255),
        description TEXT,
        date VARCHAR(10),
        link TEXT,
        is_active BOOLEAN DEFAULT TRUE
    );"""