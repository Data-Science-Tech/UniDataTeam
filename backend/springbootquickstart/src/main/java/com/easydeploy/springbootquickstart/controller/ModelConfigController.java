package com.easydeploy.springbootquickstart.controller;

import com.easydeploy.springbootquickstart.model.ModelConfig;
import com.easydeploy.springbootquickstart.model.SceneInfo;
import com.easydeploy.springbootquickstart.model.User;
import com.easydeploy.springbootquickstart.service.ModelConfigService;
import com.easydeploy.springbootquickstart.service.SceneInfoService;
import com.easydeploy.springbootquickstart.dto.request.ModelConfigRequest;
import com.easydeploy.springbootquickstart.model.TrainingResult;
import com.easydeploy.springbootquickstart.repository.ServerTypeRepository;
import com.easydeploy.springbootquickstart.model.UserServerUsage;
import com.easydeploy.springbootquickstart.repository.UserServerUsageRepository;
import com.easydeploy.springbootquickstart.service.UserService;
import com.easydeploy.springbootquickstart.repository.TrainingResultRepository;
import jakarta.transaction.Transactional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.scheduling.annotation.Async;
import org.springframework.scheduling.annotation.EnableAsync;

import java.io.IOException;
import java.util.List;
import java.util.Set;

@RestController
@RequestMapping("/api/model-configs")
@EnableAsync
public class ModelConfigController {

    @Autowired
    private ModelConfigService modelConfigService;
    @Autowired
    private SceneInfoService sceneInfoService;

    @Autowired
    private TrainingResultRepository trainingResultRepository;
    @Autowired
    private UserServerUsageRepository userServerUsageRepository;
    @Autowired
    private ServerTypeRepository serverTypeRepository;
    @Autowired
    private UserService userService;

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

        // 设置 User (根据 userId 查找 User)
        User user = userService.findById(request.getUserId());
        if (user == null) {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }
        config.setUser(user);

        return ResponseEntity.ok(modelConfigService.createModelConfig(config));
    }
    

    @PostMapping("/{id}/train")
    public void startTraining(@PathVariable Long id, @RequestParam Long serverId, @RequestParam String taskName) throws IOException {
        modelConfigService.startTraining(id);
        UserServerUsage usage = new UserServerUsage();
        usage.setUsageId(null); // 让数据库自动生成ID
        usage.setUserId(modelConfigService.getModelConfig(id).getUser().getUserId().longValue());
        usage.setServerType(serverTypeRepository.findById(serverId.intValue()).orElseThrow(() -> new RuntimeException("Server not found")));
        usage.setStatus("RUNNING");
        usage.setName(taskName); // 设置训练任务名称
        userServerUsageRepository.save(usage);

        // 异步任务，1秒后更新 TrainingResult
        updateTrainingResult(id, usage);
    }

    @Async
    public void updateTrainingResult(Long configId, UserServerUsage usage) {
        try {
            Thread.sleep(1000);
            List<TrainingResult> trainingResults = trainingResultRepository.findByModelConfigId(configId);
            if (trainingResults != null && !trainingResults.isEmpty()) {
                usage.setTrainingResult(trainingResults.get(0)); // Assuming you want the first result
                userServerUsageRepository.save(usage);
            }
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    @Transactional
    @GetMapping("/user/{userId}")
    public ResponseEntity<List<ModelConfig>> getModelConfigByUserId(@PathVariable int userId) {
        List<ModelConfig> configs = modelConfigService.findByUserId(userId);
        return ResponseEntity.ok(configs);
    }

}