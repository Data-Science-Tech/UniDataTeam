package com.easydeploy.springbootquickstart.dto.request;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class UserRegisterDTO {
    @NotBlank(message = "Username cannot be blank")
    @Size(min = 2, max = 20, message = "Username must be between 2 and 20 characters")
    private String username;

    @NotBlank(message = "Password cannot be blank")
    @Size(min = 3, max = 20, message = "Password must be between 3 and 20 characters")
    private String password;
}
