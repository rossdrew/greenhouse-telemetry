import { useEffect, useState } from "react";
import { sensorIcons } from "./icons/IconIndex";
import { water } from "./api";

function WaterButton({ pumpOn, secondsRemaining, defaultSeconds, maxSeconds, onChanged }) {
  const [seconds, setSeconds] = useState(defaultSeconds);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState(null);
  const [displaySeconds, setDisplaySeconds] = useState(secondsRemaining);

  const WaterIcon = sensorIcons["water"];

  // Resync from the server on every poll, then tick down locally in between polls so the
  // countdown doesn't visibly jump/stall between 5s status refreshes.
  useEffect(() => {
    setDisplaySeconds(secondsRemaining);
    if (!pumpOn) return undefined;

    const tickId = setInterval(() => {
      setDisplaySeconds((prev) => (prev == null ? prev : Math.max(0, prev - 1)));
    }, 1000);
    return () => clearInterval(tickId);
  }, [pumpOn, secondsRemaining]);

  const handleWater = async () => {
    setBusy(true);
    setError(null);
    try {
      await water(seconds);
      onChanged?.();
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="sensorCard waterControl">
      <div className="sensorName">{WaterIcon && <WaterIcon />} water</div>
      <div className="sensorReading">
        {pumpOn ? `${Math.ceil(displaySeconds ?? 0)}s` : "Idle"}
      </div>

      <label className="waterSeconds">
        seconds
        <input
          type="number"
          min={1}
          max={maxSeconds}
          value={seconds}
          disabled={pumpOn || busy}
          onChange={(e) => setSeconds(Number(e.target.value))}
        />
      </label>

      <button type="button" onClick={handleWater} disabled={pumpOn || busy}>
        {pumpOn ? "Watering…" : "Water now"}
      </button>

      {error && <div className="statusError">{error}</div>}
    </div>
  );
}

export default WaterButton;
