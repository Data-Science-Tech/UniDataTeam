package com.easydeploy.springbootquickstart.model;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

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

    @ElementCollection(fetch = FetchType.EAGER)
    @CollectionTable(name = "visualized_image",
            joinColumns = @JoinColumn(name = "training_result_id")
    )
    @Column(name = "image_path")
    private List<String> visualizedImages = new ArrayList<>();  // 初始化为空列表

}