package com.easydeploy.springbootquickstart.service;

import com.easydeploy.springbootquickstart.model.ModelConfig;
import com.easydeploy.springbootquickstart.model.UserServerUsage;

import java.io.IOException;
import java.util.List;

public interface ModelConfigService {

    ModelConfig createModelConfig(ModelConfig config);

    ModelConfig getModelConfig(Long id);

    void startTraining(Long configId, Long trainingResultId, UserServerUsage usage) throws IOException; // 添加 UserServerUsage 参数

    List<ModelConfig> findByUserId(int userId);
}
