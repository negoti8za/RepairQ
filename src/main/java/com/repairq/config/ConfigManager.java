package com.repairq.config;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.Properties;

public class ConfigManager {
    private static final String CONFIG_FILE = "repairq.properties";
    private static final String FIRST_TIME_SETUP_COMPLETED = "first.time.setup.completed";
    private static final String DB_INITIALIZED = "db.initialized";

    private static ConfigManager instance;
    private Properties properties;

    private ConfigManager() {
        properties = new Properties();
        loadConfig();
    }

    public static ConfigManager getInstance() {
        if (instance == null) {
            instance = new ConfigManager();
        }
        return instance;
    }

    private void loadConfig() {
        File configFile = new File(CONFIG_FILE);
        if (configFile.exists()) {
            try (FileInputStream fis = new FileInputStream(configFile)) {
                properties.load(fis);
            } catch (IOException e) {
                // Handle error - could log but don't fail the app
            }
        }
    }

    public void saveConfig() {
        try (FileOutputStream fos = new FileOutputStream(CONFIG_FILE)) {
            properties.store(fos, "RepairQ Configuration");
        } catch (IOException e) {
            // Handle error - could log but don't fail the app
        }
    }

    public boolean isFirstTimeSetupCompleted() {
        return "true".equals(properties.getProperty(FIRST_TIME_SETUP_COMPLETED, "false"));
    }

    public void setFirstTimeSetupCompleted(boolean completed) {
        properties.setProperty(FIRST_TIME_SETUP_COMPLETED, String.valueOf(completed));
        saveConfig();
    }

    public boolean isDatabaseInitialized() {
        return "true".equals(properties.getProperty(DB_INITIALIZED, "false"));
    }

    public void setDatabaseInitialized(boolean initialized) {
        properties.setProperty(DB_INITIALIZED, String.valueOf(initialized));
        saveConfig();
    }
}