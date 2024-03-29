const userId = 1; // ID пользователя, чей статус нужно проверить

function checkOnlineStatus() {
    fetch(`/api/user-status/${userId}`)
        .then(response => response.json())
        .then(data => {
            if (data.status) {
                // Отобразить "Online"
            } else {
                // Отобразить "Offline"
            }
        });
}

setInterval(checkOnlineStatus, 5000); // Проверка статуса
