package com.example.management.service.impl;

import com.example.management.model.Course;
import com.example.management.repository.CourseRepository;
import com.example.management.service.CourseService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class CourseServiceImpl implements CourseService {

    @Autowired
    private CourseRepository courseRepository;

    @Override
    public Course addCourse(Course course) {
        return courseRepository.save(course);
    }

    @Override
    public List<Course> getAllCourses() {
        return courseRepository.findAll();
    }

    @Override
    public Course getCourseById(Long courseId) {
        Optional<Course> course = courseRepository.findById(courseId);
        return course.orElse(null); // If course not found, return null
    }

    @Override
    public Course updateCourse(Long courseId, Course course) {
        // First, check if the course exists
        Optional<Course> existingCourse = courseRepository.findById(courseId);
        if (existingCourse.isPresent()) {
            Course updatedCourse = existingCourse.get();
            updatedCourse.setCourseName(course.getCourseName());
            updatedCourse.setCreditHours(course.getCreditHours());
            updatedCourse.setDepartment(course.getDepartment());
            return courseRepository.save(updatedCourse);
        }
        return null; // Return null if the course is not found
    }

    @Override
    public void deleteCourse(Long courseId) {
        Optional<Course> existingCourse = courseRepository.findById(courseId);
        if (existingCourse.isPresent()) {
            courseRepository.deleteById(courseId); // Delete the course
        }
    }
}
