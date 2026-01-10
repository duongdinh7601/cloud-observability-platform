# Scripts

The `scripts/` folder contains utility scripts for the Cloud Observability Platform.  
These scripts support setup, database seeding, and automation tasks for development and testing.

---

## Responsibilities

- Initialize or seed databases  
- Automate repetitive tasks for development  
- Provide helper scripts for service setup and testing  
- Support CI/CD workflows (optional in future)  

---

## Folder Structure

scripts/

├── .gitkeep # Placeholder file to keep folder tracked by Git

├── setup_db.sh # Script to initialize or reset the database

├── seed_logs.py # Script to seed the database with example logs

└── utils.py # Utility functions used by scripts

---

## Usage Examples

### 1. Database Setup
```bash
cd scripts
./setup_db.sh
```
### 2. Seed Example Logs
```bash
python seed_logs.py
```

---

## Notes

- Scripts are intended for **deployment and testing** only
- Use meaningful filenames and document each script as the folder grows
- Scripts should be **idempotent** where possible, so repeated execution doesn't break anything
- Optional: Add scripts for CI/CD piplines in the future
