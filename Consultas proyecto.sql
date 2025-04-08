-- Mostrar las tablas de una base de datos
SHOW TABLES;

-- Recuperar cantidad de columnas de una tabla
SELECT COUNT(*) AS CANTIDAD_CAMPOS FROM Information_Schema.Columns WHERE Table_Name = "clientes" GROUP BY Table_Name;

-- Recuperar el nombre de las columnas de una tabla
SELECT COLUMN_NAME FROM Information_Schema.Columns WHERE Table_Name = "clientes";
