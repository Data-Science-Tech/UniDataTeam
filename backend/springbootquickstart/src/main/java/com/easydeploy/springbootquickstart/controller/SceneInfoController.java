package com.easydeploy.springbootquickstart.controller;

import com.easydeploy.springbootquickstart.model.SceneInfo;
import com.easydeploy.springbootquickstart.service.SceneInfoService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import java.io.IOException;
import java.util.List;

@RestController
@RequestMapping("/api/scene-info")
public class SceneInfoController {
    @Autowired
    private SceneInfoService sceneInfoService;

    @GetMapping("/all")
    public List<SceneInfo> getAllSceneInfos()
    {
        return sceneInfoService.getAllSceneInfos();
    }

}
