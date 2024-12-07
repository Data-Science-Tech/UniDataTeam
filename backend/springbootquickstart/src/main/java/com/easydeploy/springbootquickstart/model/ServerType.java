package com.easydeploy.springbootquickstart.model;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.Getter;
import lombok.Setter;

@Setter
@Getter
@Table(name = "server_types")
@Entity
public class ServerType {
    @Id
    private Integer Id;

    private String name;
    private Double pricePerHour;
    private String description;
    private String gpuType;
    private Integer vCpuNum;
    private Integer ramSize;
}
