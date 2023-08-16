# mockPy

mockPy is a utility for quickly creating and simulating API endpoints for development and testing purposes. 
It allows you to configure API routes, responses, and behaviours using YAML configuration files.

## Features

- Easy configuration using YAML files.
- Simulate various HTTP methods (GET, POST, PUT, DELETE, etc.).
- Supports dynamic response generation.

## Installation 

1. Install dependencies
   ```bash
     pip install -f requirements.txt
   ```
2. Configure: Update the file present in resources/api.yaml
3. To create a new domain / api-resource
4. Update the yaml add under domains section
5. ```yaml
   - book:
      schema: { id: "string", name: "string" }
      resource_identifier: [id, name]
      uuid: id
      expose: [GET, PUT]
      slug: /books
      id: "book_id"
   ```
6. 
   


