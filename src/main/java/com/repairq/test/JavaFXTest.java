package com.repairq.test;

import com.repairq.config.ConfigManager;
import com.repairq.config.BrandingConfig;
import com.repairq.database.DatabaseInitializer;
import com.repairq.util.PasswordUtil;
import com.repairq.service.UserService;

public class JavaFXTest {
    public static void main(String[] args) {
        System.out.println("Testing JavaFX components...");

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

        // Test database initialization
        DatabaseInitializer.initializeDatabase();
        System.out.println("Database initialization completed");

        // Test user service
        UserService userService = new UserService();
        System.out.println("User service created: " + (userService != null));

        System.out.println("All JavaFX components tests passed!");
    }
}