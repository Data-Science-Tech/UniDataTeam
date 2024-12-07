package com.easydeploy.springbootquickstart.service.Impl;

import com.easydeploy.springbootquickstart.dto.request.UserLoginDTO;
import com.easydeploy.springbootquickstart.dto.request.UserRegisterDTO;
import com.easydeploy.springbootquickstart.model.User;
import com.easydeploy.springbootquickstart.repository.UserRepository;
import com.easydeploy.springbootquickstart.service.UserService;
import jakarta.annotation.Resource;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
public class UserImpl implements UserService {
    @Resource
    private UserRepository userRepository;

    @Resource
    private PasswordEncoder passwordEncoder;

    @Override
    public User login(UserLoginDTO loginDTO) {
    // 查找用户
        User user = userRepository.findByUsername(loginDTO.getUsername());
        if (user == null) {
            throw new RuntimeException("用户不存在") ;
        }

        // 验证密码
        if (!passwordEncoder.matches(loginDTO.getPassword(), user.getPassword())) {
            throw new RuntimeException("密码错误");
        }

        // 生成登录Token（这里可以使用JWT）
        return user;
    }

    @Override
    public void register(UserRegisterDTO registerDTO) {
        // 检查用户名是否已存在
        if (userRepository.existsUserByUsername((registerDTO.getUsername()))) {
            throw new RuntimeException("用户名已存在");
        }

        // 创建新用户
        User newUser = new User();
        newUser.setUsername(registerDTO.getUsername());

        // 密码加密
        String encodedPassword = passwordEncoder.encode(registerDTO.getPassword());
        newUser.setPassword(encodedPassword);

        // 保存用户
        userRepository.save(newUser);
    }

    @Override
    public User findById(int userId) {
        return userRepository.findById(userId).orElse(null);
    }
}
