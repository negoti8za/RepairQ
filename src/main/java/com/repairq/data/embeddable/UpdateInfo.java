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
public class UpdateInfo implements EmbeddableClass {
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user", nullable = false, updatable = true, referencedColumnName = "id")
    private User user;

    @Column(name = "last_update_date", nullable = false, updatable = true)
    @Temporal(TemporalType.TIMESTAMP)
    private Calendar lastUpdateDate;
    
    @Override
    public void initialize(InputData data) {
	setUser((User) data.get(FieldType.USER));
	setLastUpdateDate((Calendar) data.get(FieldType.TIMESTAMP));
    }
}
