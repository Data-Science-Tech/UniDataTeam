package com.easydeploy.springbootquickstart.service.Impl;

import com.easydeploy.springbootquickstart.dto.response.UserServerUsageResponseDTO;
import com.easydeploy.springbootquickstart.model.ServerType;
import com.easydeploy.springbootquickstart.model.UserServerUsage;
import com.easydeploy.springbootquickstart.repository.ServerTypeRepository;
import com.easydeploy.springbootquickstart.repository.TrainingResultRepository;
import com.easydeploy.springbootquickstart.repository.UserServerUsageRepository;
import jakarta.annotation.Resource;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class UserServerUsageServiceImpl {
    @Resource
    private UserServerUsageRepository userServerUsageRepository;

    @Resource
    private ServerTypeRepository serverTypeRepository;

    @Resource
    private TrainingResultRepository trainingResultRepository;

    @Override
    public List<UserServerUsageResponseDTO> getUserServerUsageDetails(Long userId) {
        // 1. 获取所有指定 userId 的 UserServerUsage 记录
        List<UserServerUsage> userServerUsages = userServerUsageRepository.findByUserId(userId);

        // 2. 将每个 UserServerUsage 转换为 UserServerUsageResponseDTO
        List<UserServerUsageResponseDTO> responseDTOs = new ArrayList<>();

        for (UserServerUsage usage : userServerUsages) {
            UserServerUsageResponseDTO dto = new UserServerUsageResponseDTO();

            // 设置 UserServerUsage 的基本字段
            dto.setUserServerName(usage.getName());
            dto.setStatus(usage.getStatus());

            // 3. 获取 ServerType 数据
            Optional<ServerType> serverTypeOpt = serverTypeRepository.findById(usage.getServerType().getServerTypeId());
            if (serverTypeOpt.isPresent()) {
                ServerType serverType = serverTypeOpt.get();
                dto.setServerTypeName(serverType.getName());
                dto.setPricePerHour(serverType.getPricePerHour());
                dto.setDescription(serverType.getDescription());
                dto.setGpuType(serverType.getGpuType());
                dto.setVCpuNum(serverType.getVCpuNum());
                dto.setRamSize(serverType.getRamSize());
            }

            // 4. 获取 TrainingResult 数据
            Optional<TrainingResult> trainingResultOpt = trainingResultRepository.findById(usage.getTrainingResult().getId());
            if (trainingResultOpt.isPresent()) {
                TrainingResult trainingResult = trainingResultOpt.get();
                dto.setStartTime(trainingResult.getStartTime());
                dto.setEndTime(trainingResult.getEndTime());
                dto.setTrainingLogs(trainingResult.getTrainingLogs());
                dto.setModelFilePath(trainingResult.getModelFilePath());
            }

            // 5. 将数据添加到返回的 DTO 列表
            responseDTOs.add(dto);
        }

        return responseDTOs;
    }
}
