# RepairQ jpackage Build Script

This file contains instructions for creating a native Windows installer for RepairQ.

## Prerequisites
1. Java 21 JDK with jpackage (available in JDK 14+)
2. Maven installed

## Build Steps

1. Compile the project:
   ```bash
   mvn clean compile
   ```

2. Package the application:
   ```bash
   mvn package
   ```

3. Create the native Windows installer using jpackage:
   ```bash
   jpackage --name RepairQ \
            --input target \
            --main-jar repairq-0.0.1-SNAPSHOT.jar \
            --main-class com.repairq.app.RepairQ \
            --app-version 1.0 \
            --vendor "RepairQ" \
            --description "RepairQ Desktop Application" \
            --icon src/main/resources/images/repairq-icon.ico \
            --win-dir-chooser \
            --win-menu \
            --win-shortcut \
            --java-options "-Xmx512m"
   ```

## Notes
- The icon file `repairq-icon.ico` should be placed in `src/main/resources/images/`
- Adjust memory options as needed for your application
- The jpackage command will create a Windows installer in the current directory