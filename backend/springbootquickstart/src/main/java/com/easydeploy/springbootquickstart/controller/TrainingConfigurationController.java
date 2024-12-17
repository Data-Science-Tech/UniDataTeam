package com.easydeploy.springbootquickstart.controller;


import com.easydeploy.springbootquickstart.dto.request.ModelConfigRequest;
import com.easydeploy.springbootquickstart.model.*;
import com.easydeploy.springbootquickstart.repository.ServerTypeRepository;
import com.easydeploy.springbootquickstart.repository.TrainingResultRepository;
import com.easydeploy.springbootquickstart.repository.UserServerUsageRepository;
import com.easydeploy.springbootquickstart.service.ModelConfigService;
import com.easydeploy.springbootquickstart.service.SceneInfoService;
import com.easydeploy.springbootquickstart.service.UserService;
import jakarta.annotation.Resource;
import jakarta.transaction.Transactional;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.web.bind.annotation.*;

import java.io.IOException;
import java.util.List;
import java.util.Set;

@RestController
@RequestMapping("/api/configuration")
@EnableAsync
public class TrainingConfigurationController {
    @Resource
    private ModelConfigService modelConfigService;
    @Resource
    private SceneInfoService sceneInfoService;

    @Resource
    private TrainingResultRepository trainingResultRepository;
    @Resource
    private UserServerUsageRepository userServerUsageRepository;
    @Resource
    private ServerTypeRepository serverTypeRepository;
    @Resource
    private UserService userService;

    private static final Logger logger = LoggerFactory.getLogger(TrainingConfigurationController.class);

    // 创建配置
    @PostMapping("/create_config")
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

    // 根据model_id等参数进行训练
    @PostMapping("/train/{id}")
    public void startTraining(@PathVariable Long id, @RequestBody TrainingConfigurationController.TrainingRequest request) throws IOException {
        logger.info("Received serverId: {}", request.getServerId());

        // 创建 TrainingResult
        TrainingResult trainingResult = new TrainingResult();
        trainingResult.setModelConfig(modelConfigService.getModelConfig(id));
        trainingResult.setStartTime(java.time.LocalDateTime.now()); // 设置当前时间
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


    // 根据useid获取其配置的列表
    @Transactional
    @GetMapping("/find_model_config_by_userId/{userId}")
    public ResponseEntity<List<ModelConfig>> getModelConfigByUserId(@PathVariable int userId) {
        List<ModelConfig> configs = modelConfigService.findByUserId(userId);
        return ResponseEntity.ok(configs);
    }
}
