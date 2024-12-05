package com.easydeploy.springbootquickstart.service.Impl;

import com.easydeploy.springbootquickstart.model.TrainingResult;
import com.easydeploy.springbootquickstart.repository.TrainingResultRepository;
import com.easydeploy.springbootquickstart.service.TrainingResultService;
import jakarta.transaction.Transactional;
import org.hibernate.Hibernate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class TrainingResultImpl implements TrainingResultService {

    @Autowired
    private TrainingResultRepository trainingResultRepository;

    public TrainingResult getTrainingResult(Long trainingResultId) {
        return trainingResultRepository.findById(trainingResultId)
                .orElseThrow(() -> new RuntimeException("Training result not found"));
    }

    @Transactional
    public List<TrainingResult> getTrainingResultsByModelConfigId(Long modelConfigId) {
        List<TrainingResult> results = trainingResultRepository.findByModelConfigId(modelConfigId);

        // 显式初始化懒加载的集合（确保 'scenes' 集合被加载）
        for (TrainingResult result : results) {
            if (result.getModelConfig() != null) {
                Hibernate.initialize(result.getModelConfig().getScenes());
            }
        }

        return results;
    }
}
