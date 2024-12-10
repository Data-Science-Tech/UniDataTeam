package com.easydeploy.springbootquickstart.service.Impl;

import com.easydeploy.springbootquickstart.model.TrainingProcess;
import com.easydeploy.springbootquickstart.repository.TrainingProcessRepository;
import com.easydeploy.springbootquickstart.service.TrainingProcessService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class TrainingProcessImpl implements TrainingProcessService {

    @Autowired
    private TrainingProcessRepository trainingProcessRepository;

    @Override
    public List<TrainingProcess> getTrainingProcessesByUserServerUsageId(Integer userServerUsageId) {
        return trainingProcessRepository.findByUserServerUsageId(userServerUsageId);
    }
}
