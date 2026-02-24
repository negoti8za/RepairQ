package com.repairq.data.entity;

import java.util.List;

import jakarta.persistence.CascadeType;
import jakarta.persistence.Entity;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;

import lombok.Data;
import lombok.EqualsAndHashCode;

/**
 * Class DeviceType represents a device type.
 *
 */
@Data
@EqualsAndHashCode(callSuper = true)
@Entity
@Table(name = "device_type")
public class DeviceType extends BasicInfo {
    @OneToMany(cascade = CascadeType.ALL)
    private List<Model> models;
}

