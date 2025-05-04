package com.example.management.controller;

import com.example.management.model.Student;
import com.example.management.service.StudentService;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/students")
public class StudentController {

    private final StudentService service;

    public StudentController(StudentService service) {
        this.service = service;
    }

    @PostMapping
    public Student create(@RequestBody Student student) {
        return service.createStudent(student);
    }

    @GetMapping("/{id}")
    public Student get(@PathVariable Long id) {
        return service.getStudentById(id);
    }

    @GetMapping
    public List<Student> list() {
        return service.getAllStudents();
    }
}
