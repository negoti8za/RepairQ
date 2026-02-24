# RepairQ Modernization Project

This repository contains the modernized version of the RepairQ Java desktop application, upgraded to use Java 21, JavaFX, and SQLite.

## Project Status

### Completed Tasks
1. **Project Analysis and Preparation** - Analyzed existing Swing-based codebase
2. **First-Time Setup Module** - Implemented auto-creation of admin user and password management
3. **Database Migration** - Migrated from MySQL to SQLite
4. **Security Implementation** - Added BCrypt password hashing

### In Progress Tasks
- **UI Migration** - Gradual migration from Swing to JavaFX
- **Layered Architecture** - Refactoring into clean architectural layers

## Architecture Overview

### Current Layers
- `ui` - UI components (Swing temporarily, JavaFX planned)
- `controller` - Handles user interactions
- `service` - Business logic
- `repository` - Database access
- `config` - Application settings and configuration
- `util` - Utility classes

### Key Features Implemented
1. **First-Time Setup**
   - Auto-creates default admin user (`admin`/`admin`)
   - Forces password change on first login
   - Supports additional user roles (Admin, Staff/Technician)

2. **Security**
   - Passwords are hashed using BCrypt
   - Secure credential handling

3. **Database**
   - Migrated from MySQL to SQLite
   - Schema management with Hibernate

4. **Branding and Invoice Customization**
   - Logo upload capability
   - Customizable invoice fields
   - Company information management

## Technology Stack

- **Java**: 21 LTS
- **UI Framework**: JavaFX (planned migration)
- **Database**: SQLite
- **ORM**: Hibernate JPA
- **Security**: BCrypt password hashing
- **Build Tool**: Maven

## Getting Started

### Quick Start (Windows Desktop)

**Requirements**: Java 21 LTS installed and in PATH

```cmd
REM Run the application
RepairQ-Run.bat

REM Or manually:
java -Xmx512m -jar RepairQ-0.0.1-SNAPSHOT.jar
```

> ⚠️ **Note**: JavaFX requires native libraries. See [WINDOWS-DEPLOYMENT.md](WINDOWS-DEPLOYMENT.md) for solutions if you get "JavaFX runtime components missing" error.

### Building from Source

```bash
# Clone the repository
git clone https://github.com/negoti8za/RepairQ.git
cd RepairQ

# Build with Maven
mvn clean package

# Run the application (requires JavaFX SDK setup)
java -Xmx512m \
  --add-modules javafx.controls,javafx.fxml \
  --module-path /path/to/javafx-sdk-21/lib \
  -jar target/RepairQ-0.0.1-SNAPSHOT.jar

# Or use the batch launcher
RepairQ-Run.bat
```

### Deployment Guide

For detailed deployment instructions, including:
- Running with existing Java installation
- Setting up JavaFX SDK
- Building native Windows installers
- jpackage configuration

👉 See: [WINDOWS-DEPLOYMENT.md](WINDOWS-DEPLOYMENT.md)

## Next Steps

1. Complete migration to JavaFX UI components
2. Implement full user management features
3. Add invoice generation functionality
4. Create native Windows installers with jpackage
5. Add comprehensive testing
