package com.easydeploy.springbootquickstart.service;

import com.easydeploy.springbootquickstart.model.SceneInfo;
import java.util.List;
import java.util.Set;

public interface SceneInfoService {
    List<SceneInfo> getAllSceneInfos();
    Set<SceneInfo> findAllById(List<Integer> sceneIds);
}
