package com.easydeploy.springbootquickstart.service;

import com.easydeploy.springbootquickstart.model.TrainingProcess;

import java.util.List;

public interface TrainingProcessService {
    List<TrainingProcess> getTrainingProcessesByUserServerUsageId(Integer userServerUsageId);
}
