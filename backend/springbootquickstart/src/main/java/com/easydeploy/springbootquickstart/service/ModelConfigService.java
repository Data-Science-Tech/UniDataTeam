package com.easydeploy.springbootquickstart.service;

import com.easydeploy.springbootquickstart.model.ModelConfig;
import com.easydeploy.springbootquickstart.repository.ModelConfigRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;


@Service
public class ModelConfigService {

    @Autowired
    private ModelConfigRepository modelConfigRepository;

    public ModelConfig createModelConfig(ModelConfig config) {
        return modelConfigRepository.save(config);
    }

    public ModelConfig getModelConfig(Long id) {
        return modelConfigRepository.findById(id).orElseThrow(() -> new RuntimeException("Config not found"));
    }

    public List<ModelConfig> getAllConfigs() {
        return modelConfigRepository.findAll();
    }
}
