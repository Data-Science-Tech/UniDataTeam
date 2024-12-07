package com.easydeploy.springbootquickstart.repository;

import com.easydeploy.springbootquickstart.model.User;
import com.easydeploy.springbootquickstart.model.UserServerUsage;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface UserServerUsageRepository extends JpaRepository<User, Long> {

    List<UserServerUsage> findByUserId(Long userId);
}
