package com.easydeploy.springbootquickstart.config;

import com.easydeploy.springbootquickstart.websocket.TrainingProgressHandler;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.socket.config.annotation.EnableWebSocket;
import org.springframework.web.socket.config.annotation.WebSocketConfigurer;
import org.springframework.web.socket.config.annotation.WebSocketHandlerRegistry;

@Configuration
@EnableWebSocket
public class WebSocketConfig implements WebSocketConfigurer {

    @Autowired
    private TrainingProgressHandler trainingProgressHandler;

    @Override
    public void registerWebSocketHandlers(WebSocketHandlerRegistry registry) {
        registry.addHandler(trainingProgressHandler, "/ws/training-progress/**")
                .setAllowedOrigins("*");  // 实际生产环境要限制允许的源
    }

}
