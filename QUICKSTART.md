## RepairQ Quick Reference

### Running RepairQ - Three Ways

#### 1️⃣ Easiest: Using RepairQ-Run.bat
```cmd
RepairQ-Run.bat
```
✅ Automatic Java detection  
✅ Logs errors to RepairQ-run.log  
⚠️ Requires: Java 21 LTS installed

---

#### 2️⃣ With JavaFX SDK (Recommended for development)

**Download JavaFX SDK:**
1. Go to: https://gluonhq.com/products/javafx/
2. Download: JavaFX SDK 21 (Windows)
3. Extract to: `C:\javafx-sdk-21`

**Run with JavaFX:**
```cmd
java -Xmx512m ^
  --add-modules javafx.controls,javafx.fxml ^
  --module-path C:\javafx-sdk-21\lib ^
  -jar RepairQ-0.0.1-SNAPSHOT.jar
```

Or update `RepairQ-Run.bat` with the above command.

---

#### 3️⃣ Advanced: Create Native Installer

**For complete solution with bundled Java 21 & JavaFX:**

See `WINDOWS-DEPLOYMENT.md` → "Solution C: Use jpackage"

This creates: `RepairQ-1.0.exe` (standalone installer, no external Java needed)

---

### Troubleshooting

**Q: "JavaFX runtime components missing" error**  
A: See WINDOWS-DEPLOYMENT.md Solutions A or B

**Q: "Java not found" error**  
A: Install Java 21 from: https://adoptium.net/

**Q: Application window doesn't appear**  
A: Check `RepairQ-run.log` for errors

**Q: Want to build from source?**  
A: Use `RepairQ-Build.bat` or: `mvn clean package`

---

### File Descriptions

| File | Purpose |
|------|---------|
| `RepairQ-Run.bat` | Main Windows launcher script |
| `RepairQ-0.0.1-SNAPSHOT.jar` | Compiled application + all dependencies (38.97 MB) |
| `WINDOWS-DEPLOYMENT.md` | Complete deployment guide |
| `README.md` | Project overview & architecture |
| `pom.xml` | Maven build configuration |

---

### System Requirements

| Component | Requirement |
|-----------|-------------|
| Operating System | Windows 10 or later |
| Java | Java 21 LTS |
| Memory | 512 MB RAM (minimum) |
| Disk | 50 MB for installation |
| Database | SQLite (local, no server) |

---

### Default Login

| Field | Value |
|-------|-------|
| Username | `admin` |
| Password | `admin` |

⚠️ Change password on first login!

---

### Support

1. Check `RepairQ-run.log` in the application directory
2. Read `WINDOWS-DEPLOYMENT.md` for detailed solutions
3. Ensure Java 21 is installed: `java -version`
