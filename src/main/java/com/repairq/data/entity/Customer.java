package com.repairq.data.entity;

import java.util.List;

import jakarta.persistence.CascadeType;
import jakarta.persistence.Embedded;
import jakarta.persistence.Entity;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;

import com.repairq.data.InputData;
import com.repairq.data.embeddable.ContactInfo;
import com.repairq.data.embeddable.PersonalInfo;

import lombok.Data;
import lombok.EqualsAndHashCode;

/**
 * Class Client represents a client with associated information about that
 * client.
 *
 */
@Data
@EqualsAndHashCode(callSuper = true)
@Entity
@Table(name = "customer")
public class Customer extends BaseEntity {
    @Embedded
    private PersonalInfo personalInfo;

    @Embedded
    private ContactInfo contactInfo;
    
    @OneToMany(cascade = CascadeType.ALL)
    private List<Ticket> tikets;
    
    @Override
    public void initialize(InputData data) {
	setPersonalInfo(new PersonalInfo());
	setContactInfo(new ContactInfo());
	super.initialize(data);
    }
    
    @Override
    protected void setFields(InputData data) {
	getPersonalInfo().initialize(data);
	getContactInfo().initialize(data);
    }
    
    @Override
    public String getDisplayName() {
	return super.getDisplayName() + " " + getPersonalInfo().getDispalyName();
    }
}

