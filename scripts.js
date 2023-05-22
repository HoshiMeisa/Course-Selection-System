async function login() {
    // 这里只是一个简单的例子，实际上你需要验证用户名和密码
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    if (username === '1' && password === '1') {
      document.getElementById('loginForm').style.display = 'none';
      document.getElementById('coursesTable').style.display = '';
      await loadCourses();
    } else {
      alert('用户名或密码错误');
    }
  }
  
  async function loadCourses() {
    // 这里只是一个简单的例子，实际上你需要从 JSON 文件中读取数据
    const response = await fetch('data.json');
    const data = await response.json();
    const courses = data.courses;
    
    const tbody = document.getElementById('coursesBody');
    courses.forEach(course => {
      const row = document.createElement('tr');
      row.innerHTML = `
        <td>${course.id}</td>
        <td>${course.name}</td>
        <td>${course.credits}</td>
        <td>${course.maxStudents}</td>
        <td>${course.teacher}</td>
        <td>${course.grade}</td>
        <td>${course.location}</td>
      `;
      tbody.appendChild(row);
    });
  }
  