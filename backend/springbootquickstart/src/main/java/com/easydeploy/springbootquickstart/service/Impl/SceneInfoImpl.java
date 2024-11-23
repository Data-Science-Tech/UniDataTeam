package com.easydeploy.springbootquickstart.service.Impl;

import com.easydeploy.springbootquickstart.model.SceneInfo;
import com.easydeploy.springbootquickstart.repository.SceneInfoRepository;
import com.easydeploy.springbootquickstart.service.SceneInfoService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class SceneInfoImpl implements SceneInfoService {
    @Autowired
    private SceneInfoRepository sceneInfoRepository;

    @Override
    public List<SceneInfo> getAllSceneInfos() {
        return sceneInfoRepository.findAll();
    }
}
