package com.repairq.data.entity;

import jakarta.persistence.Embedded;
import jakarta.persistence.Entity;
import jakarta.persistence.Table;

import com.repairq.data.InputData;
import com.repairq.data.embeddable.ContactInfo;
import com.repairq.data.embeddable.PersonalInfo;
import com.repairq.data.embeddable.UserInfo;

import lombok.Data;
import lombok.EqualsAndHashCode;

/**
 * Class User represents a employee with associated information about that
 * employee.
 *
 */
@Data
@EqualsAndHashCode(callSuper = true)
@Entity
@Table(name = "user")
public class User extends BaseEntity {
    @Embedded
    private PersonalInfo personalInfo;

    @Embedded
    private ContactInfo contactInfo;

    @Embedded
    private UserInfo userInfo;
    
    @Override
    public void initialize(InputData data) {
	setPersonalInfo(new PersonalInfo());
	setContactInfo(new ContactInfo());
	setUserInfo(new UserInfo());
	super.initialize(data);
    }
    
    @Override
    protected void setFields(InputData data) {
	getPersonalInfo().initialize(data);
	getContactInfo().initialize(data);
	getUserInfo().initialize(data);
    }

    @Override
    public String getDisplayName() {
	return userInfo.getUsername();
    }
}

