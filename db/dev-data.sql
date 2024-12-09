CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY,
  name TEXT,
  email TEXT
);

INSERT INTO users (name, email) VALUES
  ('Alice Smith', 'alice.smith@example.com'),
  ('Bob Johnson', 'bob.johnson@example.com'),
  ('Charlie Brown', 'charlie.brown@example.com'),
  ('Diana Prince', 'diana.prince@example.com'),
  ('Eve Adams', 'eve.adams@example.com'),
  ('Frank Miller', 'frank.miller@example.com'),
  ('Grace Lee', 'grace.lee@example.com'),
  ('Hank Green', 'hank.green@example.com'),
  ('Ivy White', 'ivy.white@example.com'),
  ('Jack Black', 'jack.black@example.com');
