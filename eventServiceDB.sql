CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    location VARCHAR(255) NOT NULL,
    date TIMESTAMP DEFAULT NOW(),
    num_tickets INT NOT NULL DEFAULT 100,  -- Default 100 tickets available
    ticket_price FLOAT NOT NULL DEFAULT 50.0  -- Default price per ticket is 50.0
);

INSERT INTO events (title, description, location, date, num_tickets, ticket_price) 
VALUES (
    'Music Festival 2025', 
    'A grand music festival with top artists.', 
    'Los Angeles', 
    '2025-07-20 18:00:00', 
    500,  -- Total available tickets
    100.00  -- Price per ticket
);

select * from events;
