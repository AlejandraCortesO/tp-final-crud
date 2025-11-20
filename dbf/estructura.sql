CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL CHECK(precio >= 0),
    stock INTEGER NOT NULL CHECK(stock >= 0)
);

INSERT INTO productos (nombre, precio, stock) VALUES
    ('Laptop Dell', 45000.50, 10),
    ('Mouse Logitech', 1500.00, 25),
    ('Teclado Mecánico', 8500.00, 15);
