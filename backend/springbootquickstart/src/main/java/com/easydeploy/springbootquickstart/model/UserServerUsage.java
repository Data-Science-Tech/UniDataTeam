package com.easydeploy.springbootquickstart.model;


import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

@Setter
@Getter
@Table(name = "user_server_usage")
@Entity
public class UserServerUsage {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer usageId;


    private Long userId;
    private String name;
    private String status;


    @ManyToOne
    @JoinColumn(name = "server_type_id")
    private ServerType serverType;

    @ManyToOne
    @JoinColumn(name = "result_id")
    private TrainingResult trainingResult;

}
