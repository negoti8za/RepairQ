package com.repairq.data.entity;

import java.util.List;

import jakarta.persistence.CascadeType;
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
 * Class Model represents a device model with associated information about that
 * model.
 *
 */
@Data
@EqualsAndHashCode(callSuper = true)
@Entity
@Table(name = "model")
public class Model extends BasicInfo {
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "device_type_id", nullable = false)
    private DeviceType deviceType;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "brand_id", nullable = false)
    private Brand brand;
    
    @OneToMany(cascade = CascadeType.ALL)
    private List<Device> devices;
    
    @Override
    protected void setFields(InputData data) {
	super.setFields(data);
	setDeviceType((DeviceType) data.get(FieldType.DEVICE_TYPE));
	setBrand((Brand) data.get(FieldType.BRAND));
    }
}

