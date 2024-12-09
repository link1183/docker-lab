CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY,
  name TEXT,
  email TEXT
);

-- Test users with various name patterns and email formats
INSERT INTO users (name, email) VALUES
  -- Standard format names
  ('Alice Smith', 'alice.smith@example.com'),
  ('Bob Johnson', 'bob.johnson@example.com'),
  ('Charlie Brown', 'charlie.brown@example.com'),
  
  -- Names with special characters
  ('María García', 'maria.garcia@example.com'),
  ('André Martin', 'andre.martin@example.com'),
  ('Søren Nielsen', 'soren.nielsen@example.com'),
  
  -- Different email formats
  ('John Doe', 'johndoe@example.com'),
  ('Jane Smith', 'j.smith@example.com'),
  ('Tom Wilson', 'tom.wilson.dev@example.com'),
  
  -- Short and long names
  ('Li Wei', 'li.wei@example.com'),
  ('Christopher Alexander Thompson', 'cat@example.com'),
  ('Mo Li', 'moli@example.com'),
  
  -- Names with hyphens and apostrophes
  ('Mary-Jane Parker', 'mjparker@example.com'),
  ('O''Connor Smith', 'oconnor.s@example.com'),
  ('Jean-Pierre Dubois', 'jp.dubois@example.com'),
  
  -- Different domain variations for testing
  ('Test Admin', 'admin@test.example.com'),
  ('Test User', 'user@test.example.com'),
  ('Dev Test', 'dev@staging.example.com'),
  
  -- Edge cases for testing
  ('Test Long Email', 'very.long.email.address.for.testing.purposes@example.com'),
  ('Test Uppercase', 'UPPERCASE.EMAIL@example.com'),
  
  -- Common name collisions for testing
  ('John Smith', 'john.smith.1@example.com'),
  ('John Smith', 'john.smith.2@example.com'),
  ('John Smith Jr', 'john.smith.jr@example.com'),
  
  -- Various cultural name formats
  ('Zhang Wei', 'zhang.wei@example.com'),
  ('Yuki Tanaka', 'yuki.tanaka@example.com'),
  ('Mohammed Ahmed', 'm.ahmed@example.com'),
  ('Vladimir Popov', 'v.popov@example.com'),
  ('Giuseppe Romano', 'g.romano@example.com'),
  
  -- Names with titles for edge case testing
  ('Dr. James Wilson', 'dr.wilson@example.com'),
  ('Prof. Sarah Connor', 'prof.connor@example.com'),
  
  -- Numbers in email addresses
  ('Test User 123', 'test123@example.com'),
  ('Dev User 456', 'dev456@example.com'),
  
  -- Mock service accounts for testing
  ('System Admin', 'system.admin@example.com'),
  ('No Reply', 'noreply@example.com'),
  ('Support Test', 'support@example.com'),
  
  -- Special case formatting
  ('Test Spaces', 'test.spaces@example.com'),
  ('Test.Dots', 'test.dots@example.com'),
  ('Test_Underscore', 'test_underscore@example.com'),
  
  -- Various length patterns
  ('A B', 'ab@example.com'),
  ('Test Middlename User', 'tmuser@example.com'),
  ('Supercalifragilisticexpialidocious User', 'super.user@example.com');
