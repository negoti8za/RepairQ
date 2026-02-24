package com.repairq.data.embeddable;

import java.util.Calendar;

import jakarta.persistence.Column;
import jakarta.persistence.Embeddable;
import jakarta.persistence.FetchType;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Temporal;
import jakarta.persistence.TemporalType;

import com.repairq.data.FieldType;
import com.repairq.data.InputData;
import com.repairq.data.entity.User;

import lombok.Data;

@Data
@Embeddable
public class CreationInfo implements EmbeddableClass {
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "created_by_user_id", nullable = false, updatable = false, referencedColumnName = "id")
    private User owner;

    @Column(name = "creation_date", nullable = false, updatable = false)
    @Temporal(TemporalType.TIMESTAMP)
    private Calendar creationDate;
    
    @Override
    public void initialize(InputData data) {
	setOwner((User) data.get(FieldType.USER));
	setCreationDate((Calendar) data.get(FieldType.TIMESTAMP));
    }
}
