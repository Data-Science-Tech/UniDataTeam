package com.easydeploy.springbootquickstart.service.Impl;

import com.easydeploy.springbootquickstart.config.PythonScriptConfig;
import com.easydeploy.springbootquickstart.service.PythonScriptService;
import com.easydeploy.springbootquickstart.websocket.TrainingProgressHandler;
import com.jcraft.jsch.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.io.InputStream;
import java.util.concurrent.CompletableFuture;

@Service
public class PythonScriptImpl implements PythonScriptService {
    private static final Logger logger = LoggerFactory.getLogger(PythonScriptImpl.class);

    @Autowired
    private PythonScriptConfig config;

    @Autowired
    private TrainingProgressHandler progressHandler;

    @Value("${remote.server.host}")
    private String remoteHost;

    @Value("${remote.server.port}")
    private int remotePort;

    @Value("${remote.server.username}")
    private String remoteUsername;

    @Value("${remote.server.password}")
    private String remotePassword;

    @Value("${docker.image.name}")
    private String dockerImageName;

    public CompletableFuture<Process> executeTrainingScript(String[] args) throws IOException {
        return executeScript(config.getScript().getTrainScript(), args);
    }

    public CompletableFuture<Process> executePredictionScript(String[] args) throws IOException {
        return executeScript(config.getScript().getPredictScript(), args);
    }

    // 简化DockerOutputReader，直接输出到控制台
    private static class DockerOutputReader implements Runnable {
        private final ChannelExec channel;
        private final InputStream in;
        private final String configId;
        private final TrainingProgressHandler progressHandler;

        public DockerOutputReader(ChannelExec channel, InputStream in, String configId, 
                                TrainingProgressHandler progressHandler) {
            this.channel = channel;
            this.in = in;
            this.configId = configId;
            this.progressHandler = progressHandler;
        }

        @Override
        public void run() {
            try {
                byte[] buffer = new byte[1024];
                while (!channel.isClosed()) {
                    while (in.available() > 0) {
                        int len = in.read(buffer, 0, buffer.length);
                        if (len < 0) break;
                        
                        String output = new String(buffer, 0, len);
                        System.out.print(output); // 直接打印到控制台
                        
                        // 只处理进度信息
                        if (output.contains("PROGRESS:")) {
                            String[] lines = output.split("\n");
                            for (String line : lines) {
                                if (line.startsWith("PROGRESS:")) {
                                    String progress = line.substring("PROGRESS:".length()).trim();
                                    progressHandler.sendProgressUpdate(configId, progress);
                                }
                            }
                        }
                    }
                    Thread.sleep(100);
                }
            } catch (Exception e) {
                System.err.println("读取输出时发生错误: " + e.getMessage());
            }
        }
    }

    private CompletableFuture<Process> executeScript(String scriptName, String[] args) throws IOException {
        return CompletableFuture.supplyAsync(() -> {
            Session session = null;
            ChannelExec channel = null;
            try {
                logger.info("开始连接训练服务器 {}:{}", remoteHost, remotePort);
                
                JSch jsch = new JSch();
                session = jsch.getSession(remoteUsername, remoteHost, remotePort);
                session.setPassword(remotePassword);
                
                // 设置JSch配置
                java.util.Properties config = new java.util.Properties();
                config.put("StrictHostKeyChecking", "no");
                // 添加这些配置以确保正确的输出处理
                config.put("PreferredAuthentications", "password");
                session.setConfig(config);
                
                // 设置连接超时时间为30秒
                session.setTimeout(30000);
                session.connect();
                logger.info("成功连接到训练服务器");

                // 修改Docker命令，移除-it参数（因为是非交互式执行）
                StringBuilder dockerCommand = new StringBuilder();
                dockerCommand.append("docker run -it -v /root/datasets:/app/datasets -v /mnt:/mnt -v /root:/root --rm --gpus all ")
                        .append(dockerImageName)
                        .append(" python3 train_model.py");

                // 添加参数
                for (String arg : args) {
                    dockerCommand.append(" ").append(arg);
                }
                
                logger.info("准备执行Docker命令: {}", dockerCommand);

                try {
                    channel = (ChannelExec) session.openChannel("exec");
                    
                    // 设置PTY以确保能获取到输出
                    ((ChannelExec) channel).setPty(true);
                    
                    channel.setCommand(dockerCommand.toString());
                    
                    // 获取输入流和错误流
                    InputStream in = channel.getInputStream();

                    channel.connect(5000);
                    logger.info("Docker命令开始执行");

                    String configId = extractConfigId(args);
                    
                    // 使用简化后的DockerOutputReader
                    Thread outputThread = new Thread(
                        new DockerOutputReader(channel, in, configId, progressHandler)
                    );
                    outputThread.start();

                    // 等待命令执行完成
                    outputThread.join();
                    
                    int exitStatus = channel.getExitStatus();
                    if (exitStatus != 0) {
                        throw new RuntimeException("Docker命令执行失败，退出码: " + exitStatus);
                    }

                    logger.info("Docker命令执行成功完成");
                    return null;

                } catch (Exception e) {
                    String errorMsg = "执行Docker命令时发生错误: " + e.getMessage();
                    logger.error(errorMsg, e);
                    throw new RuntimeException(errorMsg);
                }

            } catch (Exception e) {
                String errorMsg = "训练任务执行失败: " + e.getMessage();
                logger.error(errorMsg, e);
                throw new RuntimeException(errorMsg);
                
            } finally {
                if (channel != null && channel.isConnected()) {
                    channel.disconnect();
                    logger.info("已断开Docker命令通道");
                }
                if (session != null && session.isConnected()) {
                    session.disconnect();
                    logger.info("已断开训练服务器连接");
                }
            }
        });
    }

    public byte[] downloadFileFromServer(String remoteFilePath) throws JSchException, IOException {
        Session session = null;
        ChannelSftp channelSftp = null;
        try {
            JSch jsch = new JSch();
            session = jsch.getSession(remoteUsername, remoteHost, remotePort);
            session.setPassword(remotePassword);
            java.util.Properties config = new java.util.Properties();
            config.put("StrictHostKeyChecking", "no");
            session.setConfig(config);
            session.connect();

            channelSftp = (ChannelSftp) session.openChannel("sftp");
            channelSftp.connect();

            InputStream inputStream = null;
            byte[] fileContent = null;
            try {
                inputStream = channelSftp.get(remoteFilePath);
                fileContent = inputStream.readAllBytes();
                inputStream.close();
                return fileContent;
            } catch (SftpException e) {
                logger.error("Failed to download file from server", e);
                throw new IOException("Failed to download file from server", e);
            }
        } finally {
            if (channelSftp != null && channelSftp.isConnected()) {
                channelSftp.disconnect();
            }
            if (session != null && session.isConnected()) {
                session.disconnect();
            }
        }
    }

    private String extractConfigId(String[] args) {
        // 从参数中提取model_config_id
        for (int i = 0; i < args.length - 1; i++) {
            if (args[i].equals("--model_config_id")) {
                return args[i + 1];
            }
        }
        return null;
    }

    // 可选：添加检查conda环境是否可用的方法
    public boolean checkCondaEnvironment() {
        try {
            ProcessBuilder processBuilder = new ProcessBuilder(
                    config.getConda().getPath(), "--version"
            );
            Process process = processBuilder.start();
            int exitCode = process.waitFor();
            return exitCode == 0;
        } catch (IOException | InterruptedException e) {
            logger.error("Failed to check conda environment", e);
            return false;
        }
    }
}