def create_vacancies_model() -> str:
    return """CREATE TABLE IF NOT EXISTS vacancies(
        _id SERIAL PRIMARY KEY,
        photo_id VARCHAR(255),
        description TEXT,
        link TEXT,
        is_active BOOLEAN DEFAULT TRUE
    );"""