document.getElementById('toggleSearchBtn').addEventListener('click', function() {
    const overlay = document.getElementById('overlay');
    const searchForm = document.querySelector('.search-form');
    if (overlay.style.display === 'none') {
      overlay.style.display = 'flex';
    } else {
      overlay.style.display = 'none';
      document.getElementById('cancelSearchBtn').style.display = 'none';
      document.getElementById('searchBtn').innerText = 'Искать';
    }
  });
  
  document.getElementById('searchBtn').addEventListener('click', function() {
    const lastName = document.getElementById('lastName').value;
    const firstName = document.getElementById('firstName').value;
    const birthDate = document.getElementById('birthDate').value;
    const uploadDate = document.getElementById('uploadDate').value;
    const errorMessage = document.getElementById('errorMessage');
  
    if (!lastName && !firstName && !birthDate && !uploadDate) {
      errorMessage.style.display = 'block';
    } else {
      errorMessage.style.display = 'none';
      const formData = {
        lastName: lastName,
        firstName: firstName,
        birthDate: birthDate,
        uploadDate: uploadDate
      };
  
      fetch('/search', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
        console.log('Success:', data);
        renderSearchResults(data); // Отображение результатов поиска
        document.getElementById('overlay').style.display = 'none'; // Скрытие формы поиска
        document.getElementById('cancelSearchBtn').style.display = 'inline'; // Отображение кнопки отмены поиска
        document.getElementById('searchBtn').innerText = 'Поиск снова'; // Изменение текста кнопки поиска
        })
        .catch((error) => {
        console.error('Error:', error);
        });
        }
        });
        document.getElementById('cancelSearchBtn').addEventListener('click', function() {
  fetch('/dashboard/first_five_json')
    .then(response => response.json())
    .then(data => {
      renderSearchResults(data); // Отображение первых пяти записей
      document.getElementById('overlay').style.display = 'none'; // Скрытие формы поиска
      document.getElementById('cancelSearchBtn').style.display = 'none'; // Скрытие кнопки отмены поиска
      document.getElementById('searchBtn').innerText = 'Искать'; // Возвращение исходного текста
    })
    .catch(error => console.error('Error:', error));
  });
  
  function renderSearchResults(data) {
    const tableBody = document.querySelector('.history_lists table tbody');
    tableBody.innerHTML = '';
    data.forEach(note => {
      const row = document.createElement('tr');
      row.innerHTML = `
        <td>${note.id}</td>
        <td>${note.date_of_birth}</td>
        <td>${note.date_of_upload}</td>
        <td>${note.first_name}</td>
        <td>${note.last_name}</td>
        <td>
          <a href="/detail/${note.id}">Показать больше</a>
          <button type="button" class="save-btn">
            <i class="fa-solid fa-save fa-2x"></i>
          </button>
        </td>
      `;
      tableBody.appendChild(row);
    });
  }
  
  document.getElementById('toggleTableBtn').addEventListener('click', function() {
    const tableBody = document.querySelector('.history_lists table tbody');
    if (!isTableVisible) {
      fetch('/dashboard/all_json')
        .then(response => response.json())
        .then(data => {
          tableBody.innerHTML = '';
          data.forEach(note => {
            const row = document.createElement('tr');
            row.innerHTML = `
              <td>${note.id}</td>
              <td>${note.date_of_birth}</td>
              <td>${note.date_of_upload}</td>
              <td>${note.first_name}</td>
              <td>${note.last_name}</td>
              <td>
                <a href="/detail/${note.id}">Показать больше</a>
                <button type="button" class="save-btn">
                  <i class="fa-solid fa-save fa-2x"></i>
                </button>
              </td>
            `;
            tableBody.appendChild(row);
          });
          this.textContent = 'Скрыть';
          isTableVisible = true;
        })
        .catch(error => console.error('Error:', error));
    } else {
      fetch('/dashboard/first_five_json')
        .then(response => response.json())
        .then(data => {
          renderSearchResults(data); 
          this.textContent = 'Больше';
          isTableVisible = false;
        })
        .catch(error => console.error('Error:', error));
    }
  });
  