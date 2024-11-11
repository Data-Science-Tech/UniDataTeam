package com.easydeploy.springbootquickstart.controller;

import com.easydeploy.springbootquickstart.model.TrainingResult;
import com.easydeploy.springbootquickstart.service.TrainingResultService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.util.FileCopyUtils;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.io.File;
import java.io.IOException;

@RestController
@RequestMapping("/api/training-results")
public class TrainingResultController {

    @Autowired
    private TrainingResultService trainingResultService;

    @GetMapping("/download/model/{trainingResultId}")
    public ResponseEntity<byte[]> downloadModelFile(@PathVariable Long trainingResultId) {
        try {
            TrainingResult result = trainingResultService.getTrainingResult(trainingResultId);
            String modelFilePath = result.getModelFilePath();
            File modelFile = new File(modelFilePath);

            if (!modelFile.exists()) {
                return ResponseEntity.status(HttpStatus.NOT_FOUND)
                        .body(("Model file not found at path: " + modelFilePath).getBytes());
            }

            byte[] fileContent = FileCopyUtils.copyToByteArray(modelFile);
            HttpHeaders headers = new HttpHeaders();
            headers.add("Content-Disposition", "attachment; filename=" + modelFile.getName());

            return new ResponseEntity<>(fileContent, headers, HttpStatus.OK);
        } catch (IOException e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(("Error occurred while reading model file: " + e.getMessage()).getBytes());
        }
    }

    @GetMapping("/download/log/{trainingResultId}")
    public ResponseEntity<byte[]> downloadLogFile(@PathVariable Long trainingResultId) {
        try {
            TrainingResult result = trainingResultService.getTrainingResult(trainingResultId);
            String logFilePath = result.getTrainingLogs();
            File logFile = new File(logFilePath);

            if (!logFile.exists()) {
                return ResponseEntity.status(HttpStatus.NOT_FOUND)
                        .body(("Log file not found at path: " + logFilePath).getBytes());
            }

            byte[] fileContent = FileCopyUtils.copyToByteArray(logFile);
            HttpHeaders headers = new HttpHeaders();
            headers.add("Content-Disposition", "attachment; filename=" + logFile.getName());

            return new ResponseEntity<>(fileContent, headers, HttpStatus.OK);
        } catch (IOException e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(("Error occurred while reading log file: " + e.getMessage()).getBytes());
        }
    }
}
