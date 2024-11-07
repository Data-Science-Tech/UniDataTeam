package com.easydeploy.springbootquickstart.service;

import com.easydeploy.springbootquickstart.config.PythonScriptConfig;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.Resource;
import org.springframework.core.io.ResourceLoader;
import org.springframework.stereotype.Service;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.concurrent.CompletableFuture;

@Service
public class PythonScriptService {
    private static final Logger logger = LoggerFactory.getLogger(PythonScriptService.class);

    @Autowired
    private PythonScriptConfig config;

    @Autowired
    private ResourceLoader resourceLoader;

    private Path getScriptPath(String scriptName) throws IOException {
        // 首先尝试从resources目录加载
        String scriptPath = config.getScript().getPath() + scriptName;
        Resource resource = resourceLoader.getResource("classpath:" + scriptPath);

        if (resource.exists()) {
            // 如果脚本在jar包内，需要先复制到临时目录
            File tempFile = File.createTempFile(scriptName, ".py");
            Files.copy(resource.getInputStream(), tempFile.toPath(), StandardCopyOption.REPLACE_EXISTING);
            return tempFile.toPath();
        }

        // 如果不在resources中，尝试从外部目录加载
        Path externalPath = Paths.get(config.getScript().getPath(), scriptName);
        if (Files.exists(externalPath)) {
            return externalPath;
        }

        throw new IOException("Script not found: " + scriptName);
    }

    public CompletableFuture<Process> executeTrainingScript(String[] args) throws IOException {
        return executeScript(config.getScript().getTrainScript(), args);
    }

    public CompletableFuture<Process> executePredictionScript(String[] args) throws IOException {
        return executeScript(config.getScript().getPredictScript(), args);
    }

    private CompletableFuture<Process> executeScript(String scriptName, String[] args) throws IOException {
        Path scriptPath = getScriptPath(scriptName);

        // 构建命令列表
        List<String> command = new ArrayList<>();

        // 使用conda环境的Python解释器
        command.add(config.getConda().getPath());
        command.add(scriptPath.toString());

        // 添加参数
        command.addAll(Arrays.asList(args));

        // 创建进程构建器
        ProcessBuilder processBuilder = new ProcessBuilder(command);
        processBuilder.redirectErrorStream(true);

        // 设置工作目录为脚本所在目录
        processBuilder.directory(scriptPath.getParent().toFile());

        logger.info("Executing command: {}", String.join(" ", command));

        // 异步执行
        return CompletableFuture.supplyAsync(() -> {
            try {
                Process process = processBuilder.start();

                // 读取输出
                try (BufferedReader reader = new BufferedReader(
                        new InputStreamReader(process.getInputStream()))) {
                    String line;
                    while ((line = reader.readLine()) != null) {
                        logger.info("Python output: " + line);
                    }
                }

                // 等待进程完成
                int exitCode = process.waitFor();
                if (exitCode != 0) {
                    throw new RuntimeException("Python script failed with exit code: " + exitCode);
                }

                return process;
            } catch (IOException | InterruptedException e) {
                throw new RuntimeException("Failed to execute Python script", e);
            }
        });
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