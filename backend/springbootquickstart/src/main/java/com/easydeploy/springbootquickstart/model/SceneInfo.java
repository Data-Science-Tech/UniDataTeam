package com.easydeploy.springbootquickstart.model;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@Table(name = "scene_info")
@Entity
public class SceneInfo {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer sceneId;

    @Column(length = 1000)
    private String sceneDescription;

    private Long logInfoId;
    private int sampleCount;
    private Long firstSampleId;
    private Long lastSampleId;
}
