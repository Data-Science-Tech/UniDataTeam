package com.easydeploy.springbootquickstart.repository;

import com.easydeploy.springbootquickstart.model.TrainingResult;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface TrainingResultRepository extends JpaRepository<TrainingResult, Long> {

    // 根据配置ID查找训练结果
    List<TrainingResult> findByModelConfigId(Long modelConfigId);

}