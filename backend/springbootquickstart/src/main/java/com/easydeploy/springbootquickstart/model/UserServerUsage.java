package com.easydeploy.springbootquickstart.model;


import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.Getter;
import lombok.Setter;

@Setter
@Getter
@Table(name = "user_server_usage")
@Entity
public class UserServerUsage {
    @Id
    private Long usageId;

    private Long userId;
    private String name;
    private String status;
    private Long serverTypeId;
    private Long resultId;

}
