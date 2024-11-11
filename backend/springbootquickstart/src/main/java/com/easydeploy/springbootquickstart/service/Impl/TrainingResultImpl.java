package com.easydeploy.springbootquickstart.service.Impl;

import com.easydeploy.springbootquickstart.model.TrainingResult;
import com.easydeploy.springbootquickstart.repository.TrainingResultRepository;
import com.easydeploy.springbootquickstart.service.TrainingResultService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class TrainingResultImpl implements TrainingResultService {

    @Autowired
    private TrainingResultRepository trainingResultRepository;

    public TrainingResult getTrainingResult(Long trainingResultId) {
        return trainingResultRepository.findById(trainingResultId)
                .orElseThrow(() -> new RuntimeException("Training result not found"));
    }
}
