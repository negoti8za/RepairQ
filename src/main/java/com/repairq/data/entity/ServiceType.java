package com.repairq.data.entity;

import java.util.List;

import jakarta.persistence.CascadeType;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;

import com.repairq.data.FieldType;
import com.repairq.data.InputData;

import lombok.Data;
import lombok.EqualsAndHashCode;

/**
 * Class ServiceType extends abstract class Property and represents a the type
 * of a service.
 *
 */
@Data
@EqualsAndHashCode(callSuper = true)
@Entity
@Table(name = "service_type")
public class ServiceType extends BasicInfo {
    @Column(name = "default_price", nullable = false)
    private int defaultPrice;
    
    @OneToMany(cascade = CascadeType.ALL)
    private List<Service> services;
    
    @Override
    protected void setFields(InputData data) {
	super.setFields(data);
	setDefaultPrice((int) data.get(FieldType.PRICE));
    }
}

