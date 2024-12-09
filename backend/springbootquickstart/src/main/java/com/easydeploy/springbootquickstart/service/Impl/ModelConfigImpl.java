package com.easydeploy.springbootquickstart.service.Impl;

import com.easydeploy.springbootquickstart.model.ModelConfig;
import com.easydeploy.springbootquickstart.repository.ModelConfigRepository;
import com.easydeploy.springbootquickstart.service.ModelConfigService;
import com.easydeploy.springbootquickstart.service.PythonScriptService;
import jakarta.transaction.Transactional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class ModelConfigImpl implements ModelConfigService {

    @Autowired
    private ModelConfigRepository modelConfigRepository;

    @Autowired
    private PythonScriptService pythonScriptService;

    public ModelConfig createModelConfig(ModelConfig config) {
        config.setStatus(ModelConfig.TrainingStatus.PENDING);
        return modelConfigRepository.save(config);
    }

    public ModelConfig getModelConfig(Long id) {
        return modelConfigRepository.findById(id).orElseThrow(() -> new RuntimeException("Config not found"));
    }

    @Transactional
    public void startTraining(Long configId) throws IOException {
        ModelConfig config = getModelConfig(configId);

        config.setStatus(ModelConfig.TrainingStatus.RUNNING);
        System.out.println("before save config！");
        modelConfigRepository.save(config);
        System.out.println("save config successfully！");

        // 修改 createPythonScriptArgs 方法，确保包含 model_config_id
        String[] args = createPythonScriptArgs(config, configId); // 添加 configId 参数

        try {
            pythonScriptService.executeTrainingScript(args)
                    .thenAccept(process -> {
                        config.setStatus(ModelConfig.TrainingStatus.COMPLETED);
                        modelConfigRepository.save(config);
                    })
                    .exceptionally(throwable -> {
                        config.setStatus(ModelConfig.TrainingStatus.FAILED);
                        modelConfigRepository.save(config);
                        // 输出到控制台
                        System.err.println("Training failed: " + throwable.getMessage());
                        return null;
                    });
        } catch (Exception e) {
            config.setStatus(ModelConfig.TrainingStatus.FAILED);
            modelConfigRepository.save(config);
            throw e;
        }
    }

    @Override
    public List<ModelConfig> findByUserId(int userId) {
        return modelConfigRepository.findByUser_UserId(userId);
    }

    private String[] createPythonScriptArgs(ModelConfig config, Long configId) {
        // 将场景ID列表转换为逗号分隔的字符串
        String sceneIds = config.getScenes().stream()
                .map(scene -> String.valueOf(scene.getSceneId()))
                .collect(Collectors.joining(","));

        return new String[]{
                "--model_config_id", String.valueOf(configId),
                "--algorithm", config.getAlgorithm().toString(),
                "--learning_rate", String.valueOf(config.getLearningRate()),
                "--num_epochs", String.valueOf(config.getNumEpochs()),
                "--batch_size", String.valueOf(config.getBatchSize()),
                "--momentum", String.valueOf(config.getMomentumValue()),
                "--weight_decay", String.valueOf(config.getWeightDecay()),
                "--scene_ids", sceneIds  // 修改为多场景ID参数
        };
    }

}