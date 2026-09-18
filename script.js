document.addEventListener("DOMContentLoaded", function () {

    const sosBtn = document.getElementById("sosBtn");
    const alarmSound = document.getElementById("alarmSound");

    if (sosBtn) {

        sosBtn.addEventListener("click", function () {

            // Play emergency alarm
            alarmSound.currentTime = 0;
            alarmSound.loop = true;
            alarmSound.play();

            if (navigator.geolocation) {

                navigator.geolocation.getCurrentPosition(

                    function (position) {

                        let lat = position.coords.latitude;
                        let lon = position.coords.longitude;

                        let mapLink =
                            `https://www.google.com/maps?q=${lat},${lon}`;

                        fetch('/sos', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({
                                latitude: lat,
                                longitude: lon,
                                map: mapLink
                            })
                        });

                        alert("🚨 SOS ALERT SENT 🚨");

                        window.open(mapLink, "_blank");

                    },

                    function (error) {

                        alert(
                            "Error Code: " + error.code +
                            "\nMessage: " + error.message
                        );

                        console.error("Geolocation error:", error);

                    }

                );

            } else {

                alert("Geolocation is not supported.");
            
            }

        });

    }

});

function stopAlarm() {

    let alarmSound = document.getElementById("alarmSound");

    alarmSound.pause();
    alarmSound.currentTime = 0;

}
