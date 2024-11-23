package com.easydeploy.springbootquickstart.repository;

import com.easydeploy.springbootquickstart.model.SceneInfo;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface SceneInfoRepository extends JpaRepository<SceneInfo, Long> {

}
