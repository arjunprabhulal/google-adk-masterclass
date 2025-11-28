# 14. MCP Toolbox for Databases - PostgreSQL

Connect ADK agents to PostgreSQL databases using MCP Toolbox for enterprise-grade data access.

**Blog Post:** [https://arjunprabhulal.com/adk-mcp-toolbox/](https://arjunprabhulal.com/adk-mcp-toolbox/)

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Setup Steps](#setup-steps)
4. [Running the Agent](#running-the-agent)
5. [Example Queries](#example-queries)
6. [Next Steps](#next-steps)

## Overview

MCP Toolbox for Databases provides:

- **Connection pooling** - Efficient database connections
- **Parameterized queries** - Secure query execution
- **Authentication** - Secure credential handling
- **Observability** - Built-in OpenTelemetry support

## Prerequisites

- Python 3.10+
- PostgreSQL 12+ (local or remote)
- Gemini API key from [AI Studio](https://aistudio.google.com/apikey)
- MCP Toolbox server ([installation guide](https://github.com/googleapis/genai-toolbox/releases))

## Setup Steps

1. Navigate to this module:

```bash
cd 14-mcp-toolbox
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install google-adk toolbox-core python-dotenv
```

4. Install MCP Toolbox Server:

```bash
# macOS/Linux via Homebrew
brew install mcp-toolbox

# Or download binary directly (macOS Apple Silicon)
export VERSION=0.21.0
curl -L -o toolbox https://storage.googleapis.com/genai-toolbox/v$VERSION/darwin/arm64/toolbox
chmod +x toolbox
```

5. Set up PostgreSQL with sample data:

```sql
CREATE DATABASE ecommerce_db;
\c ecommerce_db

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    price DECIMAL(10,2),
    stock_quantity INTEGER
);

INSERT INTO products (name, category, price, stock_quantity) VALUES
    ('Laptop Pro', 'Electronics', 1299.99, 50),
    ('Wireless Mouse', 'Electronics', 29.99, 200),
    ('Office Chair', 'Furniture', 399.99, 30);
```

6. The `tools.yaml` file is already included. It defines database tools:

```yaml
sources:
  ecommerce_db:
    kind: postgres
    host: localhost
    port: 5432
    database: ecommerce_db
    user: postgres
    password: postgres

tools:
  get_products:
    kind: postgres-sql
    source: ecommerce_db
    description: "Retrieve all products"
    statement: SELECT * FROM products ORDER BY name

toolsets:
  ecommerce:
    - get_products
    - search_products
    - get_customers
    - get_inventory_value
```

7. Set up environment variables in `postgres_agent/.env`:

```
GOOGLE_API_KEY=your-api-key-here
TOOLBOX_URL=http://localhost:5050
```

## Running the Agent

### Terminal 1: Start Toolbox Server

```bash
toolbox --tools-file tools.yaml --port 5050
```

### Terminal 2: Start ADK Agent

```bash
source .venv/bin/activate
adk web
```

> **Note (macOS):** Port 5000 is used by AirPlay Receiver. Always use port 5050 or higher.

Open http://127.0.0.1:8000 in your browser.

## Example Queries

- "What products do we have in inventory?"
- "Show me all electronics products"
- "What's the total value of our inventory?"

## Next Steps

Continue to [15. Model Context Protocol (MCP)](../15-mcp-deep-dive/)
