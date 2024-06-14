def create_admins_model() -> str:
    return """CREATE TABLE IF NOT EXISTS admins(
        _id SERIAL PRIMARY KEY,
        telegram_chat_id VARCHAR(255) UNIQUE,
        telegram_username VARCHAR(255) UNIQUE,
        photo VARCHAR(255),
        name VARCHAR(255),
        description TEXT,
        phone_number VARCHAR(255)
    );"""