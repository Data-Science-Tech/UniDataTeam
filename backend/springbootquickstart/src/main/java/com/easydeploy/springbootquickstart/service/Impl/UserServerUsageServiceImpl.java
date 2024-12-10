package com.easydeploy.springbootquickstart.service.Impl;

import com.easydeploy.springbootquickstart.dto.response.UserServerUsageResponseDTO;
import com.easydeploy.springbootquickstart.model.ServerType;
import com.easydeploy.springbootquickstart.model.TrainingResult;
import com.easydeploy.springbootquickstart.model.UserServerUsage;
import com.easydeploy.springbootquickstart.model.ModelConfig; // 添加此行
import com.easydeploy.springbootquickstart.repository.ServerTypeRepository;
import com.easydeploy.springbootquickstart.repository.TrainingResultRepository;
import com.easydeploy.springbootquickstart.repository.UserServerUsageRepository;
import com.easydeploy.springbootquickstart.service.UserServerUsageService;
import jakarta.annotation.Resource;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@Service
public class UserServerUsageServiceImpl implements UserServerUsageService {
    @Resource
    private UserServerUsageRepository userServerUsageRepository;

    @Resource
    private ServerTypeRepository serverTypeRepository;

    @Resource
    private TrainingResultRepository trainingResultRepository;

    @Override
    public List<UserServerUsageResponseDTO> getUserServerUsageDetails(Long userId) {
        // 获取所有指定 userId 的 UserServerUsage 记录
        List<UserServerUsage> userServerUsages = userServerUsageRepository.findByUserId(userId);

        // 保存返回的数据
        List<UserServerUsageResponseDTO> responseDTOs = new ArrayList<>();

        for (UserServerUsage usage : userServerUsages) {
            UserServerUsageResponseDTO dto = new UserServerUsageResponseDTO();

            // 设置 UserServerUsage 的基本字段
            dto.setUserServerName(usage.getName());
            dto.setStatus(usage.getStatus());
            dto.setId(usage.getUsageId());

            System.out.println(usage.getServerType());
            // 获取 ServerType 数据
            Optional<ServerType> serverTypeOpt = serverTypeRepository.findById(usage.getServerType().getId());
            if (serverTypeOpt.isPresent()) {
                ServerType serverType = serverTypeOpt.get();
                dto.setServerTypeName(serverType.getName());
                dto.setPricePerHour(serverType.getPricePerHour());
                dto.setDescription(serverType.getDescription());
                dto.setGpuType(serverType.getGpuType());
                dto.setVCpuNum(serverType.getVCpuNum());
                dto.setRamSize(serverType.getRamSize());
            }

            // 获取 TrainingResult 数据
            Optional<TrainingResult> trainingResultOpt = trainingResultRepository.findById(usage.getTrainingResult().getId());
            if (trainingResultOpt.isPresent()) {
                TrainingResult trainingResult = trainingResultOpt.get();
                dto.setStartTime(trainingResult.getStartTime());
                dto.setEndTime(trainingResult.getEndTime());
                dto.setTrainingLogs(trainingResult.getTrainingLogs());
                dto.setModelFilePath(trainingResult.getModelFilePath());

                // 获取 ModelConfig 数据
                ModelConfig modelConfig = trainingResult.getModelConfig();
                dto.setAlgorithm(modelConfig.getAlgorithm().name());
                dto.setLearningRate(modelConfig.getLearningRate());
                dto.setNumEpochs(modelConfig.getNumEpochs());
                dto.setBatchSize(modelConfig.getBatchSize());
                dto.setMomentumValue(modelConfig.getMomentumValue());
                dto.setWeightDecay(modelConfig.getWeightDecay());
            }

            // 将数据添加到返回的 DTO 列表
            responseDTOs.add(dto);
        }

        return responseDTOs;
    }
}
