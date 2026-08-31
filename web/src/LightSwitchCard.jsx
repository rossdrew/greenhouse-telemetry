import { useState } from "react";
import { sensorIcons } from "./icons/IconIndex";
import { setLight } from "./api";

function LightSwitchCard({ on, disabled, onChanged }) {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState(null);

  const IconComponent = sensorIcons["sunlight"];
  const StateIcon = sensorIcons[on ? "on" : "off"];

  const toggle = async () => {
    setBusy(true);
    setError(null);
    try {
      await setLight(!on);
      onChanged?.();
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  };

  return (
    <button
      type="button"
      className="sensorCard"
      onClick={toggle}
      disabled={disabled || busy}
    >
      <div className="sensorName">{IconComponent && <IconComponent />} light</div>
      <div className="sensorReading">{StateIcon && <StateIcon />} {on ? "ON" : "OFF"}</div>
      {error && <div className="statusError">{error}</div>}
    </button>
  );
}

export default LightSwitchCard;
