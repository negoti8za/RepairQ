package com.repairq.config;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.Properties;

public class BrandingConfig {
    private static final String CONFIG_FILE = "branding.properties";
    private static final String COMPANY_NAME = "company.name";
    private static final String COMPANY_ADDRESS = "company.address";
    private static final String COMPANY_PHONE = "company.phone";
    private static final String COMPANY_EMAIL = "company.email";
    private static final String COMPANY_FOOTER = "company.footer";
    private static final String LOGO_PATH = "logo.path";

    private static BrandingConfig instance;
    private Properties properties;

    private BrandingConfig() {
        properties = new Properties();
        loadConfig();
    }

    public static BrandingConfig getInstance() {
        if (instance == null) {
            instance = new BrandingConfig();
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
            properties.store(fos, "RepairQ Branding Configuration");
        } catch (IOException e) {
            // Handle error - could log but don't fail the app
        }
    }

    // Company information
    public String getCompanyName() {
        return properties.getProperty(COMPANY_NAME, "RepairQ Company");
    }

    public void setCompanyName(String companyName) {
        properties.setProperty(COMPANY_NAME, companyName);
        saveConfig();
    }

    public String getCompanyAddress() {
        return properties.getProperty(COMPANY_ADDRESS, "");
    }

    public void setCompanyAddress(String companyAddress) {
        properties.setProperty(COMPANY_ADDRESS, companyAddress);
        saveConfig();
    }

    public String getCompanyPhone() {
        return properties.getProperty(COMPANY_PHONE, "");
    }

    public void setCompanyPhone(String companyPhone) {
        properties.setProperty(COMPANY_PHONE, companyPhone);
        saveConfig();
    }

    public String getCompanyEmail() {
        return properties.getProperty(COMPANY_EMAIL, "");
    }

    public void setCompanyEmail(String companyEmail) {
        properties.setProperty(COMPANY_EMAIL, companyEmail);
        saveConfig();
    }

    public String getCompanyFooter() {
        return properties.getProperty(COMPANY_FOOTER, "Thank you for your business!");
    }

    public void setCompanyFooter(String companyFooter) {
        properties.setProperty(COMPANY_FOOTER, companyFooter);
        saveConfig();
    }

    // Logo path
    public String getLogoPath() {
        return properties.getProperty(LOGO_PATH, "");
    }

    public void setLogoPath(String logoPath) {
        properties.setProperty(LOGO_PATH, logoPath);
        saveConfig();
    }
}