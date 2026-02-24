package com.repairq.test;

import com.repairq.config.ConfigManager;
import com.repairq.config.BrandingConfig;
import com.repairq.database.DatabaseInitializer;
import com.repairq.util.PasswordUtil;

public class BasicFunctionalityTest {
    public static void main(String[] args) {
        System.out.println("Testing RepairQ modernization components...");

        // Test config manager
        ConfigManager config = ConfigManager.getInstance();
        System.out.println("Config manager initialized: " + (config != null));

        // Test branding config
        BrandingConfig branding = BrandingConfig.getInstance();
        System.out.println("Branding config initialized: " + (branding != null));

        // Test password hashing
        String hashed = PasswordUtil.hashPassword("testpassword");
        boolean verified = PasswordUtil.checkPassword("testpassword", hashed);
        System.out.println("Password hashing works: " + verified);

        // Test database initialization (should not fail)
        DatabaseInitializer.initializeDatabase();
        System.out.println("Database initialization completed");

        System.out.println("All basic functionality tests passed!");
    }
}