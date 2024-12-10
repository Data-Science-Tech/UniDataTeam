package com.easydeploy.springbootquickstart.service;

import com.easydeploy.springbootquickstart.model.ModelConfig;

import java.io.IOException;
import java.util.List;

public interface ModelConfigService {

    ModelConfig createModelConfig(ModelConfig config);

    ModelConfig getModelConfig(Long id);

    void startTraining(Long configId) throws IOException;

    public List<ModelConfig> findByUserId(int userId);
}
