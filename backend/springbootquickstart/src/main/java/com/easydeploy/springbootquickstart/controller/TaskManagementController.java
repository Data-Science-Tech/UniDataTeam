package com.easydeploy.springbootquickstart.controller;

import com.easydeploy.springbootquickstart.dto.response.UserServerUsageResponseDTO;
import com.easydeploy.springbootquickstart.model.TrainingResult;
import com.easydeploy.springbootquickstart.service.PythonScriptService;
import com.easydeploy.springbootquickstart.service.TrainingResultService;
import com.easydeploy.springbootquickstart.service.UserServerUsageService;
import jakarta.annotation.Resource;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.io.File;
import java.util.*;


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

    private static final Logger logger = LoggerFactory.getLogger(TaskManagementController.class);

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

    @GetMapping("/get_visualized_images/{trainingResultId}")
    public ResponseEntity<?> getVisualizedImages(@PathVariable Long trainingResultId) {
        try {
            TrainingResult result = trainingResultService.getTrainingResult(trainingResultId);
            if (result == null) {
                logger.error("Training result not found for ID: {}", trainingResultId);
                return ResponseEntity.notFound().build();
            }

            List<String> imagePaths = result.getVisualizedImages();
            if (imagePaths == null || imagePaths.isEmpty()) {
                logger.info("No visualized images found for training result ID: {}", trainingResultId);
                return ResponseEntity.noContent().build();
            }

            List<Map<String, Object>> response = new ArrayList<>();
            for (String imagePath : imagePaths) {
                try {
                    String remoteImagePath = "/root/datasets/" + imagePath;
                    byte[] imageContent = pythonScriptService.downloadFileFromServer(remoteImagePath);

                    Map<String, Object> imageData = new HashMap<>();
                    imageData.put("path", imagePath);
                    imageData.put("data", Base64.getEncoder().encodeToString(imageContent));
                    response.add(imageData);
                } catch (Exception e) {
                    logger.error("Error processing image {}: {}", imagePath, e.getMessage());
                    // 继续处理下一张图片
                }
            }

            if (response.isEmpty()) {
                return ResponseEntity.noContent().build();
            }

            return ResponseEntity.ok(response);
        } catch (Exception e) {
            logger.error("Error getting visualized images for training result {}: {}", trainingResultId, e.getMessage(), e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(Collections.singletonMap("error", e.getMessage()));
        }
    }

}
