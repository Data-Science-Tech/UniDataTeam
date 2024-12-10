package com.easydeploy.springbootquickstart.service.Impl;

import com.easydeploy.springbootquickstart.model.ModelConfig;
import com.easydeploy.springbootquickstart.model.UserServerUsage;
import com.easydeploy.springbootquickstart.repository.ModelConfigRepository;
import com.easydeploy.springbootquickstart.repository.UserServerUsageRepository;
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

    @Autowired
    private UserServerUsageRepository userServerUsageRepository;

    public ModelConfig createModelConfig(ModelConfig config) {
        config.setStatus(ModelConfig.TrainingStatus.PENDING);
        return modelConfigRepository.save(config);
    }

    public ModelConfig getModelConfig(Long id) {
        return modelConfigRepository.findById(id).orElseThrow(() -> new RuntimeException("Config not found"));
    }

    @Transactional
    public void startTraining(Long configId, Long trainingResultId, UserServerUsage usage) throws IOException {
        ModelConfig config = getModelConfig(configId);

        config.setStatus(ModelConfig.TrainingStatus.RUNNING);
        usage.setStatus("RUNNING");
        modelConfigRepository.save(config);
        userServerUsageRepository.save(usage); // 保存 usage
        System.out.println("save config successfully！");

        String[] args = createPythonScriptArgs(config, configId, trainingResultId); // 传递 trainingResultId 参数

        try {
            pythonScriptService.executeTrainingScript(args)
                    .thenAccept(process -> {
                        config.setStatus(ModelConfig.TrainingStatus.COMPLETED);
                        usage.setStatus("COMPLETED");
                        modelConfigRepository.save(config);
                        userServerUsageRepository.save(usage); // 保存 usage
                    })
                    .exceptionally(throwable -> {
                        config.setStatus(ModelConfig.TrainingStatus.FAILED);
                        usage.setStatus("FAILED");
                        modelConfigRepository.save(config);
                        userServerUsageRepository.save(usage); // 保存 usage
                        System.err.println("Training failed: " + throwable.getMessage());
                        return null;
                    });
        } catch (Exception e) {
            config.setStatus(ModelConfig.TrainingStatus.FAILED);
            usage.setStatus("FAILED");
            modelConfigRepository.save(config);
            userServerUsageRepository.save(usage); // 保存 usage
            throw e;
        }
    }

    @Override
    public List<ModelConfig> findByUserId(int userId) {
        return modelConfigRepository.findByUser_UserId(userId);
    }

    private String[] createPythonScriptArgs(ModelConfig config, Long configId, Long trainingResultId) {
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
                "--scene_ids", sceneIds,
                "--training_result_id", String.valueOf(trainingResultId) // 添加 training_result_id 参数
        };
    }

}