package com.easydeploy.springbootquickstart.controller;

import com.easydeploy.springbootquickstart.model.ModelConfig;
import com.easydeploy.springbootquickstart.service.ModelConfigService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/model-config")
public class ModelConfigController {

    @Autowired
    private ModelConfigService modelConfigService;

    // Endpoint to create a new configuration
    @PostMapping
    public ModelConfig createConfig(@RequestBody ModelConfig config) {
        return modelConfigService.createModelConfig(config);
    }

    // Endpoint to get a specific configuration by id
    @GetMapping("/{id}")
    public ModelConfig getConfig(@PathVariable Long id) {
        return modelConfigService.getModelConfig(id);
    }

    // Endpoint to get all configurations
    @GetMapping
    public List<ModelConfig> getAllConfigs() {
        return modelConfigService.getAllConfigs();
    }
}
