package com.example.management.model;

import jakarta.persistence.*;
import java.util.Set;

@Entity
public class Student {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String firstName;

    private String lastName;

    private String email;

    private String enrollmentNumber;

    private String phoneNumber; // Add the phoneNumber field

    // Bi-directional Many-to-Many relationship with Course
    @ManyToMany
    @JoinTable(
            name = "student_courses",  // The name of the join table
            joinColumns = @JoinColumn(name = "student_id"), // Column for the student in the join table
            inverseJoinColumns = @JoinColumn(name = "course_id") // Column for the course in the join table
    )
    private Set<Course> courses;

    // Constructors
    public Student() {}

    public Student(String firstName, String lastName, String email, String enrollmentNumber, String phoneNumber) {
        this.firstName = firstName;
        this.lastName = lastName;
        this.email = email;
        this.enrollmentNumber = enrollmentNumber;
        this.phoneNumber = phoneNumber;  // Initialize phoneNumber
    }

    // Getters and Setters
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getFirstName() {
        return firstName;
    }

    public void setFirstName(String firstName) {
        this.firstName = firstName;
    }

    public String getLastName() {
        return lastName;
    }

    public void setLastName(String lastName) {
        this.lastName = lastName;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getEnrollmentNumber() {
        return enrollmentNumber;
    }

    public void setEnrollmentNumber(String enrollmentNumber) {
        this.enrollmentNumber = enrollmentNumber;
    }

    public String getPhoneNumber() {
        return phoneNumber;  // Getter for phoneNumber
    }

    public void setPhoneNumber(String phoneNumber) {
        this.phoneNumber = phoneNumber;  // Setter for phoneNumber
    }

    public Set<Course> getCourses() {
        return courses;
    }

    public void setCourses(Set<Course> courses) {
        this.courses = courses;
    }
}
