import com.repairq.database.DatabaseInitializer;
import com.repairq.data.embeddable.UserInfo;
import com.repairq.util.PasswordUtil;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import jakarta.persistence.EntityManager;
import jakarta.persistence.EntityManagerFactory;
import jakarta.persistence.Persistence;
import static org.junit.jupiter.api.Assertions.*;

public class DatabaseInitializerTest {
    private static EntityManagerFactory emf;
    private static EntityManager em;

    @BeforeAll
    public static void setup() {
        // Ensure fresh database by deleting file if exists
        java.io.File dbFile = new java.io.File("repairq.db");
        if (dbFile.exists()) {
            dbFile.delete();
        }
        emf = Persistence.createEntityManagerFactory("jbd-pu");
        em = emf.createEntityManager();
    }

    @Test
    public void testAdminUserCreation() {
        DatabaseInitializer.initializeDatabase();
        em.getTransaction().begin();
        UserInfo admin = em.createQuery("SELECT u.userInfo FROM com.repairq.data.entity.User u WHERE u.userInfo.username = :user", UserInfo.class)
                .setParameter("user", "admin")
                .getSingleResult();
        em.getTransaction().commit();
        assertNotNull(admin, "Admin user should exist");
        assertEquals("ADMIN", admin.getUserRole().name());
        assertTrue(PasswordUtil.checkPassword("admin", admin.getPasswordHash()), "Password should be hashed and match original");
    }
}

