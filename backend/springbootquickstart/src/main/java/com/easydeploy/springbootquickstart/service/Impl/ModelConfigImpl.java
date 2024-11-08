package com.easydeploy.springbootquickstart.service.Impl;

import com.easydeploy.springbootquickstart.model.ModelConfig;
import com.easydeploy.springbootquickstart.model.TrainingResult;
import com.easydeploy.springbootquickstart.repository.ModelConfigRepository;
import com.easydeploy.springbootquickstart.repository.TrainingResultRepository;
import com.easydeploy.springbootquickstart.service.ModelConfigService;
import com.easydeploy.springbootquickstart.service.PythonScriptService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.time.LocalDateTime;

@Service
public class ModelConfigImpl implements ModelConfigService {

    @Autowired
    private ModelConfigRepository modelConfigRepository;

    @Autowired
    private TrainingResultRepository trainingResultRepository;

    @Autowired
    private PythonScriptService pythonScriptService;

    public ModelConfig createModelConfig(ModelConfig config) {
        config.setStatus(ModelConfig.TrainingStatus.PENDING);
        return modelConfigRepository.save(config);
    }

    public ModelConfig getModelConfig(Long id) {
        return modelConfigRepository.findById(id).orElseThrow(() -> new RuntimeException("Config not found"));
    }

    public TrainingResult getTrainingResult(Long id) {
        return trainingResultRepository.findById(id).orElseThrow(() -> new RuntimeException("Training result not found"));
    }

    public void startTraining(Long configId) throws IOException {
        ModelConfig config = getModelConfig(configId);

        config.setStatus(ModelConfig.TrainingStatus.RUNNING);
        modelConfigRepository.save(config);

        TrainingResult result = new TrainingResult();
        result.setModelConfig(config);
        result.setStartTime(LocalDateTime.now());
        trainingResultRepository.save(result);

        // Create arguments for Python script
        String[] args = createPythonScriptArgs(config);

        try {
            pythonScriptService.executeTrainingScript(args)
                    .thenAccept(process -> {
                        config.setStatus(ModelConfig.TrainingStatus.COMPLETED);
                        result.setEndTime(LocalDateTime.now());
                        modelConfigRepository.save(config);
                        trainingResultRepository.save(result);
                    })
                    .exceptionally(throwable -> {
                        config.setStatus(ModelConfig.TrainingStatus.FAILED);
                        result.setEndTime(LocalDateTime.now());
                        result.setTrainingLogs("Training failed: " + throwable.getMessage());
                        modelConfigRepository.save(config);
                        return null;
                    });
        } catch (Exception e) {
            config.setStatus(ModelConfig.TrainingStatus.FAILED);
            result.setEndTime(LocalDateTime.now());
            result.setTrainingLogs("Training failed: " + e.getMessage());
            modelConfigRepository.save(config);
            throw e;
        }
    }

    private String[] createPythonScriptArgs(ModelConfig config) {
        return new String[]{
                "--algorithm", config.getAlgorithm().toString(),
                "--learning_rate", String.valueOf(config.getLearningRate()),
                "--num_epochs", String.valueOf(config.getNumEpochs()),
                "--batch_size", String.valueOf(config.getBatchSize()),
                "--momentum", String.valueOf(config.getMomentumValue()),
                "--weight_decay", String.valueOf(config.getWeightDecay()),
                "--scene_id", String.valueOf(config.getSceneId())
        };
    }

}