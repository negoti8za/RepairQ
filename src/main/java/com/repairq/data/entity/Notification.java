package com.repairq.data.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;

import com.repairq.data.FieldType;
import com.repairq.data.InputData;

import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
@Entity
@Table(name = "notification")
public class Notification extends BasicInfo {
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "notification_type_id", nullable = false)
    private NotificationType notificationType;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "ticket_id", nullable = false)
    private Ticket ticket;

    @Column(name = "comment")
    private String comment;

    @Override
    protected void setFields(InputData data) {
	setNotificationType((NotificationType) data.get(FieldType.NOTIFICATION_TYPE));
	setTicket((Ticket) data.get(FieldType.TICKET));
	setComment((String) data.get(FieldType.COMMENT));
    }
}
