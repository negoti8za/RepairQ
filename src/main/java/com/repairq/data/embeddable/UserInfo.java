package com.repairq.data.embeddable;

import jakarta.persistence.Column;
import jakarta.persistence.Embeddable;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;

import com.repairq.data.FieldType;
import com.repairq.data.InputData;
import com.repairq.data.UserRole;
import com.repairq.util.PasswordUtil;

import lombok.Data;

@Data
@Embeddable
public class UserInfo implements EmbeddableClass {
    @Enumerated(EnumType.ORDINAL)
    @Column(name = "user_type", nullable = false)
    private UserRole userRole;

    @Column(name = "username", nullable = false, unique = true)
    private String username;

    @Column(name = "password", nullable = false)
    private String passwordHash;

    @Override
    public void initialize(InputData data) {
	setUserRole((UserRole) data.get(FieldType.USER_ROLE));
	setUsername((String) data.get(FieldType.USERNAME));
	// Hash the password when setting it
	setPasswordHash(PasswordUtil.hashPassword((String) data.get(FieldType.PASSWORD)));
    }
}
