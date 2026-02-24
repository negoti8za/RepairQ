package com.repairq.data.entity;

import jakarta.persistence.Column;
import jakarta.persistence.MappedSuperclass;

import com.repairq.data.FieldType;
import com.repairq.data.InputData;

import lombok.Data;
import lombok.EqualsAndHashCode;

/**
 * Class BasicInfo represents a basic information of various entity classes.
 *
 */

@Data
@EqualsAndHashCode(callSuper = true)
@MappedSuperclass
public abstract class BasicInfo extends BaseEntity {
    @Column(name = "name", nullable = false, unique = true)
    private String name;

    @Column(name = "description", nullable = true, unique = false)
    private String description;
    
    @Override
    protected void setFields(InputData data) {
	setName((String) data.get(FieldType.NAME));
	setDescription((String) data.get(FieldType.DESCRIPTION));
    }
    
    @Override
    public String getDisplayName() {
	return name;
    }
}

