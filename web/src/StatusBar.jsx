import { useCallback, useEffect, useState } from 'react';
import Clock from './Clock';
import SensorCard from './SensorCard';
import LightSwitchCard from './LightSwitchCard';
import WaterButton from './WaterButton';
import { getStatus } from './api';

const POLL_INTERVAL_MS = 5000;

function formatReading(value, unit) {
  return value == null ? 'N/A' : `${value.toFixed(1)}${unit}`;
}

function StatusBar() {
  const [status, setStatus] = useState(null);
  const [error, setError] = useState(null);

  const refresh = useCallback(() => {
    return getStatus()
      .then((data) => {
        setStatus(data);
        setError(null);
      })
      .catch((err) => {
        setError(err.message);
      });
  }, []);

  useEffect(() => {
    refresh();
    const timerId = setInterval(refresh, POLL_INTERVAL_MS);
    return () => clearInterval(timerId);
  }, [refresh]);

  return (
    <section id="center-stretch">

      <div className="left">
        <SensorCard
          name="Temperature"
          reading={status ? formatReading(status.temperature, 'C') : '…'}
          color="#9e743d"
        />
        <SensorCard
          name="Humidity"
          reading={status ? formatReading(status.humidity, '%') : '…'}
          color="#21deff"
        />
        <SensorCard
          name="Moisture"
          reading={status ? formatReading(status.soil_moisture_percent, '%') : '…'}
          color="#3d9e5c"
        />
      </div>

      <div className="center">
        {status && (
          <>
            <LightSwitchCard on={status.light_on} onChanged={refresh} />
            <WaterButton
              pumpOn={status.pump_on}
              secondsRemaining={status.pump_seconds_remaining}
              defaultSeconds={status.default_pump_seconds}
              maxSeconds={status.max_pump_seconds}
              onChanged={refresh}
            />
          </>
        )}
      </div>

      <div className="right">
        {error && <div className="statusError">Can't reach greenhouse API: {error}</div>}
        <Clock />
      </div>

    </section>
  );
}

export default StatusBar;
