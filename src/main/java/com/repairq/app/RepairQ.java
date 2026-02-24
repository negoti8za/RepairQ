package com.repairq.app;

import com.repairq.config.ConfigManager;
import com.repairq.database.DatabaseInitializer;
import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;

import java.io.IOException;
import java.net.URL;

public class RepairQ extends Application {

    @Override
    public void start(Stage primaryStage) {
        try {
            System.out.println("[RepairQ] JavaFX initialization successful");
            System.out.println("[RepairQ] Starting application...");
            
            // Initialize database if needed
            System.out.println("[RepairQ] Initializing database...");
            DatabaseInitializer.initializeDatabase();
            System.out.println("[RepairQ] Database initialized");

            // Check if first-time setup is completed
            if (!ConfigManager.getInstance().isFirstTimeSetupCompleted()) {
                System.out.println("[RepairQ] First-time setup in progress...");
                ConfigManager.getInstance().setFirstTimeSetupCompleted(true);
                ConfigManager.getInstance().saveConfig();
            }

            // Load the login screen
            System.out.println("[RepairQ] Loading login screen...");
            URL fxmlResource = getClass().getResource("/login.fxml");
            if (fxmlResource == null) {
                System.err.println("[ERROR] login.fxml not found in classpath");
                showErrorAndExit(primaryStage, "Failed to load UI", "login.fxml not found. Application cannot start.");
                return;
            }
            
            FXMLLoader loader = new FXMLLoader(fxmlResource);
            Parent root = loader.load();
            
            Scene scene = new Scene(root, 300, 200);
            primaryStage.setTitle("RepairQ Login");
            primaryStage.setScene(scene);
            primaryStage.show();
            
            System.out.println("[RepairQ] Application started successfully");
        } catch (IOException e) {
            System.err.println("[ERROR] IOException: " + e.getMessage());
            e.printStackTrace();
            showErrorAndExit(primaryStage, "Failed to load application", e.getMessage());
        } catch (Exception e) {
            System.err.println("[ERROR] Unexpected error: " + e.getMessage());
            e.printStackTrace();
            showErrorAndExit(primaryStage, "Application error", e.getMessage());
        }
    }

    private void showErrorAndExit(Stage stage, String title, String message) {
        System.err.println("[ERROR] " + title + ": " + message);
        // For now, just exit - in future, show an error dialog
        System.exit(1);
    }

    public static void main(String[] args) {
        System.out.println("[RepairQ] JVM started");
        System.out.println("[RepairQ] Java version: " + System.getProperty("java.version"));
        System.out.println("[RepairQ] Java home: " + System.getProperty("java.home"));
        System.out.println("[RepairQ] Working directory: " + System.getProperty("user.dir"));
        System.out.println("[RepairQ] OS: " + System.getProperty("os.name"));
        System.out.println("[RepairQ] Launching JavaFX application...");
        System.out.flush();
        System.err.flush();
        
        try {
            launch(args);
        } catch (Exception e) {
            System.err.println("[FATAL] Failed to start JavaFX application");
            System.err.println("[FATAL] " + e.getClass().getName() + ": " + e.getMessage());
            e.printStackTrace(System.err);
            System.exit(1);
        }
    }
}