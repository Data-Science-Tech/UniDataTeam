package com.easydeploy.springbootquickstart.service;

import com.easydeploy.springbootquickstart.model.ModelConfig;
import com.easydeploy.springbootquickstart.model.TrainingResult;

import java.io.IOException;

public interface ModelConfigService {

    ModelConfig createModelConfig(ModelConfig config);

    ModelConfig getModelConfig(Long id);

    void startTraining(Long configId) throws IOException;
}
