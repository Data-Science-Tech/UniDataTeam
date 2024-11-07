package com.easydeploy.springbootquickstart.config;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Configuration;

import lombok.Data;

@Configuration
@ConfigurationProperties(prefix = "python")
@Data
public class PythonScriptConfig {
    private Script script;
    private Conda conda;

    @Data
    public static class Script {
        private String path;
        private String trainScript;
        private String predictScript;
    }

    @Data
    public static class Conda {
        private String envName;
        private String path;
    }
}