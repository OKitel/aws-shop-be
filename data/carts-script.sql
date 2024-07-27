INSERT INTO carts (user_id, created_at, updated_at, status) values
('d37ccb1a-0fff-47fa-a392-261b5cf61198', CURRENT_DATE, CURRENT_DATE, 'OPEN'),
('9323e628-fb8f-4423-ba1d-659840ee9383', CURRENT_DATE, CURRENT_DATE, 'ORDERED')

INSERT INTO cart_items (cart_id, product_id, count) VALUES
('8349093d-a25d-4709-a263-59b66cebb156', '90dd4c59-59c7-4a55-b0e9-ff53669a9d77', 1), -- Ticket to Ride
('8349093d-a25d-4709-a263-59b66cebb156', '6b72c7bd-2583-4b96-949f-82339d157821', 2), -- Wingspan
('9d3a1e9b-8056-4c03-9e45-ec58600310ff', 'cbdc0fdc-9ef3-4674-8e48-4a7bb7d11b2d', 1), -- Everdell
('9d3a1e9b-8056-4c03-9e45-ec58600310ff', '6d410df3-e513-4c26-9695-6c6691fbe8f7', 1), -- Terraforming Mars
('9d3a1e9b-8056-4c03-9e45-ec58600310ff', 'b5e12977-2353-4d49-836f-b4c354f55aea', 3) -- Carcassonne