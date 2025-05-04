package com.example.management.service;

import com.example.management.model.Student;
import java.util.List;

public interface StudentService {
    Student createStudent(Student student);
    Student getStudentById(Long id);
    Student getStudentByEmail(String email);
    Student getStudentByEnrollmentNumber(String enrollmentNumber);
    List<Student> getAllStudents();
    Student updateStudent(Long id, Student student);
    void deleteStudent(Long id);
}
