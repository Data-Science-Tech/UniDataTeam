package com.easydeploy.springbootquickstart.controller;

import com.easydeploy.springbootquickstart.dto.response.UserServerUsageResponseDTO;
import com.easydeploy.springbootquickstart.service.UserServerUsageService;
import jakarta.annotation.Resource;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;


@RestController
@RequestMapping("/api/tests")
public class UserServerUsageController {
    @Resource
    private UserServerUsageService userServerUsageService;

    @GetMapping("/{userId}")
    public ResponseEntity<List<UserServerUsageResponseDTO>> getUserServerUsageDetails(@PathVariable Long userId) {
        List<UserServerUsageResponseDTO> details = userServerUsageService.getUserServerUsageDetails(userId);
        return ResponseEntity.ok(details);
    }
}
