package com.easydeploy.springbootquickstart.repository;

import com.easydeploy.springbootquickstart.model.SceneInfo;
import com.easydeploy.springbootquickstart.model.ServerType;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ServerTypeRepository extends JpaRepository<ServerType, Integer> {

}
