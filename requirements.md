**1) Project Description:**

Our web application is a Personality to Book matcher which allows users to sign in to a personal account using OAuth to take a short personality quiz, utilizing the 16 personalities test API to identify their personality type. The web app then matches this personality type with a predefined list of book genres (e.g., Inquisitive personality -\> Mystery genre). Utilizing the Goodreads API, the application recommends books within the matched genre to the user.

**2) Product Requirements:**

- **Goal:** To provide personalized book recommendations based on the user's personality type.
- **Non-Goal:** To provide an accurate/comprehensive psychological analysis or a detailed personality report.
- **Non-functional Requirement 1: Security**
  - **Functional Requirements:**
    1. Use OAuth authentication to access personal account.
    2. Securely store Goodreads api keys in local files without exposing them on github / the web.
- **Non-functional Requirement 2: Usability**
  - **Functional Requirements:**
    1. Have a clear interactive quiz interface that allows users to select answers to personality quiz (ability to review or change answers, progress indicators).
    2. Have a clear and personalized result dashboard which displays the user's personality type and book recommendations.
- **Non-functional Requirement 3: Repeatability**
  - **Functional requirements**:
    1. Previous personality types and book recommendations will be stored locally

**3) Project Management:**

- **Theme:** Provide a unique and entertaining experience by offering personalized book recommendations based on personality type.
- **Epic:** Personality to Book recommendation Website Beta
- **User Story 1:** As a user, I want to easily log into my account to take the personality quiz.
  - **Task:** Implement user account creation/login functionality
    - **Ticket 1:** Implement OAuth.
    - **Ticket 2:** Integrate the 16 personalities test API for the personality quiz.
- **User Story 2:** As a user, I want to see personalized book recommendations based on my quiz results so that I can find books that match my interests.
  - **Task:** Match personality types to genres and fetch book recommendations
    - **Ticket 1:** Create a mapping of personality types to book genres.
    - **Ticket 2:** Integrate the Goodreads API to fetch book recommendations based on the matched genre.
