package com.easydeploy.springbootquickstart.controller;

import com.easydeploy.springbootquickstart.model.ModelConfig;
import com.easydeploy.springbootquickstart.model.TrainingResult;
import com.easydeploy.springbootquickstart.service.ModelConfigService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.io.IOException;

@RestController
@RequestMapping("/api/model-configs")
public class ModelConfigController {

    @Autowired
    private ModelConfigService modelConfigService;

    @PostMapping
    public ModelConfig createConfig(@RequestBody ModelConfig config) {
        return modelConfigService.createModelConfig(config);
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