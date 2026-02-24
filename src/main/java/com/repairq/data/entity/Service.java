package com.repairq.data.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.OneToOne;
import jakarta.persistence.Table;

import com.repairq.data.FieldType;
import com.repairq.data.InputData;

import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
@Entity
@Table(name = "service")
public class Service extends BaseEntity {
    @Column(name = "price", nullable = false)
    private int price;

    @OneToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "ticket_id")
    private Ticket ticket;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "service_type_id")
    private ServiceType serviceType;

    @Override
    protected void setFields(InputData data) {
	setPrice((int) data.get(FieldType.PRICE));
	setTicket((Ticket) data.get(FieldType.TICKET));
	setServiceType((ServiceType) data.get(FieldType.SERVICE_TYPE));
    }
}
