package com.easydeploy.springbootquickstart.model;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

import java.time.LocalDateTime;

@Setter
@Getter
@Table(name = "training_result")
@Entity
public class TrainingResult {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @OneToOne
    private ModelConfig modelConfig;

    private LocalDateTime startTime;
    private LocalDateTime endTime;

    @Column(length = 1000)
    private String trainingLogs;

    private String modelFilePath;
    private double finalLoss;
    private double accuracy;

}