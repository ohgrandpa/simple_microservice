
def create_tables():
    tables = list()

    # Company table
    tables.append({"name": "companies",
                   "sql": """
      CREATE TABLE IF NOT EXISTS companies (
      id INTEGER PRIMARY KEY,
      name TEXT NOT NULL)"""})

    # Customers table
    tables.append({"name": "customers",
                   "sql": """CREATE TABLE IF NOT EXISTS customers (
      id INTEGER PRIMARY KEY,
      company_id INTEGER,
      first_name TEXT NULL,
      last_name TEXT NULL,
      FOREIGN KEY (company_id)
        REFERENCES companies (id)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION)"""})

    # Products table
    tables.append({"name": "products",
                   "sql": """
      CREATE TABLE IF NOT EXISTS `products` (
      id INTEGER,
      name TEXT NULL,
      price TEXT NULL,
      PRIMARY KEY (id))"""})

    # Customer_orders association table
    tables.append({"name": "customer_orders",
                  "sql": """
    CREATE TABLE IF NOT EXISTS `customer_orders` (
      `customer_id` INTEGER,
      `product_id` INTEGER,
      `quantity` INTEGER NULL,
    PRIMARY KEY (customer_id, product_id)
        FOREIGN KEY (`customer_id`)
        REFERENCES `customers` (`id`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION,
      CONSTRAINT `product_id`
        FOREIGN KEY (`product_id`)
        REFERENCES `products` (`id`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION)"""})

    return tables
