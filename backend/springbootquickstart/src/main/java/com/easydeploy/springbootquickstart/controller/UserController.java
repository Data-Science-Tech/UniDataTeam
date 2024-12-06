package com.easydeploy.springbootquickstart.controller;

import com.easydeploy.springbootquickstart.dto.request.UserLoginDTO;
import com.easydeploy.springbootquickstart.dto.request.UserRegisterDTO;
import com.easydeploy.springbootquickstart.model.User;
import com.easydeploy.springbootquickstart.service.UserService;
import jakarta.annotation.Resource;
import jakarta.servlet.http.HttpSession;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;


@RestController
@RequestMapping("/api/users")
public class UserController {
    @Resource
    private UserService userService;

    @PostMapping("/register")
    public ResponseEntity<?> registerUser(@Valid @RequestBody UserRegisterDTO registerDTO) {
        try {
            // 注册用户
            userService.register(registerDTO);
            return ResponseEntity.ok().body("用户注册成功");
        } catch (Exception e) {
            return ResponseEntity
                    .status(HttpStatus.BAD_REQUEST)
                    .body("注册失败：" + e.getMessage());
        }
    }

    @PostMapping("/login")
    public ResponseEntity<?> loginUser(@Valid @RequestBody UserLoginDTO loginDTO, HttpSession session) {
        try {
            // 登录验证
            User user = userService.login(loginDTO);

            // 将用户信息存入Session
            session.setAttribute("user", user);

            // 返回用户基本信息（不包含敏感信息）
            Map<String, Object> userInfo = new HashMap<>();
            userInfo.put("id", user.getUserId());
            userInfo.put("username", user.getUsername());

            return ResponseEntity.ok(userInfo);
        } catch (Exception e) {
            return ResponseEntity
                    .status(HttpStatus.UNAUTHORIZED)
                    .body("登录失败：" + e.getMessage());
        }
    }

    @PostMapping("/logout")
    public ResponseEntity<?> logout(HttpSession session) {
        // 使Session失效
        session.invalidate();
        return ResponseEntity.ok("退出成功");
    }

    // 获取当前用户信息
    @GetMapping("/current")
    public ResponseEntity<?> getCurrentUser(HttpSession session) {
        User user = (User) session.getAttribute("user");
        if (user == null) {
            return ResponseEntity
                    .status(HttpStatus.UNAUTHORIZED)
                    .body("用户未登录");
        }

        // 返回非敏感信息
        Map<String, Object> userInfo = new HashMap<>();
        userInfo.put("id", user.getUserId());
        userInfo.put("username", user.getUsername());

        return ResponseEntity.ok(userInfo);
    }
}
