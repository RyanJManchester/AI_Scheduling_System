insert into Inspector (name, email) values
    ('John Doe', 'JohnDoe@gmail.com'),
    ('Jane Smith', 'janesmith@gmail.com'),
    ('Michael Brown', 'michaelbrown@gmail.com'),
    ('Emily Clark', 'emilyclark@gmail.com'),
    ('Daniel Lee', 'daniellee@gmail.com');

INSERT INTO Qualification (code) VALUES 
    ('R1'),
    ('C1'),
    ('R2'),
    ('C2'),
    ('R3'),
    ('C3'),
    ('R4'),
    ('C4');

INSERT INTO Inspector_Qualification (inspector_id, qualification_code) VALUES 
    ((SELECT id FROM Inspector WHERE name = 'John Doe'), 'R1'),
    ((SELECT id FROM Inspector WHERE name = 'John Doe'), 'C1'),
    
    ((SELECT id FROM Inspector WHERE name = 'Jane Smith'), 'R2'),
    ((SELECT id FROM Inspector WHERE name = 'Jane Smith'), 'C2'),
    ((SELECT id FROM Inspector WHERE name = 'Jane Smith'), 'R1'),  
    ((SELECT id FROM Inspector WHERE name = 'Jane Smith'), 'C1'),

    ((SELECT id FROM Inspector WHERE name = 'Michael Brown'), 'R3'),
    ((SELECT id FROM Inspector WHERE name = 'Michael Brown'), 'C3'),
    ((SELECT id FROM Inspector WHERE name = 'Michael Brown'), 'R2'),  
    ((SELECT id FROM Inspector WHERE name = 'Michael Brown'), 'C2'),  
    ((SELECT id FROM Inspector WHERE name = 'Michael Brown'), 'R1'),  
    ((SELECT id FROM Inspector WHERE name = 'Michael Brown'), 'C1'),  
    
    ((SELECT id FROM Inspector WHERE name = 'Emily Clark'), 'R4'),
    ((SELECT id FROM Inspector WHERE name = 'Emily Clark'), 'C4'),
    ((SELECT id FROM Inspector WHERE name = 'Emily Clark'), 'R3'), 
    ((SELECT id FROM Inspector WHERE name = 'Emily Clark'), 'C3'), 
    ((SELECT id FROM Inspector WHERE name = 'Emily Clark'), 'R2'), 
    ((SELECT id FROM Inspector WHERE name = 'Emily Clark'), 'C2'), 
    ((SELECT id FROM Inspector WHERE name = 'Emily Clark'), 'R1'), 
    ((SELECT id FROM Inspector WHERE name = 'Emily Clark'), 'C1'), 
    
    ((SELECT id FROM Inspector WHERE name = 'Daniel Lee'), 'R2'),
    ((SELECT id FROM Inspector WHERE name = 'Daniel Lee'), 'C3'),
    ((SELECT id FROM Inspector WHERE name = 'Daniel Lee'), 'R1'),
    ((SELECT id FROM Inspector WHERE name = 'Daniel Lee'), 'C2'),
    ((SELECT id FROM Inspector WHERE name = 'Daniel Lee'), 'C1');


INSERT INTO Building_Consent (bc_number, level, location) VALUES 
    (1, 'R1', '1 Smith Street, Hamilton');

INSERT INTO Inspection (bc_number, description, date, time, inspector_id, status) VALUES 
    (1, 'INS01 Excavation, Siting, and Foundations', '2024-10-01', '10:00', (SELECT id FROM Inspector WHERE name = 'John Doe'), 'Failed'),
    (1, 'INS01 Excavation, Siting, and Foundations', NULL, NULL, NULL, NULL),
    (1, 'INS02 Sub-floor/Pre-floor', NULL, NULL, NULL, NULL),
    (1, 'INS03 Blocks, Beams, Columns and Tilt Slab', NULL, NULL, NULL, NULL),
    (1, 'INS04 Pre-wrap/Structural Framing', NULL, NULL, NULL, NULL),
    (1, 'INS05 Pre-line: Building and Plumbing – COMBINED', NULL, NULL, NULL, NULL),
    (1, 'INS07 Cladding', NULL, NULL, NULL, NULL),
    (1, 'INS09 Final Building', NULL, NULL, NULL, NULL)

