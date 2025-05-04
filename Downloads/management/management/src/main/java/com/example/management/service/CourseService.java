package com.example.management.service;

import com.example.management.model.Course;

import java.util.List;

public interface CourseService {

    // Method to add a course
    Course addCourse(Course course);

    // Optional: Method to get all courses
    List<Course> getAllCourses();

    // Optional: Method to get a course by ID
    Course getCourseById(Long courseId);

    // Optional: Method to update a course
    Course updateCourse(Long courseId, Course course);

    // Optional: Method to delete a course by ID
    void deleteCourse(Long courseId);
}
