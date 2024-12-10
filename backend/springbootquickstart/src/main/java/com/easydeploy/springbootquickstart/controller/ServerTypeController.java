package com.easydeploy.springbootquickstart.controller;

import com.easydeploy.springbootquickstart.model.ServerType;
import com.easydeploy.springbootquickstart.service.ServerTypeService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import java.util.List;

@RestController
@RequestMapping("/api/server-types")
public class ServerTypeController {

    @Autowired
    private ServerTypeService serverTypeService;

    @GetMapping
    public List<ServerType> getAllServerTypes() {
        return serverTypeService.getAllServerTypes();
    }
}
