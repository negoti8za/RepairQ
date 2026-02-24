# RepairQ Fork Modernization Instructions (Claude Code)

This file is a **developer prompt template** for Claude Code.  
Use it to guide the AI in refactoring, modernizing, and improving the RepairQ Java desktop app.

---

## 1️⃣ Project Overview

- Legacy codebase: Java + Swing, Maven, Eclipse project.
- Goal: Modern Windows desktop app.
- Stack upgrade target:
  - **Java 21 (LTS)**
  - **JavaFX** UI
  - **SQLite** database
  - **jpackage** installer for native Windows `.exe`
- Project should remain:
  - Local-first
  - Offline-capable
  - Minimal dependencies
  - Secure and maintainable

---

## 2️⃣ Development Philosophy (Guidelines for Refactoring)

- **Simplicity:** Write clear, straightforward code. Avoid cleverness.  
- **Readability:** Make all code easy to understand.  
- **Performance:** Only optimize when necessary; don’t sacrifice clarity.  
- **Maintainability:** Modular, well-organized, easy-to-update code.  
- **Testability:** Business logic should be testable in isolation.  
- **Reusability:** Create reusable components/functions.  
- **Minimal Code:** Less code = less technical debt.  
- **Coding Best Practices:**
  - Use **early returns** to reduce nested conditions.
  - Use **descriptive names**, prefix handlers with `handle`.
  - Prefer **constants over functions** for static values.
  - Follow **DRY** principles; extract shared logic.
  - Prefer **functional and immutable approaches** when clear.
  - Make **minimal changes** per task.
  - Order functions so that composing functions appear before components.
  - Use `TODO:` comments for unresolved issues.
- **File Organization:** Keep a balanced, simple structure. Avoid over-engineering.

---

## 3️⃣ Modernization Plan (Actionable Steps)

1. **Stabilize Legacy App**
   - Compile and run current Swing-based RepairQ.
   - Identify all core business logic and database interactions.
   - Add minimal tests to verify existing functionality.

2. **Refactor Architecture**
   - Separate into clear layers:
     - `ui` → JavaFX components only handle display/events.
     - `controller` → Bridges UI and business logic.
     - `service` → Encapsulates all business rules.
     - `repository` → Handles SQLite DB access.
     - `config` → Settings and constants.
   - Remove tightly coupled code.

3. **Upgrade Java & Dependencies**
   - Upgrade to **Java 21 LTS**.
   - Update Maven dependencies.
   - Remove deprecated libraries.
   - Ensure compatibility with JavaFX.

4. **Migrate UI Gradually**
   - Replace Swing screens one at a time with JavaFX.
   - Apply modern UI styling (JavaFX CSS, FlatLaf optional).
   - Maintain current functionality while migrating.

5. **Database**
   - Replace legacy DB with **SQLite** if not already used.
   - Ensure schema supports tickets, users, devices, invoices.
   - Keep DB interactions isolated in `repository` layer.

6. **First-Time Setup / Admin**
   - On first launch:
     - Auto-create **default admin user**:
       - Username: `admin`
       - Password: `admin`
     - Prompt admin to **change password immediately**.
     - Force password change before any other actions.
   - Allow creation of additional users with roles:
     - Admin (full access)
     - Staff / Technician (restricted access)
   - Passwords should be securely hashed (BCrypt or equivalent).

7. **Branding & Invoice Customization**
   - Add ability to **upload a custom logo** for the business.
   - Logo should appear on:
     - Main dashboard
     - Printed / PDF invoices
   - Allow **invoice customization**:
     - Company name, address, contact info
     - Footer text
     - Optional logo inclusion
   - Store branding settings in configuration table in SQLite.

8. **Packaging**
   - Use **jpackage** to create native Windows installer.
   - Bundle Java runtime.
   - Ensure `.exe` runs offline without external Java.

9. **Security**
   - Hash passwords.
   - No hardcoded credentials beyond first-time `admin/admin`.
   - Minimize network exposure.
   - Keep dependencies up-to-date (Dependabot already present).

10. **Testing**
    - Build test environments for critical components.
    - Run frequent functional tests during migration.
    - Validate realistic input and output.

11. **Iterative Approach**
    - Only modify code relevant to the current step.
    - Verify functionality after each change.
    - Remove deprecated/unused legacy code gradually.

---

## 4️⃣ Claude Code Instructions

- Treat **RepairQ repo root** as working directory.
- Follow the modernization plan **step-by-step**, in order.
- Always separate **UI, service, and repository layers**.
- Suggest **refactorings that maintain functionality**.
- For UI screens: **suggest JavaFX replacements**, preserving layout and logic.
- For database: **ensure SQLite migration works seamlessly**.
- Include **first-time setup with admin user**, password change flow, and user management.
- Include **business branding support** (logo upload + invoice customization).
- Package instructions: **show jpackage command for Windows .exe**.
- Provide **clean, testable code examples** where possible.
- Use **TODO:** for any complex refactor that needs human review.

---

## 5️⃣ Goal for Claude

Produce a **stable, modern Windows desktop app** that:

- Uses **Java 21 + JavaFX + SQLite + jpackage**.
- Has a **clean layered architecture**.
- Supports **tickets, devices, users, invoices**.
- Includes **first-time admin setup**, **user management**, and **branding/invoice customization**.
- Is **offline-first, easy to install, maintainable, and secure**.
- Can be **incrementally refactored** from the existing Swing app.