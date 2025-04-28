# Manual Testing Flow

This document outlines the steps for manually testing the core features of the Kanban + Post Management application based on the current project progress.

**Target Users/Roles:**

*   **New User:** A user who hasn't registered yet.
*   **Regular User:** A standard registered user without admin privileges.
*   **Admin User:** A user with `is_admin=True` (e.g., the Superuser).

**Prerequisites:**

1.  The Django development server is running (`python manage.py runserver`).
2.  You have the credentials for the Admin User (Superuser).
3.  Have a sample image file ready (e.g., `.jpg`, `.png`) for testing post image uploads.
4.  Have a sample document file ready (e.g., `.pdf`, `.txt`, `.docx`) for testing task attachments.
5.  The application should be accessible in a web browser (usually `http://127.0.0.1:8000/`).
6.  The root URL (`/`) should redirect to the Kanban board (`/tasks/`).

---

## I. Authentication & User Management

**Scenario 1: New User Registration**

*   **Actor:** New User
*   **Preconditions:** None
*   **Steps:**
    1.  Navigate to the signup page (e.g., `/users/signup/`).
    2.  Fill in the registration form with a unique username, email, and a password (confirm password).
    3.  Submit the form.
*   **Expected Result:**
    *   User is successfully registered.
    *   User is redirected to the login page (`/users/login/`) or the Kanban board (`/tasks/`) as configured by `LOGIN_REDIRECT_URL` after login.
    *   Attempting to register again with the *same* username or email should display validation errors on the form.

**Scenario 2: User Login & Logout**

*   **Actor:** Regular User
*   **Preconditions:** User account created in Scenario 1 exists.
*   **Steps:**
    1.  Navigate to the login page (`/users/login/`).
    2.  Enter the credentials (username/password) of the user created in Scenario 1.
    3.  Submit the form.
    4.  Verify successful login (e.g., username displayed, redirected to `/tasks/`).
    5.  Find and click the "Logout" link/button.
*   **Expected Result:**
    *   User is successfully logged in and redirected to the Kanban board (`/tasks/`).
    *   User-specific elements (like username, logout link) are visible in the base template/navigation.
    *   User is successfully logged out and redirected (likely to the login page or home page as per `LOGOUT_REDIRECT_URL`).
    *   Attempting to log in with incorrect credentials should display an error message on the login form.

**Scenario 3: Admin Login**

*   **Actor:** Admin User
*   **Preconditions:** Superuser account exists.
*   **Steps:**
    1.  Navigate to the login page (`/users/login/`).
    2.  Enter the Superuser credentials.
    3.  Submit the form.
*   **Expected Result:**
    *   Admin user is successfully logged in and redirected to the Kanban board (`/tasks/`).
    *   Admin user should have access to the Django admin interface (`/admin/`).

---

## II. Post Management (as Regular User)

**Scenario 4: Create Post (No Image)**

*   **Actor:** Regular User
*   **Preconditions:** Logged in as a Regular User.
*   **Steps:**
    1.  Navigate to the "Create Post" page (find the link, likely `/posts/new/`).
    2.  Enter a title and content for the post.
    3.  Leave the image field empty.
    4.  Submit the form.
*   **Expected Result:**
    *   Post is created successfully.
    *   User is redirected to the post detail page (`/posts/<post_id>/`) or the post list page (`/posts/`).
    *   The new post appears correctly on the post list page.
    *   The post detail page shows the correct title and content, and indicates no image.

**Scenario 5: Create Post (With Image)**

*   **Actor:** Regular User
*   **Preconditions:** Logged in as a Regular User. Have a sample image file.
*   **Steps:**
    1.  Navigate to the "Create Post" page (`/posts/new/`).
    2.  Enter a title and content.
    3.  Use the file input to select and upload the sample image file.
    4.  Submit the form.
*   **Expected Result:**
    *   Post is created successfully.
    *   User is redirected to the post detail page or list page.
    *   The new post appears on the post list page.
    *   The post detail page shows the correct title, content, and the uploaded image is displayed correctly.

