package com.easydeploy.springbootquickstart.repository;

import com.easydeploy.springbootquickstart.model.TrainingResult;
import com.easydeploy.springbootquickstart.model.ModelConfig;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface TrainingResultRepository extends JpaRepository<TrainingResult, Long> {

    // 根据配置ID查找训练结果
    List<TrainingResult> findByModelConfigId(Long modelConfigId);

    // 查找特定时间段内的训练结果
    List<TrainingResult> findByStartTimeBetween(LocalDateTime startTime, LocalDateTime endTime);

    // 查找特定配置的最新训练结果
    @Query("SELECT t FROM TrainingResult t WHERE t.modelConfig = ?1 ORDER BY t.endTime DESC")
    List<TrainingResult> findLatestResultForConfig(ModelConfig config);

    // 查找训练时间最短的结果
    @Query("SELECT t FROM TrainingResult t WHERE t.endTime IS NOT NULL ORDER BY (t.endTime - t.startTime) ASC")
    List<TrainingResult> findFastestTrainingResults();

    // 查找所有失败的训练（final_loss为null的记录）
    List<TrainingResult> findByFinalLossIsNull();

    // 删除特定配置的所有训练结果
    void deleteByModelConfigId(Long modelConfigId);
}