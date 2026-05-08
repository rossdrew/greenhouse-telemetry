import { useState, useEffect } from 'react';

function Clock() {
    const [currentTime, setCurrentTime] = useState(new Date());

    useEffect(() => {
        const timerId = setInterval(() => {
            setCurrentTime(new Date());
        }, 1000);

        return () => clearInterval(timerId);
    }, []);

    return (
        <div className="sensorCard">
            <div className="sensorName">Current Time</div>
            <div className="sensorReading">{currentTime.toLocaleTimeString()}</div>
        </div>
    );
}

export default Clock;