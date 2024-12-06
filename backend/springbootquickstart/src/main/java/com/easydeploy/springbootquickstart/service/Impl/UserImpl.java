package com.easydeploy.springbootquickstart.service.Impl;

import com.easydeploy.springbootquickstart.model.User;
import com.easydeploy.springbootquickstart.repository.UserRepository;
import com.easydeploy.springbootquickstart.service.UserService;
import jakarta.annotation.Resource;
import org.springframework.security.crypto.password.PasswordEncoder;


public class UserImpl implements UserService {
    @Resource
    private UserRepository userRepository;

    @Resource
    private PasswordEncoder passwordEncoder;

    @Override
    public Boolean login(String username, String password) {
        User user = userRepository.findByUsername(username);

        if (user != null) {
            // 使用matches方法验证密码
            return passwordEncoder.matches(password, user.getPassword());
        }

        return false;
    }

    @Override
    public User register(User user) {
        if (userRepository.findByUsername(user.getUsername())!=null) {
            return null;
        } else {
            user.setPassword(passwordEncoder.encode(user.getPassword()));
            userRepository.save(user);
            return user;
        }
    }
}
