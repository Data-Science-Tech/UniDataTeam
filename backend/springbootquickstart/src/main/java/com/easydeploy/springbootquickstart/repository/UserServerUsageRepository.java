package com.easydeploy.springbootquickstart.repository;

import com.easydeploy.springbootquickstart.model.UserServerUsage;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface    UserServerUsageRepository extends JpaRepository<UserServerUsage, Long> {

    List<UserServerUsage> findByUserId(Long userId);
}
