package com.repairq.controller;

import com.repairq.service.UserService;
import com.repairq.data.entity.User;
import javafx.fxml.FXML;
import javafx.scene.control.Alert;
import javafx.scene.control.Button;
import javafx.scene.control.PasswordField;
import javafx.scene.control.TextField;
import javafx.stage.Stage;

public class LoginController {

    @FXML
    private TextField usernameField;

    @FXML
    private PasswordField passwordField;

    @FXML
    private Button loginButton;

    private UserService userService;
    private Stage stage;

    public LoginController() {
        this.userService = new UserService();
    }

    @FXML
    private void initialize() {
        // Initialize UI components
    }

    @FXML
    private void handleLogin() {
        String username = usernameField.getText();
        String password = passwordField.getText();

        if (username.isEmpty() || password.isEmpty()) {
            showAlert("Please enter both username and password");
            return;
        }

        if (userService.authenticateUser(username, password)) {
            // Login successful
            // TODO: Navigate to main window
            stage.close();
        } else {
            showAlert("Invalid username or password");
        }
    }

    private void showAlert(String message) {
        Alert alert = new Alert(Alert.AlertType.ERROR);
        alert.setTitle("Login Error");
        alert.setHeaderText(null);
        alert.setContentText(message);
        alert.showAndWait();
    }

    public void setStage(Stage stage) {
        this.stage = stage;
    }
}