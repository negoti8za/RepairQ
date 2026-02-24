package com.repairq.data.entity;

import java.util.List;

import jakarta.persistence.CascadeType;
import jakarta.persistence.Entity;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;

import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
@Entity
@Table(name = "notification_type")
public class NotificationType extends BasicInfo {
    @OneToMany(cascade = CascadeType.ALL)
    private List<Notification> notifications;
}
