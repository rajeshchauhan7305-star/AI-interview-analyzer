USE ai_interview;

INSERT INTO interview_categories (name, description) VALUES
('Software Developer', 'Technical interviews for software engineering roles'),
('Python Developer', 'Python-specific programming and systems interviews'),
('Web Developer', 'Frontend and backend web development questions'),
('Data Analyst', 'Data analysis and SQL-based interview questions'),
('AI Engineer', 'AI, ML and model deployment interview questions');

INSERT INTO questions (category_id, difficulty, text, answer) VALUES
(1, 'Easy', 'Explain the difference between a list and a tuple in Python.', 'Lists are mutable and tuples are immutable.'),
(1, 'Medium', 'How do you handle concurrency in a web application?', 'Use locks, queues, and async patterns to manage concurrency.'),
(2, 'Easy', 'What is a decorator in Python?', 'A decorator wraps a function to extend its behavior.'),
(3, 'Medium', 'What is responsive design and why is it important?', 'Responsive design adapts layouts to different screen sizes.'),
(5, 'Hard', 'Describe the main components of a transformer model.', 'A transformer uses attention, encoder-decoder stacks, and positional encoding.');

INSERT INTO admins (email, full_name, hashed_password) VALUES
('admin@aiinterview.com', 'Platform Admin', '$2b$12$N1nv5KjQKoNqqZ2DQl7Cu.eI2s5Ig6xl0xTG1Y6eU1O0dm7YJ8lBe');
