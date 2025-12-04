-- =============================================================================
-- SCHOOL DATABASE SCHEMA AND DATA
-- Complete database schema, sample data, and analytical queries
-- =============================================================================

-- =============================================================================
-- SECTION 1: TABLE CREATION
-- =============================================================================

-- Students Table
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    birth_year INTEGER NOT NULL
);

-- Grades table
CREATE TABLE IF NOT EXISTS grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    subject TEXT NOT NULL,
    grade INTEGER NOT NULL CHECK (grade BETWEEN 1 AND 100),
    FOREIGN KEY (student_id) REFERENCES students(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- =============================================================================
-- SECTION 2: INDEXES FOR PERFORMANCE OPTIMIZATION
-- =============================================================================

-- Index for joining grades with students
CREATE INDEX IF NOT EXISTS idx_student_id ON grades(student_id);

-- Index for filtering and grouping grades by subject
CREATE INDEX IF NOT EXISTS idx_subject ON grades(subject);

-- Index for filtering students by birth year
CREATE INDEX IF NOT EXISTS idx_birth_year ON students(birth_year);

-- Index for filtering grades by grade value and range queries
CREATE INDEX IF NOT EXISTS idx_grade ON grades(grade);

-- =============================================================================
-- SECTION 3: SAMPLE DATA INSERTION
-- =============================================================================

-- Insert students
INSERT INTO students (full_name, birth_year) VALUES
    ('Alice Johnson', 2005),
    ('Brian Smith', 2004),
    ('Carla Reyes', 2006),
    ('Daniel Kim', 2005),
    ('Eva Thompson', 2003),
    ('Felix Nguyen', 2007),
    ('Grace Patel', 2005),
    ('Henry Lopez', 2004),
    ('Isabella Martínez', 2006);

-- Insert grades
INSERT INTO grades (student_id, subject, grade) VALUES
    (1, 'Math', 88),
    (1, 'English', 92),
    (1, 'Science', 85),
    (2, 'Math', 75),
    (2, 'History', 83),
    (2, 'English', 79),
    (3, 'Science', 95),
    (3, 'Math', 91),
    (3, 'Art', 89),
    (4, 'Math', 84),
    (4, 'Science', 88),
    (4, 'Physical Education', 93),
    (5, 'English', 90),
    (5, 'History', 85),
    (5, 'Math', 88),
    (6, 'Science', 72),
    (6, 'Math', 78),
    (6, 'English', 81),
    (7, 'Art', 94),
    (7, 'Science', 87),
    (7, 'Math', 90),
    (8, 'History', 77),
    (8, 'Math', 83),
    (8, 'Science', 80),
    (9, 'English', 96),
    (9, 'Math', 89),
    (9, 'Art', 92);

-- =============================================================================
-- SECTION 4: ANALYTICAL QUERIES
-- =============================================================================

-- Find all grades for Alice Johnson
SELECT s.full_name, g.subject, g.grade
FROM students s
JOIN grades g ON s.id = g.student_id
WHERE s.full_name = 'Alice Johnson'
ORDER BY g.subject;

-- Calculate average grade per student
SELECT s.id, s.full_name, ROUND(AVG(g.grade), 2) as average_grade
FROM students s
JOIN grades g ON s.id = g.student_id
GROUP BY s.id, s.full_name
ORDER BY average_grade DESC;

-- List all students born after 2004
SELECT id, full_name, birth_year
FROM students
WHERE birth_year > 2004
ORDER BY birth_year DESC;

-- List all subjects and their average grades
SELECT subject, ROUND(AVG(grade), 2) as average_grade
FROM grades
GROUP BY subject
ORDER BY average_grade DESC;

-- Find top 3 students with highest average grades
SELECT s.id, s.full_name, ROUND(AVG(g.grade), 2) as average_grade
FROM students s
JOIN grades g ON s.id = g.student_id
GROUP BY s.id, s.full_name
ORDER BY average_grade DESC
LIMIT 3;

-- Show all students who scored below 80 in any subject
SELECT DISTINCT s.id, s.full_name
FROM students s
JOIN grades g ON s.id = g.student_id
WHERE g.grade < 80
ORDER BY s.full_name;