package com.easydeploy.springbootquickstart.dto.response;

import lombok.Data;

import java.time.LocalDateTime;

@Data
public class UserServerUsageResponseDTO {
    private Integer Id;
    private String userServerName;
    private String status;
    private String serverTypeName;
    private Double pricePerHour;
    private String description;
    private String gpuType;
    private Integer vCpuNum;
    private Integer ramSize;
    private LocalDateTime startTime;
    private LocalDateTime endTime;
    private String trainingLogs;
    private String modelFilePath;
}
