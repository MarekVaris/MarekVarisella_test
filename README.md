1. SETUP PROJECT

   Requirements:
   - python >= 3.11
   - django >= 5
   - sqlite3
   
   python manage.py migrate
   python example_init.py 

2. Create git repository and add all files.
3. Create new branch in format `firstName-lastName`.
4. TASKS

   1. All task are in project files. 
      Please do only tasks matching below rule
      # TODO:\sTASK\s+→\s+[^\n]+
   2. If models need changes feel free.

5. When you finish, please:
   1. Commit all changes.
   2. Create patch using git with filename in format `firstName-lastName.patch`.
   3. Patch should contain all changes as one commmit.
   4. Make sure patch contains only source code you have added/changed.
   5. Send us only patch file.

6. IMPORTANT:
   1. Please do not change example_data.csv file.
   2. After upload patch in couple of days we will run automatic tests:
      a) on example_data.csv
      b) on our data (one of them contains 1 mln of prepared rows)
   3. Patch that passes tests will be reviewed by our team.
   4. Any errors in code are intentional. If needed, handle them as part of task.
   5. Efficiency of code / run time is crucial in this task.
   6. Purpose of this task if to check your proficiency level. So give your best.
   7. **Feedback is possible only if code passes tests**
