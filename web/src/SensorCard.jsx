import { sensorIcons } from "./icons/IconIndex";

function SensorCard({ name, reading, high, avg, low, color }) {

  const IconComponent = sensorIcons[name.toLowerCase()];

  const stats = [
    { name: "high", value: high },
    { name: "average", value: avg },
    { name: "low", value: low }
  ].filter(({ value }) => value != null);

  return (
    <div className="sensorCard">
      <div className="sensorName" style={{color}}>{IconComponent && <IconComponent />} {name.toLowerCase()}</div>
      <div className="sensorReading">{reading}</div>

      <div className="sensorStats">
        {stats.map(({ name, value }) => {
          const Icon = sensorIcons[name];

          return (
            <div key={name} name={name} className="statRow">
              {Icon && <Icon />} {value}
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default SensorCard;