insert into Inspector (name, email) values
    ('John Doe', 'JohnDoe@gmail.com', 'R1', 'C1'),
    ('Jane Smith', 'janesmith@gmail.com', 'R2', 'C2'),
    ('Michael Brown', 'michaelbrown@gmail.com', 'R3', 'C3'),
    ('Emily Clark', 'emilyclark@gmail.com', 'R4', 'C4'),
    ('Daniel Lee', 'daniellee@gmail.com', 'R2', 'C3');


INSERT INTO Building_Consent (bc_number, level, location) VALUES 
    (1, 'R1', '1 Smith Street, Hamilton');

INSERT INTO Inspection (bc_number, description, date, start_time, end_time, inspector_id, status, order) VALUES 
    (1, 'INS01 Excavation, Siting, and Foundations', '2024-10-01', '10:00', '12:00',(SELECT id FROM Inspector WHERE name = 'John Doe'), 'Failed', 10),
    (1, 'INS01 Excavation, Siting, and Foundations', NULL, NULL, NULL, NULL, 11),
    (1, 'INS02 Sub-floor/Pre-floor', NULL, NULL, NULL, NULL, 20),
    (1, 'INS03 Blocks, Beams, Columns and Tilt Slab', NULL, NULL, NULL, NULL, 30),
    (1, 'INS04 Pre-wrap/Structural Framing', NULL, NULL, NULL, NULL, 40),
    (1, 'INS05 Pre-line: Building and Plumbing – COMBINED', NULL, NULL, NULL, NULL, 50),
    (1, 'INS07 Cladding', NULL, NULL, NULL, NULL, 60),
    (1, 'INS09 Final Building', NULL, NULL, NULL, NULL, 70)

