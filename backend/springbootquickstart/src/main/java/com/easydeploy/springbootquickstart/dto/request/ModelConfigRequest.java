package com.easydeploy.springbootquickstart.dto.request;

import lombok.Data;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import jakarta.validation.constraints.Size;
import java.util.List;

@Data
public class ModelConfigRequest {
    @NotNull(message = "算法名称不能为空")
    private String algorithm;

    @NotNull(message = "学习率不能为空")
    @Positive(message = "学习率必须大于0")
    private Double learningRate;

    @NotNull(message = "训练轮次不能为空")
    @Positive(message = "训练轮次必须大于0")
    private Integer numEpochs;

    @NotNull(message = "批次大小不能为空")
    @Positive(message = "批次大小必须大于0")
    private Integer batchSize;

    @NotNull(message = "动量值不能为空")
    private Double momentumValue;

    @NotNull(message = "权重衰减不能为空")
    private Double weightDecay;

    @NotEmpty(message = "场景ID列表不能为空")
    @Size(min = 1, message = "至少选择一个场景")
    private List<Integer> sceneIds;
}
