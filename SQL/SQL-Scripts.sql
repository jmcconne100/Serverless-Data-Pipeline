SELECT * FROM employees;

SELECT * FROM employees WHERE Department = 'IT';

SELECT * FROM employees WHERE Hire_Date > '2020-01-01';

SELECT Full_Name, Email FROM employees;

SELECT * FROM employees ORDER BY Salary DESC;

SELECT Department, AVG(Salary) AS avg_salary
FROM employees
GROUP BY Department;

SELECT Department, COUNT(*) AS num_employees
FROM employees
GROUP BY Department;

SELECT SUM(Salary) AS total_payroll FROM employees;

SELECT MAX(Salary) AS max_salary FROM employees;

SELECT *
FROM employees e
WHERE Salary > (
  SELECT AVG(Salary)
  FROM employees
  WHERE Department = e.Department
);

SELECT * FROM employees
WHERE YEAR(Hire_Date) = 2023;

SELECT * FROM employees
ORDER BY Hire_Date DESC
LIMIT 1;

SELECT Full_Name, ROUND(DATEDIFF(CURDATE(), Hire_Date)/365, 1) AS years_at_company
FROM employees;

SELECT * FROM employees
WHERE Full_Name IS NULL;

SELECT * FROM employees
ORDER BY Salary DESC
LIMIT 5;

SELECT * FROM employees
WHERE Department NOT IN ('HR', 'IT');

SELECT Full_Name, 
       SUBSTRING_INDEX(Email, '@', -1) AS domain
FROM employees;

SELECT * FROM employees
WHERE Email LIKE '%.org';

SELECT *, 
       RANK() OVER (PARTITION BY Department ORDER BY Salary DESC) AS dept_rank
FROM employees;

SELECT Department
FROM employees
GROUP BY Department
HAVING AVG(Salary) > 80000;
