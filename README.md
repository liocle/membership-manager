# **Membership Manager**  

## **📌 Project Overview**  
Membership Manager is a database-driven web application designed to streamline the management of a user base, including member records, subscriptions, and payment tracking. The goal of this project is to replace an outdated system with a modern, scalable, and automated solution that enhances efficiency in handling member data and communication.  

This project is a personal initiative to build a **robust, maintainable, and well-integrated system** for managing memberships while ensuring ease of access and data integrity.  

## **🛠️ Tech Stack**  

### **Backend**  
- **Python** (Core backend logic)  
- **FastAPI** (High-performance web framework for API development)  
- **SQLAlchemy** (ORM for database management)  
- **Alembic** (Database migrations and schema versioning)  
- **PostgreSQL** (Relational database for structured data storage)  

### **Infrastructure & Deployment**  
- **Docker & Docker Compose** (Containerized environment for easy deployment)  
- **GitHub Actions** (CI/CD for automated testing and integration)  

### **Testing & Development Tools**  
- **Pytest** (Unit and integration testing)  
- **pgAdmin** (Database administration)  

## **📌 Features Implemented**  
✅ **Database Design & Migrations**: Members, memberships, payment tracking  
✅ **Computed Fields**: Auto-generated `full_name` field for easy searchability  
✅ **Dockerized Environment**: Fully containerized setup for easy deployment  
✅ **Automated Testing**: CI pipeline with GitHub Actions & Pytest  
✅ **Database Seeding**: Script to populate test data for development  


### **🚀 Upcoming Features & Technologies**  
🔹 **Payment Data Import & Processing**: Script to update payment status from manually downloaded CSV files  
🔹 **Admin Dashboard** (React + TypeScript for user-friendly management)  
🔹 **Cloud Deployment** *(Hosting on AWS)*  
🔹 **User Authentication & Authorization** *(Tech to be considered in the future, depending on needs)*  
🔹 **Expanded Testing Coverage**:
  - **API Performance & Load Testing** *(e.g., Locust/k6 – to ensure the system handles multiple concurrent users efficiently)*  
  - **Security Testing** *(Basic authentication & database protection checks, tools like OWASP ZAP/Snyk)*  
  - **Automated Regression Testing** *(Set up in GitHub Actions to catch breaking changes before merging code)*  

