package com.repairq.data.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Embedded;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.MappedSuperclass;
import jakarta.persistence.Version;

import com.repairq.data.InputData;
import com.repairq.data.embeddable.CreationInfo;
import com.repairq.data.embeddable.UpdateInfo;

import lombok.Data;

/**
 * Abstract class AbstractEntity represents a basic data entity, and it is a
 * superclass for all other data entities in the data structure. All data
 * entities have unique ID number, an (int) field, they inherit that from this
 * class, together with getter and setter method for that field.
 * <p>
 * Field:
 * <p>
 * (int) id - must be unique
 * <p>
 *
 */
@Data
@MappedSuperclass
public abstract class AbstractEntity implements Entity {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    @Column(name = "id", updatable = false, nullable = false)
    private int id;
    
    @Version
    @Column(name = "version", nullable = false, updatable = true)
    private short version;

    /*
     * 
     */
    @Embedded
    private CreationInfo creation;

    @Embedded
    private UpdateInfo update;
    
    @Override
    public void initialize(InputData data) {
	setCreation(new CreationInfo());
	setUpdate(new UpdateInfo());
	getCreation().initialize(data);
	getUpdate().initialize(data);
    }
    
    @Override
    public void update(InputData data) {
	getUpdate().initialize(data);
    }
    
    @Override
    public String getDisplayName() {
	return Integer.toString(id);
    }
}

