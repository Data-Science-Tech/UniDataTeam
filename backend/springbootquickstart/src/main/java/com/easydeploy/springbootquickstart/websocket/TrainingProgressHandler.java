package com.easydeploy.springbootquickstart.websocket;

import org.jetbrains.annotations.NotNull;
import org.springframework.stereotype.Component;
import org.springframework.web.socket.CloseStatus;
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.handler.TextWebSocketHandler;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.util.Map;
import java.util.Objects;
import java.util.concurrent.ConcurrentHashMap;

@Component
public class TrainingProgressHandler extends TextWebSocketHandler {
    private static final Map<String, WebSocketSession> sessions = new ConcurrentHashMap<>();
    private static final Logger logger = LoggerFactory.getLogger(TrainingProgressHandler.class);

    @Override
    public void afterConnectionEstablished(@NotNull WebSocketSession session) {
        // 从URI中获取configId
        String uri = Objects.requireNonNull(session.getUri()).getPath();
        String configId = extractConfigId(uri);
        if (configId != null) {
            // 可以将configId存储在session的attributes中
            session.getAttributes().put("configId", configId);
        }
        sessions.put(session.getId(), session);
        System.out.println("WebSocket connection established. " +
                "Session ID: " + session.getId() + ", Config ID: " + configId);
    }

    @Override
    public void afterConnectionClosed(@NotNull WebSocketSession session, @NotNull CloseStatus status) {
        sessions.remove(session.getId());
        System.out.println("WebSocket connection closed. Session ID: " + session.getId());
    }

    public void sendProgressUpdate(String configId, String message) {
        sessions.values().forEach(session -> {
            try {
                // 检查这个session是否对应请求的configId
                String sessionConfigId = (String) session.getAttributes().get("configId");
                if (configId.equals(sessionConfigId)) {
                    session.sendMessage(new TextMessage(message));
                }
            } catch (IOException e) {
                logger.error(e.getMessage());
            }
        });
    }

    private String extractConfigId(String uri) {
        // 从 /ws/training-progress/16 这样的URI中提取16
        String[] parts = uri.split("/");
        if (parts.length > 0) {
            return parts[parts.length - 1];
        }
        return null;
    }
}
