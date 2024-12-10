package com.easydeploy.springbootquickstart.repository;

import com.easydeploy.springbootquickstart.model.TrainingProcess;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface TrainingProcessRepository extends JpaRepository<TrainingProcess, Long> {
    List<TrainingProcess> findByUserServerUsageId(Integer userServerUsageId);
}
