# Project Generator

A CLI and web-based tool that instantly scaffolds full-stack projects with proper folder structures, starter code, and configuration files. Supports Web, Desktop, and Hybrid platforms.

## Features

- Interactive CLI with questionary prompts
- Web UI accessible at http://localhost:8000
- REST API for curl/direct HTTP requests
- Generates complete folder structures for Web, Desktop, and Hybrid apps
- Creates starter code with working components, pages, hooks, services
- Backend server boilerplate with Express routes, controllers, models, middleware
- Docker and docker-compose configuration
- Environment variable management with .env.example
- Git initialization with .gitignore
- Jinja2 template support for custom project templates
- Color palette integration into generated CSS

## Installation

pip install -e .

## Usage

### CLI Mode
project-gen

### Web Server Mode
project-gen-server
Then open http://localhost:8000 in your browser

### API Mode (curl)
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"platform":"Web","category":"E-commerce","project_name":"my-shop"}' \
  -o my-shop.zip

### Direct Python Run (no install)
pip install -r requirements.txt
python -m project_gen.cli
python -m project_gen.server

## Project Structure

```
Project-Generator/
├── project_gen/
│   ├── templates/              # Jinja2 templates for generated projects
│   │   └── web/                # Web platform templates
│   │       ├── docker-compose.yml.j2
│   │       ├── Dockerfile.j2
│   │       └── README.md.j2
│   ├── web_templates/          # Templates for the web UI
│   │   └── form.html
│   ├── __init__.py
│   ├── cli.py                  # CLI entry point
│   ├── generator.py            # Core generation logic
│   ├── prompts.py              # Interactive prompts
│   ├── utils.py                # File writing and git utilities
│   ├── server.py               # FastAPI web server
│   └── structure_maker.py      # Folder structure definitions and parser
├── README.md
├── requirements.txt
└── setup.py
```

## Supported Platforms and Stacks

### Web
- E-commerce: Next.js + PostgreSQL + Prisma
- Streaming platform: React + Node.js + MongoDB + Mongoose
- Social media app: Django + PostgreSQL + Django ORM
- Default: React + Express + SQLite

### Desktop
- Default: Electron + SQLite + Sequelize

### Hybrid
- Default: Tauri + SQLite + Diesel

## Generated Project Structure (Web)

```
project-name/
├── index.html                  # Entry HTML with root div
├── vite.config.js              # Vite configuration with API proxy
├── package.json                # Dependencies (React, Vite, React Router)
├── docker-compose.yml          # Docker compose for app
├── Dockerfile                  # Docker build instructions
├── .env.example                # Environment variable template
├── .gitignore                  # Git ignore rules
├── README.md                   # Project documentation
├── src/
│   ├── main.jsx                # React entry point
│   ├── App.jsx                 # Main app component with counter demo
│   ├── index.css               # Global styles with CSS reset
│   ├── components/
│   │   ├── Header/
│   │   │   ├── Header.jsx      # Header component
│   │   │   └── Header.css      # Header styles with user's primary color
│   │   ├── Footer/
│   │   │   ├── Footer.jsx      # Footer component
│   │   │   └── Footer.css      # Footer styles
│   │   └── Layout/
│   │       ├── Layout.jsx      # Layout wrapper with Header and Footer
│   │       └── Layout.css      # Layout flexbox styles
│   ├── pages/
│   │   ├── Home/
│   │   │   ├── Home.jsx        # Home page with API data fetching
│   │   │   └── Home.css        # Home page styles
│   │   └── About/
│   │       ├── About.jsx       # About page with tech stack info
│   │       └── About.css       # About page styles
│   ├── hooks/
│   │   ├── useAuth.js          # Authentication hook (login/logout)
│   │   └── useFetch.js         # Data fetching hook
│   ├── services/
│   │   ├── api.js              # API service functions
│   │   └── auth.js             # Auth service (login/register)
│   ├── utils/
│   │   ├── helpers.js          # Utility functions
│   │   └── constants.js        # App constants
│   └── styles/
│       ├── global.css          # Global app styles
│       └── variables.css       # CSS custom properties with user colors
├── server/
│   ├── index.js                # Express server with CORS and JSON parsing
│   ├── package.json            # Server dependencies (Express, CORS)
│   ├── routes/
│   │   ├── api.js              # API routes
│   │   └── auth.js             # Auth routes (login/register)
│   ├── controllers/
│   │   ├── userController.js   # User CRUD operations
│   │   └── dataController.js   # Data CRUD operations
│   ├── models/
│   │   ├── User.js             # User model class
│   │   └── Data.js             # Data model class
│   ├── middleware/
│   │   ├── auth.js             # Authentication middleware
│   │   └── validation.js       # Input validation middleware
│   └── config/
│       ├── database.js         # Database configuration
│       └── environment.js      # Environment configuration
└── tests/
    ├── unit/
    │   └── example.test.js     # Unit test example
    ├── integration/
    │   └── api.test.js         # API integration test example
    └── setup.js                # Test setup with fetch mock
```

