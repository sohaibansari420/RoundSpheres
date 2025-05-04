package com.example.management.controller;

import com.example.management.model.Course;
import com.example.management.model.Student;
import com.example.management.service.CourseService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/courses")
public class CourseController {

    private final CourseService courseService;

    @Autowired
    public CourseController(CourseService courseService) {
        this.courseService = courseService;
    }

    @PostMapping
    public Course addCourse(@RequestBody Course course) {
        return courseService.addCourse(course); // Calling the addCourse method
    }

    @GetMapping
    public List<Course> list() {
        return courseService.getAllCourses();
    }
}