**Scenario 6: View Posts**

*   **Actor:** Regular User / Admin User
*   **Preconditions:** Logged in. At least one post exists.
*   **Steps:**
    1.  Navigate to the post list page (`/posts/`).
    2.  Verify that existing posts are listed.
    3.  Click on the title or a "View" link for a specific post.
*   **Expected Result:**
    *   The post list page displays titles/previews of existing posts.
    *   Clicking a post leads to its detail page (`/posts/<post_id>/`).
    *   The detail page shows the full title, content, author, timestamp, and image (if one exists).

**Scenario 7: Update Own Post**

*   **Actor:** Regular User
*   **Preconditions:** Logged in as the user who created the post.
*   **Steps:**
    1.  Navigate to the detail page of a post created by the logged-in user.
    2.  Find and click the "Edit" or "Update" link/button (likely `/posts/<post_id>/edit/`).
    3.  Modify the title, content, or change/add/remove the image.
    4.  Submit the form.
*   **Expected Result:**
    *   The post is updated successfully.
    *   User is redirected to the post detail page.
    *   The detail page reflects the changes made to the title, content, and/or image.

**Scenario 8: Delete Own Post**

*   **Actor:** Regular User
*   **Preconditions:** Logged in as the user who created the post.
*   **Steps:**
    1.  Navigate to the detail page of a post created by the logged-in user.
    2.  Find and click the "Delete" link/button (likely `/posts/<post_id>/delete/`).
    3.  A confirmation page should appear. Confirm the deletion.
*   **Expected Result:**
    *   The post is deleted successfully.
    *   User is redirected to the post list page (`/posts/`).
    *   The deleted post no longer appears in the list.

---

## III. Post Management (Permissions)

**Scenario 9: Attempt to Update Another User's Post**

*   **Actor:** Regular User B
*   **Preconditions:**
    *   User A exists and has created a post.
    *   User B exists and is logged in.
*   **Steps:**
    1.  Log in as User B.
    2.  Navigate to the detail page of the post created by User A.
*   **Expected Result:**
    *   The "Edit" or "Update" link/button should *not* be visible or accessible for User B on User A's post.
    *   Attempting to directly access the edit URL (`/posts/<post_id_A>/edit/`) should result in an error (e.g., 403 Forbidden or redirect).

**Scenario 10: Attempt to Delete Another User's Post**

*   **Actor:** Regular User B
*   **Preconditions:**
    *   User A exists and has created a post.
    *   User B exists and is logged in.
*   **Steps:**
    1.  Log in as User B.
    2.  Navigate to the detail page of the post created by User A.
*   **Expected Result:**
    *   The "Delete" link/button should *not* be visible or accessible for User B on User A's post.
    *   Attempting to directly access the delete URL (`/posts/<post_id_A>/delete/`) should result in an error (e.g., 403 Forbidden or redirect).

---

## IV. Task Management (Kanban & Details)

**Scenario 11: Admin Creates & Assigns Task**

*   **Actor:** Admin User
*   **Preconditions:** Logged in as Admin User. At least one Regular User exists.
*   **Steps:**
    1.  Navigate to the Kanban board (`/tasks/`).
    2.  Find and click the "Create Task" link/button (e.g., `/tasks/new/`).
    3.  Fill in the task form: title, description.
    4.  Select a Regular User from the "Assign To" dropdown/selector.
    5.  Submit the form.
*   **Expected Result:**
    *   Task is created successfully.
    *   User is redirected back to the Kanban board (`/tasks/`).
    *   The new task appears as a card in the "TODO" column, showing at least the title and assigned user.

**Scenario 12: Regular User Views Kanban Board**

*   **Actor:** Regular User
*   **Preconditions:** Logged in as the Regular User who was assigned a task in Scenario 11.
*   **Steps:**
    1.  Navigate to the Kanban board (`/tasks/`).
*   **Expected Result:**
    *   The Kanban board displays columns (TODO, INPROGRESS, DONE).
    *   The task assigned to this user is visible in the "TODO" column.
    *   Tasks assigned to other users (if any) should also be visible.

