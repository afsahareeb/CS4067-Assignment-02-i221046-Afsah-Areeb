-- Event table
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    location VARCHAR(255) NOT NULL,
    date TIMESTAMP DEFAULT NOW(),
    organizer_id INTEGER REFERENCES users(id) ON DELETE CASCADE
);
-- Attendece of event
CREATE TABLE event_attendees (
    id SERIAL PRIMARY KEY,
    event_id INTEGER REFERENCES events(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    registered_at TIMESTAMP DEFAULT NOW()
);
-- Event review
CREATE TABLE event_reviews (
    id SERIAL PRIMARY KEY,
    event_id INTEGER REFERENCES events(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    review TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO events (title, description, location, date, organizer_id) 
VALUES ('Tech Conference 2025', 'A conference on the latest technology trends.', 'Islamabad', '2025-06-15 10:00:00', 1);

select * from events

ALTER TABLE users ADD COLUMN balance FLOAT DEFAULT 100.0;

CREATE TABLE bookings (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    event_id INT NOT NULL,
    tickets INT NOT NULL,
    total_price FLOAT NOT NULL,
    status VARCHAR(50) DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
);

-- ✅ Add columns for ticket count and price per ticket
ALTER TABLE events 
ADD COLUMN num_tickets INT NOT NULL DEFAULT 100,  -- Default 100 tickets available
ADD COLUMN ticket_price FLOAT NOT NULL DEFAULT 50.0;  -- Default price per ticket is 50.0

-- ✅ Set a default value for organizer_id to 0
ALTER TABLE events 
ALTER COLUMN organizer_id SET DEFAULT 0;
