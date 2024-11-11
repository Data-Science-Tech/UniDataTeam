package com.easydeploy.springbootquickstart.model;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Column;
import jakarta.persistence.Enumerated;
import jakarta.persistence.EnumType;
import lombok.Getter;
import lombok.Setter;

@Setter
@Getter
@Entity
public class ModelConfig {

    // Getters and Setters
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Enumerated(EnumType.STRING)
    private Algorithm algorithm;

    private double learningRate;
    private int numEpochs;
    private int batchSize;
    private double momentumValue;
    private double weightDecay;
    private int sceneId;

    @Enumerated(EnumType.STRING)
    private TrainingStatus status;

    public enum Algorithm {
        FAST_R_CNN,
        SSD
    }

    public enum TrainingStatus {
        PENDING,
        RUNNING,
        COMPLETED,
        FAILED
    }

}