**Scenario 13: View Task Details**

*   **Actor:** Regular User / Admin User
*   **Preconditions:** Logged in. A task exists on the board.
*   **Steps:**
    1.  Navigate to the Kanban board (`/tasks/`).
    2.  Click on the title or a "View Details" link on a task card.
*   **Expected Result:**
    *   User is redirected to the task detail page (`/tasks/<task_id>/`).
    *   The page displays the task's title, description, status, assigned user, creator, and timestamps.
    *   Sections for viewing existing comments and attachments are present.
    *   Forms for adding new comments and attachments are present.

**Scenario 14: Add Comment to Task**

*   **Actor:** Regular User / Admin User
*   **Preconditions:** Logged in. Viewing a task detail page (`/tasks/<task_id>/`).
*   **Steps:**
    1.  Find the "Add Comment" form on the task detail page.
    2.  Enter text into the comment field.
    3.  Submit the comment form.
*   **Expected Result:**
    *   The page refreshes or updates.
    *   The new comment appears in the comments section, showing the comment text, the user who posted it, and the timestamp.

**Scenario 15: Add Attachment to Task**

*   **Actor:** Regular User / Admin User
*   **Preconditions:** Logged in. Viewing a task detail page (`/tasks/<task_id>/`). Have a sample document file.
*   **Steps:**
    1.  Find the "Add Attachment" form on the task detail page.
    2.  Use the file input to select the sample document file.
    3.  Submit the attachment form.
*   **Expected Result:**
    *   The page refreshes or updates.
    *   The new attachment appears in the attachments section, showing the filename and potentially the upload time/user.
    *   The filename should be a link. Clicking the link should allow viewing/downloading the uploaded file (check `/media/...` URL).

**Scenario 16: Update Task Status (Backend Test)**

*   **Actor:** Admin User / Assigned Regular User
*   **Preconditions:** Logged in as Admin or the user assigned to the task. Task exists in 'TODO' status. *Note: Frontend drag-and-drop (Task 4.6) was skipped, so this tests the backend view directly if accessible, or indirectly via any basic UI element provided.*
*   **Steps:**
    1.  Identify how to trigger the status update view (`TaskUpdateStatusView`). This might be via the task detail page if buttons/forms were added, or might require manual URL access if purely backend.
    2.  Trigger an update to change the status from 'TODO' to 'INPROGRESS'.
    3.  Verify the change: Navigate back to the Kanban board (`/tasks/`).
    4.  Trigger an update to change the status from 'INPROGRESS' to 'DONE'.
    5.  Verify the change: Navigate back to the Kanban board (`/tasks/`).
*   **Expected Result:**
    *   The backend view successfully updates the task's status in the database.
    *   On the Kanban board, the task card moves to the 'INPROGRESS' column after the first update.
    *   On the Kanban board, the task card moves to the 'DONE' column after the second update.

---

## V. Task Management (Permissions)

**Scenario 17: Non-Admin Attempts Task Creation**

*   **Actor:** Regular User
*   **Preconditions:** Logged in as a Regular User (not Admin).
*   **Steps:**
    1.  Attempt to find a "Create Task" link/button on the Kanban board or elsewhere.
    2.  Attempt to directly access the task creation URL (`/tasks/new/`).
*   **Expected Result:**
    *   The "Create Task" link/button should not be visible to the Regular User.
    *   Accessing the URL directly should result in an error (e.g., 403 Forbidden or redirect to login/home).

**Scenario 18: Non-Assignee/Non-Admin Attempts Status Update**

*   **Actor:** Regular User B
*   **Preconditions:**
    *   Task exists and is assigned to User A.
    *   User B is logged in (and is not an Admin).
*   **Steps:**
    1.  Attempt to access the status update mechanism (see Scenario 16 steps) for the task assigned to User A.
*   **Expected Result:**
    *   User B should not be able to see controls to update the status of User A's task.
    *   Attempting to trigger the update via direct URL access (if possible) should result in an error (e.g., 403 Forbidden).

---