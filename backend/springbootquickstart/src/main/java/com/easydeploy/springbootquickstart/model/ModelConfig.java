package com.easydeploy.springbootquickstart.model;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

import java.util.HashSet;
import java.util.Set;

@Setter
@Getter
@Table(name = "model_config")
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

    @ManyToMany(fetch = FetchType.EAGER)
    @JoinTable(
            name = "model_config_scenes",
            joinColumns = @JoinColumn(name = "model_config_id"),
            inverseJoinColumns = @JoinColumn(name = "scene_id")
    )
    private Set<SceneInfo> scenes = new HashSet<>();
    // private Long sceneId;

    @Enumerated(EnumType.STRING)
    private TrainingStatus status;

    @ManyToOne
    @JoinColumn(name = "user_id")  // 指定外键列名称
    private User user;  // 对应的 User 实体

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