package com.repairq.data.entity;

import java.util.List;

import jakarta.persistence.CascadeType;
import jakarta.persistence.Entity;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;

import lombok.Data;
import lombok.EqualsAndHashCode;

/**
 * Class Brand represents a device brand.
 *
 */
@Data
@EqualsAndHashCode(callSuper = true)
@Entity
@Table(name = "brand")
public class Brand extends BasicInfo {
    @OneToMany(cascade = CascadeType.ALL)
    private List<Model> models;
}

