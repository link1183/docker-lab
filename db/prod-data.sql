CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY,
  name TEXT,
  email TEXT
);

INSERT INTO users (name, email) 
SELECT 'Real User', 'realuser@example.com'
WHERE NOT EXISTS (SELECT 1 FROM users);

INSERT INTO users (name, email) 
SELECT 'Admin User', 'adminuser@example.com'
WHERE NOT EXISTS (SELECT 1 FROM users);
