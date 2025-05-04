package com.example.management.dto;

import javax.validation.constraints.NotBlank;
import lombok.Data;

@Data
public class CourseDTO {
    private Long id;

    @NotBlank(message = "Course name is required")
    private String name;

    @NotBlank(message = "Course code is required")
    private String code;

    private String description;
} 