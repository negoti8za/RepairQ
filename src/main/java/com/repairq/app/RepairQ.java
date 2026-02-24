package com.repairq.app;

import com.repairq.config.ConfigManager;
import com.repairq.database.DatabaseInitializer;
import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;

import java.io.IOException;

public class RepairQ extends Application {

    @Override
    public void start(Stage primaryStage) throws IOException {
        // Initialize database if needed
        DatabaseInitializer.initializeDatabase();

        // Check if first-time setup is completed
        if (!ConfigManager.getInstance().isFirstTimeSetupCompleted()) {
            // Show first-time setup - for now, we'll just mark it as completed
            // In a real implementation, this would show a setup wizard
            ConfigManager.getInstance().setFirstTimeSetupCompleted(true);
        }

        // Load the login screen
        Parent root = FXMLLoader.load(getClass().getResource("/login.fxml"));
        Scene scene = new Scene(root, 300, 200);
        primaryStage.setTitle("RepairQ Login");
        primaryStage.setScene(scene);
        primaryStage.show();
    }

    public static void main(String[] args) {
        launch(args);
    }
}