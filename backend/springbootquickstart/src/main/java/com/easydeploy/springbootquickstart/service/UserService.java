package com.easydeploy.springbootquickstart.service;

import com.easydeploy.springbootquickstart.dto.request.UserLoginDTO;
import com.easydeploy.springbootquickstart.dto.request.UserRegisterDTO;
import com.easydeploy.springbootquickstart.model.User;
import org.springframework.stereotype.Service;


public interface UserService {
    User login(UserLoginDTO loginDTO);
    void register(UserRegisterDTO requestDTO);
}
