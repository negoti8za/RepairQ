package com.repairq.service;

import com.repairq.data.entity.User;
import com.repairq.data.embeddable.UserInfo;
import com.repairq.util.PasswordUtil;

import jakarta.persistence.EntityManager;
import jakarta.persistence.EntityManagerFactory;
import jakarta.persistence.Persistence;
import jakarta.persistence.TypedQuery;

public class UserService {

    public boolean authenticateUser(String username, String password) {
        EntityManagerFactory emf = null;
        EntityManager em = null;

        try {
            emf = Persistence.createEntityManagerFactory("jbd-pu");
            em = emf.createEntityManager();

            // Query for the user
            TypedQuery<User> query = em.createQuery(
                "SELECT u FROM User u WHERE u.userInfo.username = :username", User.class);
            query.setParameter("username", username);

            User user = query.getSingleResult();

            if (user != null) {
                // Check password
                return PasswordUtil.checkPassword(password, user.getUserInfo().getPasswordHash());
            }

            return false;

        } catch (Exception e) {
            return false;
        } finally {
            if (em != null) {
                em.close();
            }
            if (emf != null) {
                emf.close();
            }
        }
    }

    public User getUserByUsername(String username) {
        EntityManagerFactory emf = null;
        EntityManager em = null;

        try {
            emf = Persistence.createEntityManagerFactory("jbd-pu");
            em = emf.createEntityManager();

            TypedQuery<User> query = em.createQuery(
                "SELECT u FROM User u WHERE u.userInfo.username = :username", User.class);
            query.setParameter("username", username);

            return query.getSingleResult();

        } catch (Exception e) {
            return null;
        } finally {
            if (em != null) {
                em.close();
            }
            if (emf != null) {
                emf.close();
            }
        }
    }
}