## Core Files Explained

### cli.py
Entry point for CLI. Calls prompts.py to gather options, then generator.py to create project.

### prompts.py
Interactive questionary prompts for platform, category, colors, style, and scope selection.

### generator.py
Main generation logic:
- suggest_stack() maps platform+category to framework+database+ORM
- create_structure_from_template() creates folder structure from tree definitions
- write_starter_files() generates all source code files with proper content
- generate_project() orchestrates the entire process
- Handles template rendering with Jinja2
- Creates config files (Dockerfile, docker-compose.yml, .env.example, .gitignore, README.md, package.json)

### server.py
FastAPI web server with:
- GET / : HTML form for web UI
- POST /generate : JSON API that returns ZIP file
- POST /generate-form : Form submission that returns ZIP file

### structure_maker.py
- Defines folder tree structures for Web, Desktop, and Hybrid platforms
- parse_tree_structure() parses ASCII tree diagrams into operations list
- calculate_tree_depth() determines nesting level from tree characters
- extract_clean_name() extracts file/folder names from tree lines

### utils.py
- write_file() handles file writing with retry logic for Windows file locks
- init_git_repo() initializes git and creates .gitignore

## How to Add New Templates

1. Add a new entry in CATEGORY_STACK dictionary in generator.py
2. Create template files in project_gen/templates/{platform}/
3. Use .j2 extension for Jinja2 template files
4. Template variables available: project_name, platform, category, colors, style, scope, framework, database, orm

Example template (docker-compose.yml.j2):
version: '3.8'
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - APP_NAME={{ project_name }}

## How to Add New Platform Structures

1. Add a new structure tree in structure_maker.py
2. Use ASCII tree format with / for folders
3. Add to STRUCTURE_TEMPLATES dictionary
4. Add starter code generation in write_starter_files() function in generator.py

## How to Add New Prompts

1. Add new options in prompts.py (lists PLATFORMS, CATEGORIES, STYLES, SCOPES)
2. Add new questionary prompts in gather_project_options()
3. Update the context dictionary in generator.py
4. Use the new variables in templates with {{ variable_name }}

## Dependencies

- questionary: Interactive CLI prompts
- Jinja2: Template rendering
- colorama: Terminal colors
- pyyaml: YAML support
- fastapi: Web server framework
- uvicorn: ASGI server
- python-multipart: Form data parsing
- pydantic: Data validation

## API Reference

### POST /generate

Request body:
{
  "platform": "Web",
  "category": "E-commerce",
  "colors": ["#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6"],
  "style": "Modern",
  "scope": "Scalable app",
  "project_name": "my-project"
}

Response: ZIP file download

### POST /generate-form

Form fields: platform, category, colors, style, scope, project_name
Response: ZIP file download

## Troubleshooting

### Permission denied on Windows
- Close any programs that might have the generated folder open
- Delete the project folder manually before regenerating
- Run terminal as Administrator

### project-gen command not found
- Add Python Scripts folder to PATH: C:\Users\USER\AppData\Roaming\Python\Python314\Scripts
- Or run directly: python -m project_gen.cli

### Templates not rendering
- Ensure template files have .j2 extension
- Check that folder structure exists: project_gen/templates/{platform}/
- Verify Jinja2 syntax in templates

### Localhost not working after generation
- Run npm install in project root
- Run cd server && npm install
- Start server: cd server && npm start
- Start frontend: npm run dev
- Open http://localhost:3000

## Security Notes

- Generated .env.example files contain placeholder values
- SECRET_KEY is set to "change_this_to_random_string"
- Database passwords default to "change_me"
- Users must change all values before deploying
- .env is added to .gitignore to prevent committing secrets

## Future Improvements

- Add more platform templates (Mobile, CLI tools, Libraries)
- Add database migration files
- Add authentication boilerplate (JWT, OAuth)
- Add testing frameworks setup (Jest, Vitest)
- Add CI/CD pipeline templates
- Add TypeScript option for all platforms
- Add more ORM options
- Add API documentation generation
- Add storybook setup for components
- Add i18n internationalization setup
