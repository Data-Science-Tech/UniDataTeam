package com.easydeploy.springbootquickstart.controller;

import com.easydeploy.springbootquickstart.model.TrainingProcess;
import com.easydeploy.springbootquickstart.service.TrainingProcessService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/training-process")
public class TrainingProcessController {

    @Autowired
    private TrainingProcessService trainingProcessService;

    @GetMapping("/user-server-usage/{id}")
    public List<TrainingProcess> getTrainingProcessesByUserServerUsageId(@PathVariable("id") Integer userServerUsageId) {
        return trainingProcessService.getTrainingProcessesByUserServerUsageId(userServerUsageId);
    }
}
