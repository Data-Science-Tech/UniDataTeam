package com.easydeploy.springbootquickstart.repository;

import com.easydeploy.springbootquickstart.model.ModelConfig;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ModelConfigRepository extends JpaRepository<ModelConfig, Long> {
}
