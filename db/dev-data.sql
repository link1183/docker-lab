CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  name TEXT,
  email TEXT
);

INSERT INTO users (name, email) VALUES
  ('Test User', 'testuser@example.com'),
  ('Mock User', 'mockuser@example.com');
