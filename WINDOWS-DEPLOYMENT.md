# RepairQ - Windows Distribution Guide

## Quick Start

### Requirements
- **Java 21 LTS** or later installed on your system
  - Download from: [Oracle JDK](https://www.oracle.com/java/technologies/downloads/) or [Adoptium](https://adoptium.net/)
  - Verify installation: `java -version` (should show Java 21 or later)

###  Running RepairQ

#### Option 1: Using the Batch Launcher (Easiest if JavaFX is available)
1. Ensure Java 21 is installed and in your PATH
2. Run: `RepairQ-Run.bat`
3. The application should start

#### Option 2: Manual Command Line (For troubleshooting)
```cmd
java -Xmx512m -jar RepairQ-0.0.1-SNAPSHOT.jar
```

---

## Troubleshooting

### ❌ Error: "JavaFX runtime components are missing"

This occurs because JavaFX requires native libraries (.dll files) that must be:
1. **Installed separately**, OR
2. **Bundled with a custom Java runtime**

### Solution A: Download JavaFX SDK and Set JAVAFX_HOME

1. **Download JavaFX SDK 21**
   - Visit: https://gluonhq.com/products/javafx/
   - Select: "JavaFX SDK 21" → "Windows" → Download

2. **Extract JavaFX SDK**
   - Extract to: `C:\javafx-sdk-21` (or your preferred location)

3. **Run RepairQ with JavaFX**
   ```cmd
   java -Xmx512m ^
     --add-modules javafx.controls,javafx.fxml ^
     --module-path C:\javafx-sdk-21\lib ^
     -jar RepairQ-0.0.1-SNAPSHOT.jar
   ```

4. **Update RepairQ-Run.bat** (Optional)
   - Edit the batch file and replace the `java` command with the above

### Solution B: Build a Custom Java Runtime with jlink

This creates a standalone Java runtime with JavaFX included:

```cmd
REM Prerequisites:
REM - Java 21 JDK installed
REM - JavaFX SDK 21 downloaded to your system

set JAVA_HOME=C:\Program Files\Java\jdk-21
set JAVAFX_SDK=C:\javafx-sdk-21

REM Create custom Java runtime with JavaFX
%JAVA_HOME%\bin\jlink ^
  --add-modules java.base,java.desktop,javafx.controls,javafx.fxml,javafx.graphics,java.sql,java.logging ^
  --module-path %JAVAFX_SDK%\lib ^
  --output repairq-runtime

REM Run RepairQ with custom runtime  
repairq-runtime\bin\java -Xmx512m -jar RepairQ-0.0.1-SNAPSHOT.jar
```

### Solution C: Use jpackage for Windows Installer (Advanced)

Create a native Windows EXE installer that includes everything:

```cmd
REM Prerequisites: Same as Solution B

set JAVA_HOME=C:\Program Files\Java\jdk-21
set JAVAFX_SDK=C:\javafx-sdk-21

REM If repairq-runtime doesn't exist, build it first (see Solution B)

REM Create Windows installer with bundled Java runtime
%JAVA_HOME%\bin\jpackage ^
  --type exe ^
  --name RepairQ ^
  --input target ^
  --main-jar RepairQ-0.0.1-SNAPSHOT.jar ^
  --main-class com.repairq.app.RepairQ ^
  --app-version 1.0 ^
  --runtime repairq-runtime ^
  --win-menu ^
  --win-shortcut
```

This creates `RepairQ-1.0.exe` that includes:
- Java 21 runtime
- JavaFX libraries
- Your application
- Windows Start Menu integration

---

## For Developers

### Building from Source

```cmd
REM Clone or extract the repository
cd RepairQ

REM Clean build
mvn clean package

REM Run directly (requires JavaFX SDK setup as Solution A)
java -Xmx512m ^
  --add-modules javafx.controls,javafx.fxml ^
  --module-path C:\path\to\javafx-sdk-21\lib ^
  -jar target\RepairQ-0.0.1-SNAPSHOT.jar
```

### Architecture

```
src/main/java/com/repairq/
├── app/          - Application entry point (RepairQ.java
)
├── config/       - Configuration & branding system
├── controller/   - UI controllers for JavaFX FXML
├── database/     - SQLite ORM with Hibernate 6
├── data/         - Entity models & value objects
├── service/      - Business logic layer
├── test/         - Test utilities
└── util/         - Helper functions

src/main/resources/
├── login.fxml    - JavaFX login screen
├── main-window.fxml  - Main application window
└── images/       - Application assets
```

### Technology Stack

- **Java 21 LTS** - Modern Java language features
- **JavaFX 21** - Modern cross-platform GUI framework
- **Hibernate 6.2.7** - ORM for database management
- **SQLite 3.45.1** - Local database (no server needed)
- **Jakarta Persistence 3.1** - JPA API for ORM
- **Lombok 1.18.42** - Code generation (getters, setters, etc.)
- **Maven 3.x** - Build automation

### First-Time Setup

On first launch, RepairQ:
1. Creates a local SQLite database
2. Initializes default configuration
3. Shows the login screen
4. Default credentials: `admin` / `admin` (change on first login)

---

## Future Improvements

- [ ] Native installer for Windows (using jpackage + bundled JVM)
- [ ] Portable USB version
- [ ] Auto-update mechanism
- [ ] Dark mode theme
- [ ] Multi-language support

---

## Support & Issues

For issues or questions:
1. Check the RepairQ-run.log file in the application directory
2. Verify Java 21 is installed: `java -version`
3. Ensure JavaFX SDK is properly configured (if using Solution A)

---

**Last Updated:** February 2026  
**Version:** 1.0.0-SNAPSHOT  
**Maintainer:** RepairQ Development Team
