package com.easydeploy.springbootquickstart.controller;

import com.easydeploy.springbootquickstart.model.TrainingProcess;
import com.easydeploy.springbootquickstart.service.TrainingProcessService;
import jakarta.annotation.Resource;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/monitoring")
@EnableAsync
public class TrainingMonitoringController {
    @Resource
    private TrainingProcessService trainingProcessService;

    @GetMapping("/training_process/{id}")
    public List<TrainingProcess> getTrainingProcessesByUserServerUsageId(@PathVariable("id") Integer userServerUsageId) {
        return trainingProcessService.getTrainingProcessesByUserServerUsageId(userServerUsageId);
    }
}
