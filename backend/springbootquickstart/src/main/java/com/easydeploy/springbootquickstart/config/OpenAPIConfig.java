package com.easydeploy.springbootquickstart.config;

import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.info.Contact;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class OpenAPIConfig {
    @Bean
    public OpenAPI customOpenAPI() {
        return new OpenAPI()
                .info(new Info()
                        .title("Car Perception API")
                        .version("1.0.0")
                        .description("Car Perception System API Documentation")
                        .contact(new Contact()
                                .name("Your Name")
                                .email("your.email@example.com")));
    }
}