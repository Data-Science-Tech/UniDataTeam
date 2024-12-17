package com.easydeploy.springbootquickstart.controller.utils;

import com.easydeploy.springbootquickstart.model.SceneInfo;
import com.easydeploy.springbootquickstart.service.SceneInfoService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/sceneinfo")
public class SceneInfoController {
    @Autowired
    private SceneInfoService sceneInfoService;

    @GetMapping("/all")
    public List<SceneInfo> getAllSceneInfos()
    {
        return sceneInfoService.getAllSceneInfos();
    }

}
