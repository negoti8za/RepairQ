package com.repairq.data.entity;

import java.util.List;

import jakarta.persistence.CascadeType;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;

import com.repairq.data.FieldType;
import com.repairq.data.InputData;
import com.repairq.data.Priority;

import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
@Entity
@Table(name = "ticket")
public class Ticket extends BaseEntity {
    @Column(name = "priority")
    private Priority priority;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "status_id", nullable = false)
    private Status status;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "customer_id", nullable = false)
    private Customer customer;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "device_id", nullable = false)
    private Device device;
    
    @OneToMany(cascade = CascadeType.ALL)
    private List<Service> services;
    
    @OneToMany(cascade = CascadeType.ALL)
    private List<Service> notifications;

    @Override
    protected void setFields(InputData data) {
	setPriority((Priority) data.get(FieldType.PRIORITY));
	setStatus((Status) data.get(FieldType.STATUS));
	setCustomer((Customer) data.get(FieldType.CUSTOMER));
	setDevice((Device) data.get(FieldType.DEVICE));
    }
}
