package com.easydeploy.springbootquickstart.dto.response;

import lombok.Data;
import java.util.List;

@Data
public class ModelConfigResponse {
    private Long id;
    private String algorithm;
    private Double learningRate;
    private Integer numEpochs;
    private Integer batchSize;
    private Double momentumValue;
    private Double weightDecay;
    private List<SceneInfoDTO> scenes;

    @Data
    public static class SceneInfoDTO {
        private Integer sceneId;
        private String sceneName;
    }
}
