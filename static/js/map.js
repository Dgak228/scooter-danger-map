ymaps.ready(function () {
    // Инициализация карты
    var myMap = new ymaps.Map('map', {
        center: [45.0448, 38.9760], // Краснодар
        zoom: 12,
        controls: ['zoomControl', 'fullscreenControl']
    });

    // Добавляем поиск по карте
    var searchControl = new ymaps.control.SearchControl({
        options: {
            provider: 'yandex#search'
        }
    });
    myMap.controls.add(searchControl);

    // Загружаем точки ДТП
    fetch('/api/dtp')
        .then(response => response.json())
        .then(points => {
            points.forEach(point => {
                var placemark = new ymaps.Placemark([point.lat, point.lon], {
                    balloonContent: point.desc
                }, {
                    preset: 'islands#redDotIcon'
                });
                myMap.geoObjects.add(placemark);
            });
        });

    // Обработчик построения маршрута
    document.getElementById('buildRoute').addEventListener('click', function() {
        var startAddress = document.getElementById('startAddress').value;
        var endAddress = document.getElementById('endAddress').value;

        if (!startAddress || !endAddress) {
            alert('Пожалуйста, введите начальный и конечный адреса');
            return;
        }

        // Очищаем предыдущий маршрут
        myMap.geoObjects.removeAll();

        // Загружаем точки ДТП заново
        fetch('/api/dtp')
            .then(response => response.json())
            .then(points => {
                points.forEach(point => {
                    var placemark = new ymaps.Placemark([point.lat, point.lon], {
                        balloonContent: point.desc
                    }, {
                        preset: 'islands#redDotIcon'
                    });
                    myMap.geoObjects.add(placemark);
                });
            });

        // Запрашиваем маршрут
        fetch('/api/route', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                start: startAddress,
                end: endAddress
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert('Ошибка: ' + data.error);
                return;
            }

            // Строим маршрут
            var route = new ymaps.multiRouter.MultiRoute({
                referencePoints: [
                    [data.route.routes[0].legs[0].startLocation.latLng.latitude, 
                     data.route.routes[0].legs[0].startLocation.latLng.longitude],
                    [data.route.routes[0].legs[0].endLocation.latLng.latitude, 
                     data.route.routes[0].legs[0].endLocation.latLng.longitude]
                ],
                params: {
                    routingMode: 'bicycle'
                }
            }, {
                boundsAutoApply: true
            });

            myMap.geoObjects.add(route);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Произошла ошибка при построении маршрута');
        });
    });
}); 