package com.easydeploy.springbootquickstart.model;

import jakarta.persistence.*;

@Entity
@Table(name = "training_progress")
public class TrainingProcess {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String type;
    private int currentEpoch;
    private int totalEpochs;
    private int currentBatch;
    private int totalBatches;
    private double currentLoss;
    private double avgLoss;
    private double progressPercentage;
    private Integer userServerUsageId;

    // Getters and Setters
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public int getCurrentEpoch() {
        return currentEpoch;
    }

    public void setCurrentEpoch(int currentEpoch) {
        this.currentEpoch = currentEpoch;
    }

    public int getTotalEpochs() {
        return totalEpochs;
    }

    public void setTotalEpochs(int totalEpochs) {
        this.totalEpochs = totalEpochs;
    }

    public int getCurrentBatch() {
        return currentBatch;
    }

    public void setCurrentBatch(int currentBatch) {
        this.currentBatch = currentBatch;
    }

    public int getTotalBatches() {
        return totalBatches;
    }

    public void setTotalBatches(int totalBatches) {
        this.totalBatches = totalBatches;
    }

    public double getCurrentLoss() {
        return currentLoss;
    }

    public void setCurrentLoss(double currentLoss) {
        this.currentLoss = currentLoss;
    }

    public double getAvgLoss() {
        return avgLoss;
    }

    public void setAvgLoss(double avgLoss) {
        this.avgLoss = avgLoss;
    }

    public double getProgressPercentage() {
        return progressPercentage;
    }

    public void setProgressPercentage(double progressPercentage) {
        this.progressPercentage = progressPercentage;
    }

    public Integer getUserServerUsageId() {
        return userServerUsageId;
    }

    public void setUserServerUsageId(Integer userServerUsageId) {
        this.userServerUsageId = userServerUsageId;
    }
}
