package com.easydeploy.springbootquickstart.service;

import com.easydeploy.springbootquickstart.model.TrainingResult;

import java.util.List;

public interface TrainingResultService {
    TrainingResult getTrainingResult(Long trainingResultId) ;
    List<TrainingResult> getTrainingResultsByModelConfigId(Long modelConfigId);
}
