package com.easydeploy.springbootquickstart.model;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Column;
import jakarta.persistence.Enumerated;
import jakarta.persistence.EnumType;
import lombok.Getter;

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
    private String modelSavePath;

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

    public void setId(Long id) {
        this.id = id;
    }

    public void setAlgorithm(Algorithm algorithm) {
        this.algorithm = algorithm;
    }

    public void setLearningRate(double learningRate) {
        this.learningRate = learningRate;
    }

    public void setNumEpochs(int numEpochs) {
        this.numEpochs = numEpochs;
    }

    public void setBatchSize(int batchSize) {
        this.batchSize = batchSize;
    }

    public void setMomentumValue(double momentumValue) {
        this.momentumValue = momentumValue;
    }

    public void setWeightDecay(double weightDecay) {
        this.weightDecay = weightDecay;
    }

    public void setSceneId(int sceneId) {
        this.sceneId = sceneId;
    }

    public void setModelSavePath(String modelSavePath) {
        this.modelSavePath = modelSavePath;
    }

    public void setStatus(TrainingStatus status) {
        this.status = status;
    }

}