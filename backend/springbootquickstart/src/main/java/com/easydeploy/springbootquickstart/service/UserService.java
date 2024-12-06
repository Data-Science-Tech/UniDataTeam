package com.easydeploy.springbootquickstart.service;

import com.easydeploy.springbootquickstart.model.User;

public interface UserService {
    Boolean login(String username, String password);
    User register(User user);
}
