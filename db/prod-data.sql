CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY,
  name TEXT,
  email TEXT
);

-- Management users
INSERT INTO users (name, email) 
SELECT 'John Smith', 'john.smith@company.com'
WHERE NOT EXISTS (SELECT 1 FROM users WHERE email = 'john.smith@company.com');

INSERT INTO users (name, email) 
SELECT 'Sarah Johnson', 'sarah.j@company.com'
WHERE NOT EXISTS (SELECT 1 FROM users WHERE email = 'sarah.j@company.com');

-- Department leads
INSERT INTO users (name, email) 
SELECT 'Michael Chen', 'mchen@engineering.company.com'
WHERE NOT EXISTS (SELECT 1 FROM users WHERE email = 'mchen@engineering.company.com');

INSERT INTO users (name, email) 
SELECT 'Emily Rodriguez', 'emily.r@sales.company.com'
WHERE NOT EXISTS (SELECT 1 FROM users WHERE email = 'emily.r@sales.company.com');

-- Regular employees
INSERT INTO users (name, email) 
SELECT 'David Wilson', 'dwilson@company.com'
WHERE NOT EXISTS (SELECT 1 FROM users WHERE email = 'dwilson@company.com');

INSERT INTO users (name, email) 
SELECT 'Lisa Brown', 'lbrown@company.com'
WHERE NOT EXISTS (SELECT 1 FROM users WHERE email = 'lbrown@company.com');

-- Contract workers
INSERT INTO users (name, email) 
SELECT 'James Martinez', 'jmartinez@contractor.company.com'
WHERE NOT EXISTS (SELECT 1 FROM users WHERE email = 'jmartinez@contractor.company.com');

INSERT INTO users (name, email) 
SELECT 'Ana Patel', 'apatel@contractor.company.com'
WHERE NOT EXISTS (SELECT 1 FROM users WHERE email = 'apatel@contractor.company.com');

-- External partners
INSERT INTO users (name, email) 
SELECT 'Robert Taylor', 'rtaylor@partner.org'
WHERE NOT EXISTS (SELECT 1 FROM users WHERE email = 'rtaylor@partner.org');

INSERT INTO users (name, email) 
SELECT 'Maria Garcia', 'mgarcia@consultancy.com'
WHERE NOT EXISTS (SELECT 1 FROM users WHERE email = 'mgarcia@consultancy.com');
