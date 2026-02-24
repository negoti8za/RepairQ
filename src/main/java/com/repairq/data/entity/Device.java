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

import lombok.Data;
import lombok.EqualsAndHashCode;

/**
 * Class Device inherits AbstractEntity class, and represents a device with
 * associated information about that device.
 *
 */
@Data
@EqualsAndHashCode(callSuper = true)
@Entity
@Table(name = "device")
public class Device extends BaseEntity {
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "model_id", nullable = false)
    private Model model;

    @Column(name = "serial", nullable = false)
    private String serial;
    
    @OneToMany(cascade = CascadeType.ALL)
    private List<Ticket> tikets;

    @Override
    protected void setFields(InputData data) {
	setModel((Model) data.get(FieldType.MODEL));
	setSerial((String) data.get(FieldType.SERIAL));
    }
}

