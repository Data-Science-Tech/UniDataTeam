package com.easydeploy.springbootquickstart.service;

import com.easydeploy.springbootquickstart.dto.response.UserServerUsageResponseDTO;

import java.util.List;

public interface UserServerUsageService {
    List<UserServerUsageResponseDTO> getUserServerUsageDetails(Long userId);
}
