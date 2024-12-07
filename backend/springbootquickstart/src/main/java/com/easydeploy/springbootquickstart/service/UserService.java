package com.easydeploy.springbootquickstart.service;

import com.easydeploy.springbootquickstart.dto.request.UserLoginDTO;
import com.easydeploy.springbootquickstart.dto.request.UserRegisterDTO;
import com.easydeploy.springbootquickstart.model.User;
import jakarta.validation.constraints.NotNull;
import org.springframework.stereotype.Service;


public interface UserService {
    User login(UserLoginDTO loginDTO);
    void register(UserRegisterDTO requestDTO);
    User findById(@NotNull(message = "用户ID不能为空") int userId);
}
