package com.easydeploy.springbootquickstart.controller;

import com.easydeploy.springbootquickstart.model.ModelConfig;
import com.easydeploy.springbootquickstart.model.SceneInfo;
import com.easydeploy.springbootquickstart.model.TrainingResult;
import com.easydeploy.springbootquickstart.service.ModelConfigService;
import com.easydeploy.springbootquickstart.service.SceneInfoService;
import com.easydeploy.springbootquickstart.dto.request.ModelConfigRequest;
import com.easydeploy.springbootquickstart.dto.response.ModelConfigResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.io.IOException;
import java.util.Set;

@RestController
@RequestMapping("/api/model-configs")
public class ModelConfigController {

    @Autowired
    private ModelConfigService modelConfigService;
    @Autowired
    private SceneInfoService sceneInfoService;

    @PostMapping
    public ResponseEntity<ModelConfig> createModelConfig(@RequestBody ModelConfigRequest request) {
        ModelConfig config = new ModelConfig();
        // 设置基本参数
        config.setAlgorithm(ModelConfig.Algorithm.valueOf(request.getAlgorithm()));
        config.setLearningRate(request.getLearningRate());
        config.setNumEpochs(request.getNumEpochs());
        config.setBatchSize(request.getBatchSize());
        config.setMomentumValue(request.getMomentumValue());
        config.setWeightDecay(request.getWeightDecay());

        // 设置多个场景
        Set<SceneInfo> scenes = sceneInfoService.findAllById(request.getSceneIds());
        config.setScenes(scenes);

        return ResponseEntity.ok(modelConfigService.createModelConfig(config));
    }
    

    @PostMapping("/{id}/train")
    public void startTraining(@PathVariable Long id) throws IOException {
        modelConfigService.startTraining(id);
    }

    @GetMapping("/{id}/status")
    public ModelConfig.TrainingStatus getTrainingStatus(@PathVariable Long id) {
        return modelConfigService.getModelConfig(id).getStatus();
    }

    @GetMapping("/{id}/result")
    public TrainingResult getTrainingResult(@PathVariable Long id) {
        return modelConfigService.getTrainingResult(id);
    }

}