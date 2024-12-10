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
import org.springframework.scheduling.annotation.EnableAsync;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

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

    private static final Logger logger = LoggerFactory.getLogger(ModelConfigController.class);

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
    
    public static class TrainingRequest {
        private Long serverId;
        private String taskName;

        // Getters and setters
        public Long getServerId() {
            return serverId;
        }

        public void setServerId(Long serverId) {
            this.serverId = serverId;
        }

        public String getTaskName() {
            return taskName;
        }

        public void setTaskName(String taskName) {
            this.taskName = taskName;
        }
    }

    @PostMapping("/{id}/train")
    public void startTraining(@PathVariable Long id, @RequestBody TrainingRequest request) throws IOException {
        logger.info("Received serverId: {}", request.getServerId());
        
        // 创建 TrainingResult
        TrainingResult trainingResult = new TrainingResult();
        trainingResult.setModelConfig(modelConfigService.getModelConfig(id));
        trainingResultRepository.save(trainingResult);

        // 创建 UserServerUsage
        UserServerUsage usage = new UserServerUsage();
        usage.setUsageId(null); // 让数据库自动生成ID
        usage.setUserId(modelConfigService.getModelConfig(id).getUser().getUserId().longValue());
        usage.setServerType(serverTypeRepository.findById(request.getServerId().intValue()).orElseThrow(() -> new RuntimeException("Server not found")));
        usage.setStatus("RUNNING");
        usage.setName(request.getTaskName()); // 设置训练任务名称
        usage.setTrainingResult(trainingResult); // 设置训练结果
        userServerUsageRepository.save(usage);

        // 开始训练
        modelConfigService.startTraining(id, trainingResult.getId(), usage); // 传递 usage 对象
    }

    @Transactional
    @GetMapping("/user/{userId}")
    public ResponseEntity<List<ModelConfig>> getModelConfigByUserId(@PathVariable int userId) {
        List<ModelConfig> configs = modelConfigService.findByUserId(userId);
        return ResponseEntity.ok(configs);
    }

}