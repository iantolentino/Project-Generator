def calculate_tree_depth(line):
    for i, char in enumerate(line):
        if char in ['├', '└']:
            return i // 4 + 1
    if line.strip().startswith('│'):
        for i, char in enumerate(line):
            if char not in ['│', ' ']:
                return i // 4 + 1
    for i, char in enumerate(line):
        if char not in [' ', '│', '├', '└', '─']:
            return 0 if i == 0 else i // 4
    return 0

def extract_clean_name(line):
    cleaned = line.rstrip()
    name_start = 0
    while name_start < len(cleaned) and cleaned[name_start] in [' ', '│', '├', '└', '─']:
        name_start += 1
    if name_start >= len(cleaned):
        return ""
    return cleaned[name_start:].strip('─ ')

def parse_tree_structure(text_input):
    lines = [l for l in text_input.strip().split('\n') if l.strip()]
    
    root_line = lines[0]
    root_name = extract_clean_name(root_line).rstrip('/')
    
    if any(c in root_line for c in ['├', '└', '│']):
        root_name = "project"
        start_index = 0
    else:
        start_index = 1

    operations = [{
        'action': 'CREATE_FOLDER',
        'path': root_name,
        'depth': 0
    }]
    
    folder_stack = [(0, root_name)]
    
    for line in lines[start_index:]:
        depth = calculate_tree_depth(line)
        name = extract_clean_name(line)
        if not name:
            continue
        
        is_folder = name.endswith('/') or ('.' not in name.split('/')[-1])
        clean_name = name.rstrip('/')
        
        while folder_stack and folder_stack[-1][0] >= depth:
            folder_stack.pop()
        
        parent_path = folder_stack[-1][1] if folder_stack else root_name
        full_path = f"{parent_path}/{clean_name}"
        
        if is_folder:
            folder_stack.append((depth, full_path))
            
        operations.append({
            'action': 'CREATE_FOLDER' if is_folder else 'CREATE_FILE',
            'path': full_path
        })
    
    return root_name, operations

# Project structure templates
WEB_STRUCTURE = """
my-web-app/
├── src/
│   ├── components/
│   │   ├── Header/
│   │   │   ├── Header.jsx
│   │   │   └── Header.css
│   │   ├── Footer/
│   │   │   ├── Footer.jsx
│   │   │   └── Footer.css
│   │   └── Layout/
│   │       ├── Layout.jsx
│   │       └── Layout.css
│   ├── pages/
│   │   ├── Home/
│   │   │   ├── Home.jsx
│   │   │   └── Home.css
│   │   ├── About/
│   │   │   ├── About.jsx
│   │   │   └── About.css
│   │   └── Dashboard/
│   │       ├── Dashboard.jsx
│   │       └── Dashboard.css
│   ├── hooks/
│   │   ├── useAuth.js
│   │   └── useFetch.js
│   ├── services/
│   │   ├── api.js
│   │   └── auth.js
│   ├── utils/
│   │   ├── helpers.js
│   │   └── constants.js
│   ├── styles/
│   │   ├── global.css
│   │   └── variables.css
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
├── public/
│   ├── images/
│   │   └── logo.png
│   ├── fonts/
│   └── favicon.ico
├── server/
│   ├── routes/
│   │   ├── api.js
│   │   └── auth.js
│   ├── controllers/
│   │   ├── userController.js
│   │   └── dataController.js
│   ├── models/
│   │   ├── User.js
│   │   └── Data.js
│   ├── middleware/
│   │   ├── auth.js
│   │   └── validation.js
│   ├── config/
│   │   ├── database.js
│   │   └── environment.js
│   └── index.js
├── tests/
│   ├── unit/
│   │   └── example.test.js
│   ├── integration/
│   │   └── api.test.js
│   └── setup.js
├── docker-compose.yml
├── Dockerfile
├── .env.example
├── .gitignore
├── package.json
└── README.md
"""

DESKTOP_STRUCTURE = """
my-desktop-app/
├── src/
│   ├── main/
│   │   ├── main.js
│   │   ├── preload.js
│   │   └── ipc.js
│   ├── renderer/
│   │   ├── components/
│   │   │   ├── Sidebar/
│   │   │   │   ├── Sidebar.jsx
│   │   │   │   └── Sidebar.css
│   │   │   ├── Header/
│   │   │   │   ├── Header.jsx
│   │   │   │   └── Header.css
│   │   │   └── Modal/
│   │   │       ├── Modal.jsx
│   │   │       └── Modal.css
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   └── Settings.jsx
│   │   ├── styles/
│   │   │   ├── global.css
│   │   │   └── theme.css
│   │   ├── App.jsx
│   │   └── index.html
│   └── shared/
│       ├── constants.js
│       └── utils.js
├── assets/
│   ├── icons/
│   │   └── app-icon.png
│   └── fonts/
├── database/
│   ├── migrations/
│   └── models/
│       └── schema.js
├── build/
│   └── installer.js
├── package.json
├── electron-builder.yml
├── .env.example
├── .gitignore
└── README.md
"""

HYBRID_STRUCTURE = """
my-hybrid-app/
├── src-tauri/
│   ├── src/
│   │   ├── main.rs
│   │   ├── lib.rs
│   │   └── commands.rs
│   ├── icons/
│   │   └── app-icon.png
│   ├── Cargo.toml
│   ├── build.rs
│   └── tauri.conf.json
├── src/
│   ├── components/
│   │   ├── Header.tsx
│   │   ├── Footer.tsx
│   │   └── Sidebar.tsx
│   ├── pages/
│   │   ├── Home.tsx
│   │   └── Dashboard.tsx
│   ├── hooks/
│   │   ├── useTauri.ts
│   │   └── useStore.ts
│   ├── services/
│   │   └── api.ts
│   ├── styles/
│   │   ├── global.css
│   │   └── variables.css
│   ├── App.tsx
│   ├── main.tsx
│   └── vite-env.d.ts
├── public/
│   └── assets/
├── package.json
├── tsconfig.json
├── vite.config.ts
├── .env.example
└── README.md
"""

STRUCTURE_TEMPLATES = {
    "Web": WEB_STRUCTURE,
    "Desktop": DESKTOP_STRUCTURE,
    "Hybrid": HYBRID_STRUCTURE
}