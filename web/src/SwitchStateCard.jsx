import { sensorIcons } from "./icons/IconIndex";

function SwitchStateCard({ name, reading, uptime, avgUptime, downtime, color }) {

  const IconComponent = sensorIcons[name.toLowerCase()];

  // XXX We could avoid adding extra icons by simply making the live icon a different color
  const StateIcon = sensorIcons[reading.toLowerCase()]

  const stats = [
    { name: "on", value: uptime },
    { name: "average", value: avgUptime },
    { name: "off", value: downtime }
  ];

  return (
    <div className="sensorCard">
      <div className="sensorName" style={{color}}>{IconComponent && <IconComponent />} {name.toLowerCase()}</div>
      <div className="sensorReading">{StateIcon && <StateIcon />} {reading}</div>

      <div className="sensorStats">
        {stats.map(({ name, value }) => {
          const Icon = sensorIcons[name];

          return (
            <div name={name} className="statRow">
              {Icon && <Icon />} {value}m
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default SwitchStateCard;