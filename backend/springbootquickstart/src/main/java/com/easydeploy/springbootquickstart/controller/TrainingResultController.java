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
import java.util.List;

@RestController
@RequestMapping("/api/training-results")
public class TrainingResultController {

    @Autowired
    private TrainingResultService trainingResultService;

    @GetMapping("/by-config/{modelConfigId}")
    public ResponseEntity<List<TrainingResult>> getTrainingResultsByModelConfig(@PathVariable Long modelConfigId) {
        try {
            List<TrainingResult> results = trainingResultService.getTrainingResultsByModelConfigId(modelConfigId);
            if (results.isEmpty()) {
                return ResponseEntity.noContent().build();
            }
            return ResponseEntity.ok(results);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(null);
        }
    }

    @GetMapping("/logs/{trainingResultId}")
    public ResponseEntity<?> getTrainingLogs(@PathVariable Long trainingResultId) {
        try {
            // 获取训练结果对象
            TrainingResult result = trainingResultService.getTrainingResult(trainingResultId);
            String relativeLogPath = result.getTrainingLogs();
            String baseDir = System.getProperty("user.dir");
            File logFile = new File(baseDir, relativeLogPath);

            // 检查日志文件是否存在
            if (!logFile.exists()) {
                return ResponseEntity.status(HttpStatus.NOT_FOUND)
                        .body("Log file not found at path: " + logFile.getAbsolutePath());
            }

            // 读取日志文件内容
            String logContent = new String(FileCopyUtils.copyToByteArray(logFile));

            return ResponseEntity.ok(logContent);
        } catch (IOException e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body("Error occurred while reading log file: " + e.getMessage());
        }
    }


    @GetMapping("/download/model/{trainingResultId}")
    public ResponseEntity<byte[]> downloadModelFile(@PathVariable Long trainingResultId) {
        try {
            TrainingResult result = trainingResultService.getTrainingResult(trainingResultId);
            String relativeModelPath = result.getModelFilePath();
            // Get the application's root directory
            String baseDir = System.getProperty("user.dir");
            // Construct absolute path by combining base directory with relative path
            File modelFile = new File(baseDir, relativeModelPath);

            if (!modelFile.exists()) {
                return ResponseEntity.status(HttpStatus.NOT_FOUND)
                        .body(("Model file not found at path: " + modelFile.getAbsolutePath()).getBytes());
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
            String relativeLogPath = result.getTrainingLogs();
            String baseDir = System.getProperty("user.dir");
            File logFile = new File(baseDir, relativeLogPath);

            if (!logFile.exists()) {
                return ResponseEntity.status(HttpStatus.NOT_FOUND)
                        .body(("Log file not found at path: " + logFile.getAbsolutePath()).getBytes());
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
