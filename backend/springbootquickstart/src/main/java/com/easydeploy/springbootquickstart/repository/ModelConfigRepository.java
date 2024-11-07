package com.easydeploy.springbootquickstart.repository;

import com.easydeploy.springbootquickstart.model.ModelConfig;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ModelConfigRepository extends JpaRepository<ModelConfig, Long> {

    // 根据算法类型查找配置
    List<ModelConfig> findByAlgorithm(String algorithm);

    // 根据训练状态查找配置
    List<ModelConfig> findByStatus(ModelConfig.TrainingStatus status);

    // 根据场景id查找配置
    List<ModelConfig> findBySceneId(int sceneId);

    // 查找最近创建的配置
    @Query("SELECT m FROM ModelConfig m ORDER BY m.id DESC")
    List<ModelConfig> findRecentConfigs();

    // 根据学习率范围查找配置
    List<ModelConfig> findByLearningRateBetween(double minRate, double maxRate);

    // 检查是否存在正在运行的训练任务
    boolean existsByStatus(ModelConfig.TrainingStatus status);
}