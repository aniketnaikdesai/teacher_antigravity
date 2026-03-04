---
description: Environment setup rule for project folders
---

# Environment Setup Rule

This project follows the rule that **every folder must have its own virtual environment (`venv`)**.

## Steps to Follow

1.  **Initialize Git** (if not already done):
    ```bash
    git init
    ```

2.  **Create Virtual Environment**:
    ```bash
    python3 -m venv venv
    ```

3.  **Create `.gitignore`**:
    Ensure `venv/` is added to the `.gitignore` to avoid committing the environment.

4.  **Activate Environment**:
    - macOS/Linux: `source venv/bin/activate`
    - Windows: `.\venv\Scripts\activate`
