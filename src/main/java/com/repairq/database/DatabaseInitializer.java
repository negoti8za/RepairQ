package com.repairq.database;

import com.repairq.config.ConfigManager;
import com.repairq.data.entity.User;
import com.repairq.data.UserRole;
import com.repairq.util.PasswordUtil;
import com.repairq.data.embeddable.PersonalInfo;
import com.repairq.data.embeddable.UserInfo;
import com.repairq.data.embeddable.ContactInfo;
import com.repairq.data.InputData;
import com.repairq.data.FieldType;

import jakarta.persistence.EntityManager;
import jakarta.persistence.EntityManagerFactory;
import jakarta.persistence.Persistence;
import java.util.HashMap;
import java.util.Map;

public class DatabaseInitializer {

    public static void initializeDatabase() {
        // Only initialize if not already done
        if (ConfigManager.getInstance().isDatabaseInitialized()) {
            return;
        }

        EntityManagerFactory emf = null;
        EntityManager em = null;

        try {
            // Create EntityManager
            emf = Persistence.createEntityManagerFactory("jbd-pu");
            em = emf.createEntityManager();

            // Begin transaction
            em.getTransaction().begin();

            // Create default admin user
            createUser(em, "admin", "admin", UserRole.ADMIN);

            // Mark database as initialized
            ConfigManager.getInstance().setDatabaseInitialized(true);

            // Commit transaction
            em.getTransaction().commit();

        } catch (Exception e) {
            if (em != null && em.getTransaction().isActive()) {
                em.getTransaction().rollback();
            }
            e.printStackTrace();
        } finally {
            if (em != null) {
                em.close();
            }
            if (emf != null) {
                emf.close();
            }
        }
    }

    private static void createUser(EntityManager em, String username, String password, UserRole role) {
        // Create user entity
        User user = new User();

        // Set personal info
        PersonalInfo personalInfo = new PersonalInfo();
        personalInfo.setFirstName("Admin");
        personalInfo.setLastName("User");

        // Set contact info
        ContactInfo contactInfo = new ContactInfo();
        contactInfo.setPhoneNumber("");
        contactInfo.setEmail("");
        contactInfo.setAddress("");

        // Set user info
        UserInfo userInfo = new UserInfo();
        userInfo.setUserRole(role);
        userInfo.setUsername(username);
        // Note: In a real implementation, we would hash the password here
        userInfo.setPasswordHash(PasswordUtil.hashPassword(password));

        user.setPersonalInfo(personalInfo);
        user.setContactInfo(contactInfo);
        user.setUserInfo(userInfo);

        // Persist the user
        em.persist(user);
    }
}
