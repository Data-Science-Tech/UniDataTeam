package com.easydeploy.springbootquickstart.controller;

import com.easydeploy.springbootquickstart.dto.response.UserServerUsageResponseDTO;
import com.easydeploy.springbootquickstart.model.TrainingResult;
import com.easydeploy.springbootquickstart.service.PythonScriptService;
import com.easydeploy.springbootquickstart.service.TrainingResultService;
import com.easydeploy.springbootquickstart.service.UserServerUsageService;
import jakarta.annotation.Resource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.io.File;
import java.util.List;


@RestController
@RequestMapping("/api/task_management")
@EnableAsync
public class TaskManagementController {
    @Resource
    private TrainingResultService trainingResultService;

    @Resource
    private PythonScriptService pythonScriptService;

    @Resource
    private UserServerUsageService userServerUsageService;

    @GetMapping("/get_training_result_by_model_config/{modelConfigId}")
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
    @GetMapping("/get_training_logs_by_training_result_id/{trainingResultId}")
    public ResponseEntity<?> getTrainingLogs(@PathVariable Long trainingResultId) {
        try {
            TrainingResult result = trainingResultService.getTrainingResult(trainingResultId);
            String remoteLogPath = "/root/datasets/" + result.getTrainingLogs();

            byte[] logContent = pythonScriptService.downloadFileFromServer(remoteLogPath);
            String logContentStr = new String(logContent);
            return ResponseEntity.ok(logContentStr);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body("Error occurred while reading log file: " + e.getMessage());
        }
    }

    @GetMapping("/download_model_by_training_result_id/{trainingResultId}")
    public ResponseEntity<byte[]> downloadModelFile(@PathVariable Long trainingResultId) {
        try {
            TrainingResult result = trainingResultService.getTrainingResult(trainingResultId);
            String remoteModelPath = "/root/datasets/" + result.getModelFilePath();

            byte[] fileContent = pythonScriptService.downloadFileFromServer(remoteModelPath);
            HttpHeaders headers = new HttpHeaders();
            headers.add("Content-Disposition", "attachment; filename=" + new File(remoteModelPath).getName());

            return new ResponseEntity<>(fileContent, headers, HttpStatus.OK);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(("Error occurred while reading model file: " + e.getMessage()).getBytes());
        }
    }

    @GetMapping("/download_log_by_training_result_id/{trainingResultId}")
    public ResponseEntity<byte[]> downloadLogFile(@PathVariable Long trainingResultId) {
        try {
            TrainingResult result = trainingResultService.getTrainingResult(trainingResultId);
            String remoteLogPath = "/root/datasets/" + result.getTrainingLogs();

            byte[] fileContent = pythonScriptService.downloadFileFromServer(remoteLogPath);
            HttpHeaders headers = new HttpHeaders();
            headers.add("Content-Disposition", "attachment; filename=" + new File(remoteLogPath).getName());

            return new ResponseEntity<>(fileContent, headers, HttpStatus.OK);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(("Error occurred while reading log file: " + e.getMessage()).getBytes());
        }
    }

    @GetMapping("/get_user_server_usage_by_userid/{userId}")
    public ResponseEntity<List<UserServerUsageResponseDTO>> getUserServerUsageDetails(@PathVariable Long userId) {
        List<UserServerUsageResponseDTO> details = userServerUsageService.getUserServerUsageDetails(userId);
        return ResponseEntity.ok(details);
    }

    @GetMapping("/get_visualized_image_paths/{trainingResultId}")
    public ResponseEntity<List<String>> getVisualizedImagePaths(@PathVariable Long trainingResultId) {
        try {
            TrainingResult result = trainingResultService.getTrainingResult(trainingResultId);
            List<String> imagePaths = result.getVisualizedImages();
            if (imagePaths.isEmpty()) {
                return ResponseEntity.noContent().build();
            }
            return ResponseEntity.ok(imagePaths);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(null);
        }
    }
}
